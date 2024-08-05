package com.ladbrokescoral.oxygen.cms.api.service.interceptors

import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher
import org.springframework.kafka.core.KafkaTemplate

import java.util.concurrent.ExecutorService

import org.bson.Document
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataCFDto
import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StructurePublicService
import com.ladbrokescoral.oxygen.cms.util.CustomExecutors

import spock.lang.Specification

class SystemConfigurationAfterSaveListenerSpec extends Specification {

  private SystemConfigurationAfterSaveListener listener;
  private StructurePublicService structurePublicService;
  private InitialDataService initialDataService;
  private DeliveryNetworkService deliveryNetworkContext;
  private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;


  void setup() {
    structurePublicService = Mock()
    initialDataService = Mock()
    initialDataService.fetchInitialData(*_) >> new InitialDataDto()
    initialDataService.fetchCFInitialData(*_) >> new InitialDataCFDto()
    deliveryNetworkContext = Mock()
    ladsCoralKafkaPublisher=Mock()

    listener = new SystemConfigurationAfterSaveListener(structurePublicService, initialDataService, deliveryNetworkContext,ladsCoralKafkaPublisher)

    structurePublicService.find(_ as String) >> Optional.empty()

    // executor stubing

    CustomExecutors customExecutors = Mock()
    ExecutorService executorService = Mock()

    customExecutors.getSingleThreadLastTaskExecutor(_ as String) >> executorService
    executorService.execute(_) >> {it[0].run()}

    listener.customExecutors = customExecutors
  }

  def "OnAfterSave"() {

    given:

    SystemConfiguration configuration = createSystemConfig("bma_brand", "conf1")
    AfterSaveEvent<SystemConfiguration> afterSaveEvent = new AfterSaveEvent<>(configuration, toDocument(configuration), "systemconfigurations")

    def allBrandConfigs = Collections.singletonMap(configuration.getName(), Collections.emptyMap())

    when:
    listener.onAfterSave(afterSaveEvent)

    then:
    1 * structurePublicService.find(configuration.getBrand()) >> Optional.of(allBrandConfigs)
    1 * deliveryNetworkContext.upload('bma_brand', 'api/bma_brand/system-configurations', 'conf1', [:])
    1 * deliveryNetworkContext.upload('bma_brand', 'api/bma_brand', 'system-configuration', allBrandConfigs);
    3 * deliveryNetworkContext.upload(
        'bma_brand',
        'api/bma_brand/initial-data',
        {
          [
            'mobile',
            'desktop',
            'tablet'
          ].contains(it)},
        _ as InitialDataDto)
    1 * deliveryNetworkContext._
  }


  def "OnAfterSaveBrand"() {

    given:

    SystemConfiguration configuration = createSystemConfig("bma", "conf1")
    AfterSaveEvent<SystemConfiguration> afterSaveEvent = new AfterSaveEvent<>(configuration, toDocument(configuration), "systemconfigurations")

    def allBrandConfigs = Collections.singletonMap(configuration.getName(), Collections.emptyMap())

    when:
    listener.onAfterSave(afterSaveEvent)

    then:
    1 * structurePublicService.find(configuration.getBrand()) >> Optional.of(allBrandConfigs)
    1 * deliveryNetworkContext.upload('bma', 'api/bma/system-configurations', 'conf1', [:])
    1 * deliveryNetworkContext.upload('bma', 'api/bma', 'system-configuration', allBrandConfigs);
    3 * deliveryNetworkContext.upload(
        'bma',
        'api/bma/initial-data',
        {
          [
            'mobile',
            'desktop',
            'tablet'
          ].contains(it)},
        _ as InitialDataDto)
    1 * deliveryNetworkContext._


  }


  def "OnAfterDelete"() {
    given:
    SystemConfiguration configuration = createSystemConfig("bma_brand", "conf1")
    AfterSaveEvent<SystemConfiguration> afterSaveEvent = new AfterSaveEvent<>(configuration, toDocument(configuration), "systemconfigurations")
    AfterDeleteEvent<SystemConfiguration> afterDeleteEvent = new AfterDeleteEvent<>(new Document("id", configuration.getId()), SystemConfiguration.class, "systemconfigurations")

    def allBrandConfigs = Collections.singletonMap(configuration.getName(), Collections.emptyMap())

    when:
    listener.onAfterDelete(afterDeleteEvent, afterSaveEvent)

    then:
    1 * structurePublicService.find(configuration.getBrand()) >> Optional.of(allBrandConfigs)
    1 * deliveryNetworkContext.upload('bma_brand', 'api/bma_brand', 'system-configuration', ['conf1':[:]])
    1 * deliveryNetworkContext.upload('bma_brand', 'api/bma_brand/system-configurations', 'conf1', [:])
    1 * deliveryNetworkContext.delete('bma_brand', "api/bma_brand/system-configurations", "conf1");
    3 * deliveryNetworkContext.upload(
        'bma_brand',
        'api/bma_brand/initial-data',
        {
          [
            'mobile',
            'desktop',
            'tablet'
          ].contains(it)},
        _ as InitialDataDto)
    1 * deliveryNetworkContext._
  }

  SystemConfiguration createSystemConfig(String brand, String name) {
    SystemConfiguration configuration = new SystemConfiguration()
    configuration.setId("id")
    configuration.setBrand(brand)
    configuration.setName(name)
    configuration.setProperties(Collections.emptyList())
    configuration
  }

  Document toDocument(SystemConfiguration config) {
    new Document("id", config.getId())
        .append("brand", config.getBrand())
        .append("name", config.getName())
        .append("initialDataConfig", config.isInitialDataConfig())
        .append("properties", config.getProperties())
  }
}
