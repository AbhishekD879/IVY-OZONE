package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.service.MaintenancePageToPeriodConverter.*;
import static java.lang.Long.compare;
import static java.lang.Long.max;
import static org.apache.commons.lang3.BooleanUtils.isTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePageNotification;
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceRequest;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceResponse;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceService;
import java.io.IOException;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.annotation.PostConstruct;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class MaintenanceNotificationSchedulerService {

  private final DelayQueue<DelayedNotificationEvent> maintenanceQueue = new DelayQueue<>();
  private final MaintenancePageExtendedRepository maintenanceExtendedRepository;
  private final MaintenanceNotificationHistoryService maintenanceNotificationHistoryService;
  private final BppMaintenanceService bppMaintenanceService;
  private Set<String> supportedBrands;

  @PostConstruct
  public void initNotifications() {
    supportedBrands = bppMaintenanceService.getSupportedBrands();
    if (!supportedBrands.isEmpty()) {
      supportedBrands.forEach(this::initBrandNotifications);

      // to be able to turn on maintenance simultaneously for two brands
      int watchersCount = supportedBrands.size();
      ExecutorService executorService = Executors.newFixedThreadPool(watchersCount);
      for (int i = 0; i < watchersCount; i++) {
        executorService.execute(this::watchMaintenanceMode);
      }
    }
  }

  protected void updateNotifications(MaintenancePage maintenancePage) {
    String brand = maintenancePage.getBrand();
    if (supportedBrands.contains(brand)) {
      stopRecentMaintenance(brand);
      initBrandNotifications(brand);
    } else {
      log.warn("{} brand is not supported for maintenance notifications", brand);
    }
  }

  private void initBrandNotifications(String brand) {
    List<MaintenancePage> maintenance =
        maintenanceExtendedRepository.findMaintenancePagesWithEndDateAfter(brand, Instant.now());
    List<DelayedNotificationEvent> notificationItems = toNotificationItems(maintenance);
    maintenanceQueue.removeIf(i -> brand.equals(i.getBrand()));
    maintenanceQueue.addAll(notificationItems);
  }

  private void stopRecentMaintenance(String brand) {
    maintenanceNotificationHistoryService
        .getLastNotification(brand)
        .filter(MaintenancePageNotification::isActivateMaintenance)
        .ifPresent(
            n ->
                sendMaintenanceNotification(
                    newDeactivateMaintenanceEvent(n.getBrand(), System.currentTimeMillis())));
  }

  private void watchMaintenanceMode() {
    while (!Thread.currentThread().isInterrupted()) {
      try {
        DelayedNotificationEvent nextNotification = maintenanceQueue.take();
        validateAndSendMaintenanceNotification(nextNotification);
      } catch (Exception e) {
        log.error("Failed to process next maintenance notification", e);
      }
    }
  }

  private void validateAndSendMaintenanceNotification(DelayedNotificationEvent notification) {
    if (isValid(notification)) {
      sendMaintenanceNotification(notification);
    } else {
      log.info(
          "Skip maintenance notification to activate({}) for {}, not valid any more",
          notification.isActivateMaintenance(),
          notification.getBrand());
    }
  }

  private boolean isValid(DelayedNotificationEvent notification) {
    List<MaintenancePage> newMaintenancePages =
        getMaintenancePagesEndingNear(notification.getBrand(), notification.getTriggerTimestamp());
    Set<BrandMaintenancePeriod> brandMaintenancePeriods =
        convertToMaintenancePeriods(notification.getBrand(), newMaintenancePages);

    return brandMaintenancePeriods.stream()
        .anyMatch(
            n ->
                notification.isActivateMaintenance()
                    ? n.getStart() == notification.getTriggerTimestamp()
                    : n.getEnd() == notification.getTriggerTimestamp());
  }

  private List<MaintenancePage> getMaintenancePagesEndingNear(String brand, long triggerTimestamp) {
    Instant minEndDate = Instant.ofEpochMilli(triggerTimestamp - TimeUnit.SECONDS.toMillis(10));
    return maintenanceExtendedRepository.findMaintenancePagesWithEndDateAfter(brand, minEndDate);
  }

  private void sendMaintenanceNotification(DelayedNotificationEvent notification) {
    try {
      BppMaintenanceRequest bppRequest =
          new BppMaintenanceRequest(
              notification.isActivateMaintenance(),
              TimeUnit.MILLISECONDS.toSeconds(notification.ttlMillis));
      BppMaintenanceResponse bppResponse =
          bppMaintenanceService.sendNotification(notification.getBrand(), bppRequest);
      log.info(
          "Sent maintenance active {} to URL {}, response: code {}, body {}",
          notification.isActivateMaintenance(),
          bppResponse.getUrl(),
          bppResponse.getCode(),
          bppResponse.getMessage());
      maintenanceNotificationHistoryService.save(
          notification.getBrand(), notification.getTriggerTimestamp(), bppRequest, bppResponse);
    } catch (IOException e) {
      log.error(
          "Failed to send maintenance active {} for brand {}",
          notification.isActivateMaintenance(),
          notification.getBrand());
    }
  }

  private List<DelayedNotificationEvent> toNotificationItems(List<MaintenancePage> maintenance) {
    Map<String, List<MaintenancePage>> activeByBrand =
        maintenance.stream()
            .filter(p -> Objects.nonNull(p.getBrand()))
            .filter(p -> isTrue(p.getDesktop()) || isTrue(p.getMobile()) || isTrue(p.getTablet()))
            .collect(Collectors.groupingBy(MaintenancePage::getBrand, Collectors.toList()));
    return activeByBrand.entrySet().stream()
        .flatMap(e -> toNotificationItems(e.getKey(), e.getValue()))
        .collect(Collectors.toList());
  }

  private Stream<DelayedNotificationEvent> toNotificationItems(
      String brand, List<MaintenancePage> maintenance) {
    if (maintenance.isEmpty()) {
      return Stream.empty();
    }
    Set<BrandMaintenancePeriod> maintenancePeriods =
        convertToMaintenancePeriods(brand, maintenance);
    return maintenancePeriods.stream()
        .flatMap(
            m ->
                Stream.of(
                    newActivateMaintenanceEvent(
                        m.getBrand(),
                        m.getStart(),
                        m.getEnd() - max(m.getStart(), System.currentTimeMillis())),
                    newDeactivateMaintenanceEvent(m.getBrand(), m.getEnd())));
  }

  private static DelayedNotificationEvent newActivateMaintenanceEvent(
      String brand, long triggerTimestamp, long ttlMillis) {
    return new DelayedNotificationEvent(brand, triggerTimestamp, true, ttlMillis);
  }

  private static DelayedNotificationEvent newDeactivateMaintenanceEvent(
      String brand, long triggerTimestamp) {
    return new DelayedNotificationEvent(brand, triggerTimestamp, false, 0);
  }

  @Getter
  @RequiredArgsConstructor
  private static class DelayedNotificationEvent implements Delayed {
    private final String brand;
    private final long triggerTimestamp;
    private final boolean activateMaintenance;

    private final long ttlMillis;

    @Override
    public long getDelay(TimeUnit unit) {
      return unit.convert(triggerTimestamp - System.currentTimeMillis(), TimeUnit.MILLISECONDS);
    }

    @Override
    public int compareTo(Delayed o) {
      return compare(this.getDelay(TimeUnit.MILLISECONDS), o.getDelay(TimeUnit.MILLISECONDS));
    }
  }
}
