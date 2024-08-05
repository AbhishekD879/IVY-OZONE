package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicBannerService;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetPackBannerAfterSaveListener extends BasicMongoEventListener<BetPackBanner> {

  private final BetPackMarketPlacePublicBannerService betPackMarketPlacePublicBannerService;

  private static final String PATH_TEMPLATE = "api/{0}/bet-pack";

  private static final String FILE_NAME = "banner";

  public BetPackBannerAfterSaveListener(
      final DeliveryNetworkService context,
      final BetPackMarketPlacePublicBannerService betPackMarketPlacePublicBannerService) {
    super(context);
    this.betPackMarketPlacePublicBannerService = betPackMarketPlacePublicBannerService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetPackBanner> event) {
    String brand = event.getSource().getBrand();
    List<BetPackBanner> content =
        betPackMarketPlacePublicBannerService.getBetPackBannerByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content.get(0)));
  }
}
