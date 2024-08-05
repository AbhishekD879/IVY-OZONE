package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.CategoryEntity
import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl
import spock.lang.Specification

class SiteServeServiceTestIsCategoryNotValidOrHasEventsSpec extends Specification {

  SiteServerApi siteServerApiMock
  SiteServeService siteServeService
  SiteServeApiProvider siteServeApiProviderMock

  def setup() {
    siteServeApiProviderMock = Mock(SiteServeApiProvider)
    siteServerApiMock = Mock(SiteServerApi)
    siteServeService = new SiteServeServiceImpl(siteServeApiProviderMock)
    siteServeApiProviderMock.api("bma") >> siteServerApiMock
  }

  def "isCategoryNotValidOrHasEvents returns true if category is not valid" () {
    given:
    siteServerApiMock.getCategory("16", Optional.empty(), Optional.empty(), true) >> Optional.empty()

    when:
    Boolean result = siteServeService.isCategoryNotValidOrHasEvents("bma", 16)

    then:
    result
  }

  def "isCategoryNotValidOrHasEvents returns true if category is valid and has at least one event" () {
    given: "category is valid"
    CategoryEntity category = new CategoryEntity()
    category.id = 16

    siteServerApiMock.getCategory("16", Optional.empty(), Optional.empty(), true) >> Optional.of(category)

    and: "category has events"
    Event event = new Event();
    siteServerApiMock.getEvent(_ as List, _ as Optional, _ as Optional) >> Optional.of(Collections.singletonList(event))

    when:
    Boolean result = siteServeService.isCategoryNotValidOrHasEvents("bma", 16)

    then:
    result
  }

  def "isCategoryNotValidOrHasEvents returns false if category is valid and has not any events" () {
    given: "category is valid"
    CategoryEntity category = new CategoryEntity()
    category.id = 16

    siteServerApiMock.getCategory("16", Optional.empty(), Optional.empty(), true) >> Optional.of(category)

    and: "category has not events"
    siteServerApiMock.getEvent(_ as List, _ as Optional, _ as Optional) >> Optional.of(Collections.emptyList())

    when:
    Boolean result = siteServeService.isCategoryNotValidOrHasEvents("bma", 16)

    then:
    !result
  }
}
