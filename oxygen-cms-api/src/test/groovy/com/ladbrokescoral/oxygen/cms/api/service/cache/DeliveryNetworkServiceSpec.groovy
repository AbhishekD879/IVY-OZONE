package com.ladbrokescoral.oxygen.cms.api.service.cache

import com.fasterxml.jackson.databind.ObjectMapper
import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem
import com.ladbrokescoral.oxygen.cms.configuration.CFCacheTagProperties
import spock.lang.Specification

import static com.ladbrokescoral.oxygen.cms.api.entity.UploadItem.Action.UPLOAD
import static com.ladbrokescoral.oxygen.cms.api.entity.UploadItem.Action.DELETE

class DeliveryNetworkServiceSpec extends Specification {
  private DeliveryNetworkService deliveryNetworkService
  private DeliveryNetworkExecutor deliveryNetworkExecutor
  private ObjectMapper objectMapper
  private CFCacheTagProperties cfCacheTagProperties;

  void setup() {
    deliveryNetworkExecutor = Mock()
    objectMapper = new ObjectMapper()
    cfCacheTagProperties = Mock()
    deliveryNetworkService = new DeliveryNetworkServiceImpl(deliveryNetworkExecutor, objectMapper, cfCacheTagProperties)
  }

  def "Upload"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"

    when:
    deliveryNetworkService.upload(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    3 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == UPLOAD
    expectedItem.getBrand() == brand
    expectedItem.getPath().endsWith(path)
    expectedItem.getFileName() == fileName
  }

  def "Upload For Exception"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"
    deliveryNetworkExecutor.addItem(_) >> {throw new Exception ("Failed")}
    when:
    deliveryNetworkService.upload(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    3 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
  }

  def "UploadCFContent"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"
    def cacheMap = new HashMap<String, String>()
    cacheMap.put("bma", "CSP-tst0-coral")
    cfCacheTagProperties.getTags() >> cacheMap

    when:
    deliveryNetworkService.uploadCFContent(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == UPLOAD
    expectedItem.getBrand() == brand
    expectedItem.getPath().endsWith(path)
    expectedItem.getFileName() == fileName
  }

  def "UploadCFContentForException"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"
    def cacheMap = new HashMap<String, String>()
    cacheMap.put("bma", "CSP-tst0-coral")
    cfCacheTagProperties.getTags() >> cacheMap

    deliveryNetworkExecutor.addItem(_) >> {new Exception("failed...")}

    when:
    deliveryNetworkService.uploadCFContent(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == UPLOAD
    expectedItem.getBrand() == brand
    expectedItem.getPath().endsWith(path)
    expectedItem.getFileName() == fileName
  }

  def "UploadCFContentForInterruptedException"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"
    def cacheMap = new HashMap<String, String>()
    cacheMap.put("bma", "CSP-tst0-coral")
    cfCacheTagProperties.getTags() >> cacheMap

    deliveryNetworkExecutor.addItem(_) >> {new InterruptedException("failed...")}

    when:
    deliveryNetworkService.uploadCFContent(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == UPLOAD
    expectedItem.getBrand() == brand
    expectedItem.getPath().endsWith(path)
    expectedItem.getFileName() == fileName
  }

  def "Delete"() {
    UploadItem expectedItem

    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"

    when:
    deliveryNetworkService.delete(brand, path, fileName)

    then:
    3 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == DELETE
    expectedItem.getBrand() == brand
    expectedItem.getPath().endsWith(path)
    expectedItem.getFileName() == fileName
  }
}
