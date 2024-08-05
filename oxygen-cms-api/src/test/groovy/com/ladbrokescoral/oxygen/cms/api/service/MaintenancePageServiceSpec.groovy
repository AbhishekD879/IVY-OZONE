package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageRepository
import org.springframework.data.domain.PageImpl
import org.springframework.data.domain.PageRequest
import spock.lang.Specification
import org.springframework.data.domain.Unpaged

class MaintenancePageServiceSpec extends Specification {

  MaintenanceNotificationSchedulerService maintenanceNotificationService
  MaintenancePageRepository repositoryMock

  def maintenancePageService
  String size = "1x1"

  def setup() {
    repositoryMock = Mock()
    maintenanceNotificationService = Mock(MaintenanceNotificationSchedulerService)
    maintenancePageService = new MaintenancePageService(repositoryMock, null, maintenanceNotificationService, size, size, size)
  }

  def "set sortOrder = -1 for new entity if all old entities do not have any sortOrder"() {
    given: "All old entities do not have sortOrder value"
    repositoryMock.findAll(_ as PageRequest) >> new PageImpl(Collections.singletonList(new MaintenancePage()), Unpaged.INSTANCE, 0)

    and: "new entity without sortOrder"
    MaintenancePage maintenancePage = new MaintenancePage()

    when:
    maintenancePageService.incrementSortOrder(maintenancePage)

    then: "new entity should has sortOrder -1"
    maintenancePage.getSortOrder() == -1.0
  }

  def "Update maintenance notification on Save"() {

    given:
    def page = new MaintenancePage()

    when:
    maintenancePageService.save(page)

    then:
    1 * repositoryMock.save(page) >> page
    1 * maintenanceNotificationService.updateNotifications(page)
  }

  def "Update maintenance notification on Delete"() {

    given:
    def page = new MaintenancePage()

    when:
    def pageId = "id"
    page.setId(pageId)
    repositoryMock.findById(pageId) >> Optional.of(page)
    maintenancePageService.delete(pageId)

    then:
    1 * maintenanceNotificationService.updateNotifications(page)
  }
}
