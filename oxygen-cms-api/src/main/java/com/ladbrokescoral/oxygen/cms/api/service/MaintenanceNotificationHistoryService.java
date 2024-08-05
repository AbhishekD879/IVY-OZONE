package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePageNotification;
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenanceNotificationRepository;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceRequest;
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceResponse;
import java.time.Instant;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class MaintenanceNotificationHistoryService {

  private final MaintenanceNotificationRepository repository;

  public Optional<MaintenancePageNotification> getLastNotification(String brand) {
    return repository.findByBrand(brand, Sort.by(Sort.Direction.DESC, "createdAt")).stream()
        .findFirst();
  }

  public void save(
      String brand,
      long scheduledTime,
      BppMaintenanceRequest request,
      BppMaintenanceResponse response) {
    MaintenancePageNotification notificationHistory = new MaintenancePageNotification();
    notificationHistory.setBrand(brand);
    notificationHistory.setActivateMaintenance(request.isActive());
    notificationHistory.setUrl(response.getUrl());
    notificationHistory.setStatus(response.getStatus());
    notificationHistory.setTriggeredDate(Instant.ofEpochMilli(scheduledTime));
    notificationHistory.setTtlSeconds(request.getTtl());

    repository.save(notificationHistory);
  }
}
