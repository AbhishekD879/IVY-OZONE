package com.coral.oxygen.middleware.common.cache

import com.coral.oxygen.middleware.common.configuration.cfcache.BrandCacheService
import com.coral.oxygen.middleware.common.configuration.cfcache.BrandCacheServiceProvider
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkWorker
import com.coral.oxygen.middleware.pojos.model.cache.UploadItem
import spock.lang.Specification

class DeliveryNetworkWorkerSpec extends Specification {

  private DeliveryNetworkWorker worker
  private BrandCacheServiceProvider brandCacheServiceProvider
  private BrandCacheService brandCacheService

  void setup() {
    brandCacheService = Mock()
    brandCacheServiceProvider = Mock()
    worker = new DeliveryNetworkWorker(brandCacheServiceProvider)

    brandCacheServiceProvider.getCacheService(_ as String) >> [brandCacheService]
  }

  def "Upload item with purge"() {
    given:
    UploadItem item  = UploadItem.builder()
        .action(UploadItem.Action.UPLOAD)
        .brand("bma")
        .path("path")
        .fileName("file").cacheTag("cachetag").build()

    when:
    worker.deliverItem(item)

    then:
    1 * brandCacheService.uploadJSON(item.getPath(), item.getFileName(), item.getJson()) >> true
    1 * brandCacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName())
  }

  def "Upload item no purge"() {
    given:
    UploadItem item  = UploadItem.builder()
        .action(UploadItem.Action.UPLOAD)
        .brand("bma")
        .path("path/")
        .fileName("file")
        .cacheTag("cachetag")
        .json("{}")
        .build()

    when:
    worker.deliverItem(item)

    then:
    1 * brandCacheService.uploadJSON(item.getPath(), item.getFileName(), item.getJson()) >> false
    0 * brandCacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName())
  }


  def "Upload null item for no purge"() {
    given:
    UploadItem item  =null;

    when:
    worker.deliverItem(item)

    then:
    0 * brandCacheService.purgeCache(_)
  }

  def "Upload item null  no purge"() {
    given:
    UploadItem item  = UploadItem.builder()
        .action(UploadItem.Action.UPLOAD)
        .brand("bma")
        .path("path")
        .fileName("file")
        .cacheTag("cachetag")
        .json("{}")
        .build()
    brandCacheServiceProvider.getCacheService("bma")>> {throw new Exception ("Failed")}

    when:
    worker.deliverItem(item);

    then:
    1 * brandCacheServiceProvider.getCacheService("bma")
  }
}
