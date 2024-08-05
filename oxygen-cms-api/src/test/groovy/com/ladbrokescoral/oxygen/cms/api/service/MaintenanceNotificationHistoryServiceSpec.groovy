package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePageNotification
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenanceNotificationRepository
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceRequest
import com.ladbrokescoral.oxygen.cms.api.service.bpp.maintenance.BppMaintenanceResponse

import java.time.Instant

import spock.lang.Specification

class MaintenanceNotificationHistoryServiceSpec extends Specification {

  MaintenanceNotificationRepository repositoryMock
  MaintenanceNotificationHistoryService notificationHistoryService

  def setup() {
    repositoryMock = Mock()
    notificationHistoryService = new MaintenanceNotificationHistoryService(repositoryMock)
  }


  def "GetLastNotification"() {
    def expectedNotification = new MaintenancePageNotification()
    when:
    repositoryMock.findByBrand(*_) >> Collections.singletonList(expectedNotification)
    def actualNotification = notificationHistoryService.getLastNotification("brand")

    then:
    actualNotification.isPresent()
    actualNotification.get() == expectedNotification
  }

  def "Save"() {
    def brand = "brand"
    def triggeredTime = Instant.now().toEpochMilli()
    def activate = true
    def ttlSeconds = 10
    def url = "http://localhost/"
    def statusCode = 200
    def statusMessage = "OK"

    def expectedNotification = new MaintenancePageNotification()
    expectedNotification.setBrand(brand)
    expectedNotification.setTriggeredDate(Instant.ofEpochMilli(triggeredTime))
    expectedNotification.setActivateMaintenance(activate)
    expectedNotification.setTtlSeconds(ttlSeconds)
    expectedNotification.setUrl(url)
    expectedNotification.setStatus(statusMessage)

    when:
    notificationHistoryService.save(brand, triggeredTime,
        new BppMaintenanceRequest(activate, ttlSeconds), new BppMaintenanceResponse(url, statusCode, statusMessage, "Done"))

    then:
    1 * repositoryMock.save(expectedNotification)
  }
}
