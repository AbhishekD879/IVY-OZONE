package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicFilterService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetPackFilterAfterSaveListener extends BasicMongoEventListener<BetPackFilter> {

  private final BetPackMarketPlacePublicFilterService betPackMarketPlacePublicFilterService;

  private static final String PATH_TEMPLATE = "api/{0}/bet-pack";

  private static final String FILE_NAME = "filter";

  public BetPackFilterAfterSaveListener(
      final DeliveryNetworkService context,
      final BetPackMarketPlacePublicFilterService betPackMarketPlacePublicFilterService) {
    super(context);
    this.betPackMarketPlacePublicFilterService = betPackMarketPlacePublicFilterService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetPackFilter> event) {
    String brand = event.getSource().getBrand();
    List<BetPackFilter> content =
        betPackMarketPlacePublicFilterService.getActiveBetPackFilterByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
