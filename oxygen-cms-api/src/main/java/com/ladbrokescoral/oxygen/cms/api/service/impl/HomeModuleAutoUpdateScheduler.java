package com.ladbrokescoral.oxygen.cms.api.service.impl;

import static com.ladbrokescoral.oxygen.cms.api.entity.SelectionType.fromString;
import static com.ladbrokescoral.oxygen.cms.api.entity.SelectionType.getAutoRefreshTypes;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.EventsSelectionSetting;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.mapping.HomeModuleMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.HomeModuleRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.HomeModuleSiteServeService;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class HomeModuleAutoUpdateScheduler {

  private final HomeModuleSiteServeService homeModuleSiteServeService;
  private final HomeModuleRepository homeModuleRepository;
  private final ScheduledTaskExecutor masterSlaveExecutor;
  private final int daysDuration;

  @Autowired
  public HomeModuleAutoUpdateScheduler(
      HomeModuleSiteServeService homeModuleSiteServeService,
      HomeModuleRepository homeModuleRepository,
      @Value("${homeModule.removeExpired.afterDays}") int daysDuration,
      ScheduledTaskExecutor masterSlaveExecutor) {
    this.homeModuleSiteServeService = homeModuleSiteServeService;
    this.homeModuleRepository = homeModuleRepository;
    this.daysDuration = daysDuration;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  @Scheduled(cron = "${homeModule.removeExpired.cron}")
  public void removeExpiredEntities() {
    masterSlaveExecutor.execute(
        () ->
            homeModuleRepository.removeHomeModulesByVisibilityDisplayToBefore(
                Instant.now().minus(Duration.ofDays(daysDuration))));
  }

  @Scheduled(fixedDelayString = "${homeModule.autoRefresh.delayMillis}")
  public void refreshModulesEvents() {
    masterSlaveExecutor.execute(this::doRefreshModules);
  }

  private void doRefreshModules() {
    try {
      List<HomeModule> toRefresh =
          homeModuleRepository.findWithAutoRefreshAndSelectionTypeIn(
              Instant.now(), getAutoRefreshTypes());
      log.info("Found {} HomeModules for auto-refresh", toRefresh.size());
      List<HomeModule> updated =
          toRefresh.stream().filter(this::refreshEvents).collect(Collectors.toList());
      if (!updated.isEmpty()) {
        homeModuleRepository.saveAll(updated);
      }
    } catch (Exception e) {
      log.error("Failed to refresh modules", e);
    }
  }

  private boolean refreshEvents(HomeModule module) {
    if (module.getBrandsCount() != 1) {
      log.warn(
          "Cannot refresh HomeModule {} with brands count = {}",
          module.getId(),
          module.getBrandsCount());
      return false;
    }

    String brand = module.getBrand();
    List<SiteServeEventDto> events = getSiteServeEvents(module, brand);
    int removedCount = removeOutdatedEvents(module, events);
    int addedCount = addNewEventsIfNeeded(module, events);
    if (removedCount > 0 || addedCount > 0) {
      log.info(
          "Updated {} HomeModule events for brand {}, added: {}, removed: {}",
          module.getId(),
          brand,
          addedCount,
          removedCount);
      return true;
    }
    return false;
  }

  private int addNewEventsIfNeeded(HomeModule module, List<SiteServeEventDto> events) {
    int maxEvents = ObjectUtils.defaultIfNull(module.getMaxRows(), Integer.MAX_VALUE);
    List<HomeModuleData> moduleData = new ArrayList<>(module.getData());
    int eventsToAdd = Integer.min(maxEvents - moduleData.size(), events.size());
    if (eventsToAdd > 0) {
      Set<String> excludeIds = getEventsIds(moduleData);
      List<HomeModuleData> newEvents =
          events.stream()
              .filter(e -> !excludeIds.contains(e.getId()))
              .map(HomeModuleMapper.INSTANCE::toHomeModuleData)
              .limit(eventsToAdd)
              .collect(Collectors.toList());
      moduleData.addAll(newEvents);
      module.setData(moduleData);
      return newEvents.size();
    }
    return 0;
  }

  private Set<String> getEventsIds(List<HomeModuleData> moduleData) {
    return moduleData.stream().map(HomeModuleData::getId).collect(Collectors.toSet());
  }

  private int removeOutdatedEvents(HomeModule homeModule, List<SiteServeEventDto> events) {
    List<HomeModuleData> homeModuleData = new ArrayList<>(homeModule.getData());
    homeModule.setData(homeModuleData);
    int beforeDeletionCount = homeModuleData.size();
    homeModuleData.removeIf(data -> events.stream().noneMatch(e -> e.getId().equals(data.getId())));
    return beforeDeletionCount - homeModuleData.size();
  }

  private List<SiteServeEventDto> getSiteServeEvents(HomeModule module, String brand) {
    DataSelection dataSelection = module.getDataSelection();
    EventsSelectionSetting selectionDates = module.getEventsSelectionSettings();
    return homeModuleSiteServeService.loadEventsFromSiteServe(
        brand,
        fromString(dataSelection.getSelectionType()),
        dataSelection.getSelectionId(),
        selectionDates.getFrom(),
        selectionDates.getTo());
  }
}
