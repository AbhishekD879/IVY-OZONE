package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl
import spock.lang.Specification

class SiteServeServiceTestHasCategoryEventsSpec extends Specification {

  SiteServerApi siteServerApiMock
  SiteServeService siteServeService
  SiteServeApiProvider serveApiProviderMock

  def setup() {
    serveApiProviderMock = Mock(SiteServeApiProvider)
    siteServerApiMock = Mock(SiteServerApi)
    siteServeService = new SiteServeServiceImpl(serveApiProviderMock)
    serveApiProviderMock.api("bma") >> siteServerApiMock
  }

  def "category has not events" () {
    given:
    siteServerApiMock.getEvent(_ as List, _ as Optional, _ as Optional) >> Optional.of(Collections.emptyList())

    when:
    Boolean result = siteServeService.hasSiteServeCategoryEvents("bma", 16)

    then:
    !result
  }

  def "category has events" () {
    given:
    Event event = new Event();
    siteServerApiMock.getEvent(_ as List, _ as Optional, _ as Optional) >> Optional.of(Collections.singletonList(event))

    when:
    Boolean result = siteServeService.hasSiteServeCategoryEvents("bma", 16)

    then:
    result
  }

  def "category has not events when categoryId is null" () {
    given:
    Event event = new Event()
    siteServerApiMock.getEvent(_ as List, _ as Optional, _ as Optional) >> Optional.of(Collections.singletonList(event))

    when:
    Boolean result = siteServeService.hasSiteServeCategoryEvents("bma", null)

    then:
    !result
  }
}
