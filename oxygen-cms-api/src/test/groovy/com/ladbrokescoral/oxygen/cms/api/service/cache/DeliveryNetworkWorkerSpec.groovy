package com.ladbrokescoral.oxygen.cms.api.service.cache

import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService
import com.ladbrokescoral.oxygen.cms.api.service.BrandCacheServiceProvider
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
    1 * brandCacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName(), item.getCacheTag())
  }

  def "Upload item no purge"() {
    given:
    UploadItem item  = UploadItem.builder()
        .action(UploadItem.Action.UPLOAD)
        .brand("bma")
        .path("path")
        .fileName("file")
        .cacheTag("cachetag")
        .json("{}")
        .build()

    when:
    worker.deliverItem(item)

    then:
    1 * brandCacheService.uploadJSON(item.getPath(), item.getFileName(), item.getJson()) >> false
    0 * brandCacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName(), item.getCacheTag())
  }

  def "Delete item"() {
    given:
    UploadItem item  = UploadItem.builder()
        .action(UploadItem.Action.DELETE)
        .brand("bma")
        .path("path")
        .fileName("file").cacheTag("cachetag").build()

    when:
    worker.deliverItem(item)

    then:
    1 * brandCacheService.deleteFile(item.getPath()+"/"+ item.getFileName()) >> true
    1 * brandCacheService.purgeCache(item.getBrand(), item.getPath(), item.getFileName(), item.getCacheTag())
  }
}
