package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.AssetManagementService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class AssetManagementAfterSaveListener extends BasicMongoEventListener<AssetManagement> {

  private final AssetManagementService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String CF_PATH_TEMPLATE = "api/{0}/cf";
  private static final String FILE_NAME = "asset-management";
  private static final String COLLECTION_NAME = "assetmanagement";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-assetmanagement}")
  private String ladsAssetmanagementTopic;

  @Value(value = "${coral.kafka.topic.cms-assetmanagement}")
  private String coralAssetmanagementTopic;

  public AssetManagementAfterSaveListener(
      AssetManagementService service,
      DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<AssetManagement> event) {
    String brand = event.getSource().getBrand();
    List<AssetManagement> items = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, items);
    uploadCFContent(brand, CF_PATH_TEMPLATE, FILE_NAME, Optional.of(items));
    String topic =
        brand.equalsIgnoreCase(Brand.BMA) ? coralAssetmanagementTopic : ladsAssetmanagementTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
