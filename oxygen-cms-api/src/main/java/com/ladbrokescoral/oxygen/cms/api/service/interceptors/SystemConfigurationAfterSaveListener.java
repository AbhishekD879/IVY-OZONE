package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StructurePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Map;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.bson.Document;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SystemConfigurationAfterSaveListener
    extends BasicInitialDataAfterSaveListener<SystemConfiguration> {
  private final StructurePublicService structureService;
  private static final String ALL_CONFIGS_PATH_TEMPLATE = "api/{0}";
  private static final String ALL_CONFIGS_FILE_NAME = "system-configuration";
  private static final String SINGLE_CONFIG_PATH_TEMPLATE = "api/{0}/system-configurations";
  private static final String COLLECTION_NAME = "systemconfigurations";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-systemconfigurations}")
  private String ladsSystemconfigurationsTopic;

  @Value(value = "${coral.kafka.topic.cms-systemconfigurations}")
  private String coralSystemconfigurationsTopic;

  public SystemConfigurationAfterSaveListener(
      final StructurePublicService structureService,
      InitialDataService initialDataService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(initialDataService, context);
    this.structureService = structureService;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SystemConfiguration> event) {
    String brand = event.getSource().getBrand();
    String configName = event.getSource().getName();
    Optional<Map<String, Map<String, Object>>> brandStructure = structureService.find(brand);
    uploadOptional(brand, ALL_CONFIGS_PATH_TEMPLATE, ALL_CONFIGS_FILE_NAME, brandStructure);
    brandStructure.ifPresent(
        prop ->
            uploadOptional(
                brand,
                SINGLE_CONFIG_PATH_TEMPLATE,
                configName,
                Optional.ofNullable(prop.get(configName))));
    super.upload(event);
    // cms-push mechanism implementation
    String topic =
        brand.equalsIgnoreCase(Brand.BMA)
            ? coralSystemconfigurationsTopic
            : ladsSystemconfigurationsTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }

  @Override
  public void onAfterDelete(
      AfterDeleteEvent<SystemConfiguration> deleteEvent,
      AfterSaveEvent<SystemConfiguration> sourceEvent) {
    Document deletedItem = deleteEvent.getSource();
    SystemConfiguration systemConfig = sourceEvent.getSource();
    String deletedItemId = (String) deletedItem.get("id");
    if (systemConfig.getId().equals(deletedItemId)) {
      delete(systemConfig.getBrand(), SINGLE_CONFIG_PATH_TEMPLATE, systemConfig.getName());
      super.onAfterDelete(deleteEvent, sourceEvent);
    }
  }
}
