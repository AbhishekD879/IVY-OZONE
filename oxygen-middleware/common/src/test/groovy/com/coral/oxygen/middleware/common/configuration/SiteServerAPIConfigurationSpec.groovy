package com.coral.oxygen.middleware.common.configuration

import javax.net.ssl.ExtendedSSLSession
import org.springframework.beans.factory.annotation.Autowired
import com.egalacoral.spark.siteserver.api.SiteServerApi
import spock.lang.Specification

class SiteServerAPIConfigurationSpec extends Specification{

  SiteServerAPIConfiguration siteServerAPIConfiguration;

  def "Check SiteserverAPI Obj"() {
    given:
    siteServerAPIConfiguration = new SiteServerAPIConfiguration()
    siteServerAPIConfiguration.level=SiteServerApi.Level.BASIC
    siteServerAPIConfiguration.keepAliveSeconds=3
    siteServerAPIConfiguration.baseUrl="https://ss-tst2.coral.co.uk/"
    expect:
    siteServerAPIConfiguration.getSiteServerAPI() != null
  }


  def "Check SiteserverAPI version"() {
    given:
    siteServerAPIConfiguration = new SiteServerAPIConfiguration()
    siteServerAPIConfiguration.level=SiteServerApi.Level.BASIC
    siteServerAPIConfiguration.keepAliveSeconds=3
    siteServerAPIConfiguration.priceBoostEnabled=true
    siteServerAPIConfiguration.latestApiVersion=2.61
    siteServerAPIConfiguration.baseUrl="https://ss-tst2.coral.co.uk/"
    expect:
    siteServerAPIConfiguration.getSiteServerAPI() != null
  }
}
