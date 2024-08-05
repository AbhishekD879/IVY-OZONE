package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipConfigPublicService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class LuckyDipConfigAfterSaveListener
    extends BasicMongoEventListener<LuckyDipConfiguration> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "luckydip";
  private final LuckyDipConfigPublicService service;

  public LuckyDipConfigAfterSaveListener(
      final LuckyDipConfigPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LuckyDipConfiguration> event) {
    String brand = event.getSource().getBrand();
    List<LuckyDipConfigurationPublicDto> luckyDipConfigs =
        service.getAllLuckyDipConfigByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, luckyDipConfigs);
  }
}
