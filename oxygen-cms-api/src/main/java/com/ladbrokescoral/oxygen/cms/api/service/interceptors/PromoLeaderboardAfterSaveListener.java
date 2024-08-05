package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavItemPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromoLeaderboardPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class PromoLeaderboardAfterSaveListener
    extends BasicMongoEventListener<PromoLeaderboardConfig> {

  private final PromoLeaderboardPublicService promoLeaderboardPublicService;
  private final NavItemPublicService navItemPublicService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "promo-leaderboard";

  private static final String NAV_FILENAME = "navigation-group";

  public PromoLeaderboardAfterSaveListener(
      final DeliveryNetworkService context,
      PromoLeaderboardPublicService promoLeaderboardPublicService,
      NavItemPublicService navItemPublicService) {
    super(context);
    this.promoLeaderboardPublicService = promoLeaderboardPublicService;
    this.navItemPublicService = navItemPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PromoLeaderboardConfig> event) {
    String brand = event.getSource().getBrand();
    List<PromoLeaderboardConfigPublicDto> promoLeaderboardList =
        promoLeaderboardPublicService.findLeaderboardByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILENAME, promoLeaderboardList);

    /*
      Pushing change in Nav Item collection on update in leaderboard Config,
      as Leaderboard is linked to Nav Item
    */
    List<NavigationGroupPublicDto> navigationGroupPublicDtoList =
        navItemPublicService.getNavigationGroupByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, NAV_FILENAME, navigationGroupPublicDtoList);
  }
}
