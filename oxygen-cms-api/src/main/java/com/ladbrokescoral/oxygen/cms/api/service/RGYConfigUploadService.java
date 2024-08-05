package com.ladbrokescoral.oxygen.cms.api.service;

import static java.text.MessageFormat.format;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
@Slf4j
public class RGYConfigUploadService {

  private RGYConfigService rgyConfigService;
  private DeliveryNetworkService deliveryNetworkService;

  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String RGY_CONFIG_BMA_FILE_NAME = "rgy-config";

  public RGYConfigUploadService(
      RGYConfigService rgyConfigService, DeliveryNetworkService deliveryNetworkService) {
    this.rgyConfigService = rgyConfigService;
    this.deliveryNetworkService = deliveryNetworkService;
  }

  public List<RGYConfigurationEntity> uploadToS3(String brand) {
    List<RGYConfigurationEntity> rgYellowConfig =
        rgyConfigService.readByBrandAndBonusSuppressionTrue(brand);
    if (!CollectionUtils.isEmpty(rgYellowConfig)) {
      deliveryNetworkService.upload(
          brand, format(PATH_TEMPLATE, brand), RGY_CONFIG_BMA_FILE_NAME, rgYellowConfig);
    } else {
      deliveryNetworkService.upload(
          brand, format(PATH_TEMPLATE, brand), RGY_CONFIG_BMA_FILE_NAME, Collections.emptyList());
      log.error("RGY configuration is not available for {}", brand);
    }
    log.info("RGY configuration updated for the brand {} and uploaded to S3 bucket", brand);
    return rgYellowConfig;
  }
}
