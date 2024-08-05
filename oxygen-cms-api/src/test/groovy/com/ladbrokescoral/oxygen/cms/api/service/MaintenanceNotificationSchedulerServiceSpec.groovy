package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceService
import spock.lang.Specification

class MaintenanceNotificationSchedulerServiceSpec extends Specification {

  public static final String BRAND = "brand"
  MaintenanceNotificationSchedulerService service

  MaintenancePageExtendedRepository extendedRepository
  MaintenanceNotificationHistoryService notificationService
  BppMaintenanceService bppMaintenanceService

  def setup() {
    extendedRepository = Mock()
    notificationService = Mock()
    bppMaintenanceService = Mock()
    bppMaintenanceService.getSupportedBrands() >> Collections.singleton(BRAND)
    extendedRepository.findMaintenancePagesWithEndDateAfter(*_) >> Collections.emptyList()
    service = new MaintenanceNotificationSchedulerService(extendedRepository, notificationService, bppMaintenanceService)
    service.initNotifications()
  }

  def "update migration"(){
    given:
    MaintenancePage maintenancePage = new MaintenancePage()
    maintenancePage.setBrand(BRAND)

    when:
    service.updateNotifications(maintenancePage)

    then:
    1 * notificationService.getLastNotification(*_) >> Optional.empty()
  }
}
