package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class TrendingBetAfterSaveListener extends BasicMongoEventListener<TrendingBet> {
  private final TrendingBetService trendingBetService;

  private static final String PATH_TEMPLATE = "api/{0}";

  private static final String FILE_NAME = "trending-bet";

  public TrendingBetAfterSaveListener(
      DeliveryNetworkService context, TrendingBetService trendingBetService) {
    super(context);
    this.trendingBetService = trendingBetService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<TrendingBet> event) {
    String brand = event.getSource().getBrand();
    String type = event.getSource().getType();
    Optional<TrendingBet> content = trendingBetService.getTrendingBetsByBrand(brand, type);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME + "/" + type, content);
  }
}
