package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.LottoBannerConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class LottoConfigAfterSaveListener extends BasicMongoEventListener<LottoConfig> {

  private final LottoConfigService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "lotto-configs";

  public LottoConfigAfterSaveListener(
      final LottoConfigService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LottoConfig> event) {
    String brand = event.getSource().getBrand();
    Optional<LottoBannerConfigDTO> content = service.readByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
