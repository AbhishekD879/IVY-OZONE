package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.ladbrokescoral.oxygen.cms.api.entity.Brand
import com.ladbrokescoral.oxygen.cms.api.exception.UnknownBrandException
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProviderImpl
import com.ladbrokescoral.oxygen.cms.configuration.SiteServerApiConfiguration
import spock.lang.Specification

class SiteServeApiProviderSpec extends Specification {

  BrandService brandService = Mock(BrandService)
  SiteServerApiConfiguration apiConfiguration = Mock(SiteServerApiConfiguration)

  SiteServerApi bmaSiteServerApi = Mock(SiteServerApi)
  SiteServerApi ladbrokesSiteServerApi = Mock(SiteServerApi)
  SiteServerApi defaultSiteServerApi = Mock(SiteServerApi)

  SiteServeApiProvider siteServeApiProvider

  def setup() {
    apiConfiguration.siteServerAPI("bma-siteserve-url") >> bmaSiteServerApi
    apiConfiguration.siteServerAPI("ladbrokes-siteserve-url") >> ladbrokesSiteServerApi
    apiConfiguration.siteServerAPI() >> defaultSiteServerApi
  }


  def "test get siteServeApi by brand"() {

    given: "Cms contains bma brand with configured siteServeApi:"
    Brand bma = new Brand()
    bma.setBrandCode("bma")
    bma.setSiteServerEndPoint("bma-siteserve-url")

    and: "ladbrokes brand with configured siteServeApi"
    Brand ladbrokes = new Brand()
    ladbrokes.setBrandCode("ladbrokes")
    ladbrokes.setSiteServerEndPoint("ladbrokes-siteserve-url")

    and: "rcomb brand with not configured siteServeApi"
    Brand rcomb = new Brand()
    rcomb.setBrandCode("rcomb")

    and: "brand service returns 3 known brands"
    brandService.findAll() >> Arrays.asList(bma, ladbrokes, rcomb)

    and: "siteServeApiProvider is initialized"
    siteServeApiProvider = new SiteServeApiProviderImpl(brandService, apiConfiguration)
    siteServeApiProvider.initApis()

    when: "get siteServeApi by bma brand"
    SiteServerApi api = siteServeApiProvider.api("bma")

    then: "siteServeApi is returned. It makes calls to bma-siteserve-url url"
    bmaSiteServerApi == api

    when: "get siteServeApi by ladbrokes brand"
    api = siteServeApiProvider.api("ladbrokes")

    then: "siteServeApi is returned. It makes calls to ladbrokes-siteserve-url url"
    ladbrokesSiteServerApi == api

    when: "get siteServeApi by rcomb brand"
    api = siteServeApiProvider.api("rcomb")

    then: "siteServeApi is returned. It makes calls to default siteserve-url url"
    defaultSiteServerApi == api

    when: "get siteServeApi by unknown brand"
    siteServeApiProvider.api("unknown")

    then: "UnknownBrandException is thrown"
    thrown UnknownBrandException
  }
}
