package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicLabelService;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetPackLabelAfterSaveListener extends BasicMongoEventListener<BetPackLabel> {

  private final BetPackMarketPlacePublicLabelService betPackMarketPlacePublicLabelService;

  private static final String PATH_TEMPLATE = "api/{0}/bet-pack";

  private static final String FILE_NAME = "label";

  public BetPackLabelAfterSaveListener(
      final DeliveryNetworkService context,
      final BetPackMarketPlacePublicLabelService betPackMarketPlacePublicLabelService) {
    super(context);
    this.betPackMarketPlacePublicLabelService = betPackMarketPlacePublicLabelService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetPackLabel> event) {
    String brand = event.getSource().getBrand();
    List<BetPackLabel> content = betPackMarketPlacePublicLabelService.getBetPackLabelByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content.get(0)));
  }
}
