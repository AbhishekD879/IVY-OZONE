package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.service.MarketLinkService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class MarketLinksAfterSaveListener extends BasicMongoEventListener<MarketLink> {
  private final MarketLinkService marketLinkService;

  @Autowired
  public MarketLinksAfterSaveListener(
      @Qualifier("publicViewOnlyDelivery") DeliveryNetworkService context,
      MarketLinkService marketLinkService) {
    super(context);
    this.marketLinkService = marketLinkService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<MarketLink> event) {
    MarketLink marketLink = event.getSource();
    String brand = marketLink.getBrand();

    uploadCollection(
        brand, "api/{0}", "market-links", marketLinkService.getMarketLinksByBrand(brand));
  }
}
