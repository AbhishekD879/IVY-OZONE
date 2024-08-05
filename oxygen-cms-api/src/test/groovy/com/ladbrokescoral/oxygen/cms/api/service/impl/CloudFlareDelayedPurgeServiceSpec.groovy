package com.ladbrokescoral.oxygen.cms.api.service.impl

import com.ladbrokescoral.oxygen.cms.api.entity.Dashboard
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService
import spock.lang.Specification

import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class CloudFlareDelayedPurgeServiceSpec extends Specification {
  private CloudFlareDelayedPurgeService purgeService
  private CloudFlareClient cloudFlareClient
  private DashboardService dashboardService
  private final String expectedRootUrl = "https://test.com"

  void setup() {
    dashboardService = Mock(DashboardService)
    cloudFlareClient = Mock(CloudFlareClient)
    def purgeUrls = new String[1]
    purgeUrls[0] = expectedRootUrl
    purgeService = new CloudFlareDelayedPurgeService(dashboardService, cloudFlareClient, 10, 0, 1,  "zoneId", purgeUrls)
  }

  void tearDown() {
    purgeService.shutdown()
  }

  def "PurgeCache with results"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)

    when:
    purgeService.purgeCache("bma", "somepath", "file.xml")
    latch.await(3, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME, Collections.emptySet()))
    1 * dashboardService.save(_) >> { args -> latch.countDown() }
  }

  def "PurgeCacheTags with results"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)
    cloudFlareClient.invalidate(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME, Collections.emptySet()))
    cloudFlareClient.invalidateCacheTags(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME_CACHE_TAG, Collections.emptySet()))
    dashboardService.save(_) >> { args -> latch.countDown() }

    when:
    purgeService.purgeCache("bma", "somepath", "file.xml", "CSP-tst0-bma")
    latch.await(3, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set)
    1 * cloudFlareClient.invalidateCacheTags(_ as String, _ as Set)
  }

  def "PurgeCache no results"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)
    cloudFlareClient.invalidate(*_) >> { args -> latch.countDown(); return Optional.empty() }

    when:
    purgeService.purgeCache("bma", "somepath", "file.xml")
    latch.await(3, TimeUnit.SECONDS)

    then:
    0 * dashboardService.save(_ as Dashboard)
  }

  def "GetRootUrl"() {
    when:
    def rootUrl = purgeService.getRootUrl()

    then:
    expectedRootUrl == rootUrl
  }
}
