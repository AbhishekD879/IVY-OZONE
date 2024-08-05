package com.coral.oxygen.middleware.common.cache

import com.coral.oxygen.middleware.common.configuration.cfcache.CloudFlareClient
import com.coral.oxygen.middleware.common.configuration.cfcache.CloudFlareDelayedPurgeService
import com.coral.oxygen.middleware.common.configuration.cfcache.InvalidateCacheResult
import spock.lang.Specification

import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class CloudFlareDelayedPurgeServiceSpec extends Specification {
  private CloudFlareDelayedPurgeService purgeService
  private CloudFlareClient cloudFlareClient
  private final String expectedRootUrl = "https://test.com"

  void setup() {
    cloudFlareClient = Mock(CloudFlareClient)
    def purgeUrls = new String[1]
    purgeUrls[0] = expectedRootUrl
    purgeService = new CloudFlareDelayedPurgeService(cloudFlareClient, 10, 0, 1,  1000,"zoneId", purgeUrls)
  }

  def tearDown() {
    when :
    purgeService.shutdown()
    then:
    0* purgeService.shutdown()
  }

  def "PurgeCache with results"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)
    when:
    purgeService.purgeCache("bma", "/somepath//", "file.xml")
    latch.await(3, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME, Collections.emptySet()))
  }

  def "PurgeCacheTags with results with purgeUrls with slash"() {
    given:
    def purgeUrlswithslash = new String[1]
    purgeUrlswithslash[0] = "https://test.com/"
    purgeService = new CloudFlareDelayedPurgeService(cloudFlareClient, 10, 0, 1,  1000,"zoneId", purgeUrlswithslash)
    CountDownLatch latch  = new CountDownLatch(1)
    cloudFlareClient.invalidate(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME, Collections.emptySet()))
    cloudFlareClient.invalidateCacheTags(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME_CACHE_TAG, Collections.emptySet()))

    when:
    purgeService.purgeCache("bma", "somepath/", "file.xml")
    latch.await(10, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set)
  }


  def "PurgeCacheTags with results with purgeUrls"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)
    cloudFlareClient.invalidate(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME, Collections.emptySet()))
    cloudFlareClient.invalidateCacheTags(_ as String, _ as Set) >> Optional.of(new InvalidateCacheResult(200, 'OK', CloudFlareClient.SERVICE_NAME_CACHE_TAG, Collections.emptySet()))

    when:
    purgeService.purgeCache("bma", "somepath/", "file.xml")
    latch.await(10, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set)
  }

  def "PurgeCache no results"() {
    given:
    CountDownLatch latch  = new CountDownLatch(1)
    cloudFlareClient.invalidate(*_) >> { args -> latch.countDown(); return Optional.empty() }

    when:
    purgeService.purgeCache("bma", "somepath", "file.xml")
    latch.await(3, TimeUnit.SECONDS)

    then:
    1 * cloudFlareClient.invalidate(_ as String, _ as Set)
  }

  def "GetRootUrl"() {
    when:
    def rootUrl = purgeService.getRootUrl()

    then:
    expectedRootUrl == rootUrl
  }
  def "GetRootUrlNull"() {
    when:
    purgeService = new CloudFlareDelayedPurgeService(cloudFlareClient, 10, 0, 1,  1000,"zoneId", new String[0])
    def rootUrl = purgeService.getRootUrl()

    then:
    null == rootUrl
  }
}
