package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.service.RGYConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class RGYGlobalSwitchAfterSaveListener extends BasicMongoEventListener<RGYMetaInfoEntity> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "rgy-config";
  private RGYConfigService rgyConfigService;

  protected RGYGlobalSwitchAfterSaveListener(
      DeliveryNetworkService context, RGYConfigService rgyConfigService) {
    super(context);
    this.rgyConfigService = rgyConfigService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<RGYMetaInfoEntity> rgyMetaInfoEntity) {
    String brand = rgyMetaInfoEntity.getSource().getBrand();
    boolean isRgyEnabled = rgyMetaInfoEntity.getSource().isRgyEnabled();
    String message = isRgyEnabled ? "Enabled" : "Disabled";
    log.info("RGY Bonus Suppression is {} for brand {}", message, brand);
    List<RGYConfigurationEntity> rgyConfigs = Collections.emptyList();
    if (isRgyEnabled) {
      rgyConfigs = rgyConfigService.readByBrandAndBonusSuppressionTrue(brand);
    }
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, rgyConfigs);
  }
}
