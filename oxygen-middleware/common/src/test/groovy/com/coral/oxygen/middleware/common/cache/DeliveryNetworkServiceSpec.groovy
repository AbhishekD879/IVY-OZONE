package com.coral.oxygen.middleware.common.cache

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkExecutor
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkServiceImpl
import com.coral.oxygen.middleware.pojos.model.cache.UploadItem
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.ObjectWriter
import spock.lang.Specification

class DeliveryNetworkServiceSpec extends Specification {
  private DeliveryNetworkService deliveryNetworkService
  private DeliveryNetworkExecutor deliveryNetworkExecutor
  private ObjectMapper objectMapper
  private ObjectWriter objectWriter;
  void setup() {
    deliveryNetworkExecutor = Mock()
    objectMapper = new ObjectMapper()
    objectWriter=objectMapper.writer();
    deliveryNetworkService = new DeliveryNetworkServiceImpl(deliveryNetworkExecutor, objectWriter)
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
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
    expectedItem != null
    expectedItem.getAction() == UploadItem.Action.UPLOAD
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
    deliveryNetworkExecutor.addItem(_ as UploadItem) >> {throw new Exception ("Failed")}
    when:
    deliveryNetworkService.upload(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
  }
  def "Upload For InterruptedException"() {
    UploadItem expectedItem
    given:
    def brand = "bma"
    def path = "wer_path_trty"
    def fileName = "file"
    deliveryNetworkExecutor.addItem(_ as UploadItem) >> {throw new InterruptedException ("Failed")}
    when:
    deliveryNetworkService.upload(brand, path, fileName, Collections.singletonMap("key", "val"))

    then:
    1 * deliveryNetworkExecutor.addItem(_) >> {arguments -> expectedItem = arguments[0] as  UploadItem}
  }
}
