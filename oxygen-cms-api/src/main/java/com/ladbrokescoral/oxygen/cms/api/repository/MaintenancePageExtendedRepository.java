package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import java.time.Instant;
import java.util.List;

public interface MaintenancePageExtendedRepository {
  List<MaintenancePage> findMaintenancePages(String brand, String deviceType);

  List<MaintenancePage> findMaintenancePagesWithEndDateAfter(String brand, Instant endDate);
}
