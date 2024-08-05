package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipV2ConfigPublicProcessor;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class LuckyDipV2ConfigAfterSaveListener extends BasicMongoEventListener<LuckyDipV2Config> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "lucky-dip";
  private final LuckyDipV2ConfigPublicProcessor luckyDipV2ConfigPublicProcessor;

  public LuckyDipV2ConfigAfterSaveListener(
      final DeliveryNetworkService context,
      LuckyDipV2ConfigPublicProcessor luckyDipV2ConfigPublicProcessor) {
    super(context);
    this.luckyDipV2ConfigPublicProcessor = luckyDipV2ConfigPublicProcessor;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LuckyDipV2Config> event) {
    String brand = event.getSource().getBrand();
    List<LuckyDipV2ConfigurationPublicDto> luckyDipConfigs =
        luckyDipV2ConfigPublicProcessor.getAllActiveLDByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, luckyDipConfigs);
  }
}
