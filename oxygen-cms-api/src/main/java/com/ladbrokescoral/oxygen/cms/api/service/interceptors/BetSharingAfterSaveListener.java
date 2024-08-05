package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.service.BetSharingService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetSharingAfterSaveListener extends BasicMongoEventListener<BetSharingEntity> {
  private final BetSharingService betSharingService;

  private static final String PATH_TEMPLATE = "api/{0}";

  private static final String FILE_NAME = "bet-sharing";

  public BetSharingAfterSaveListener(
      DeliveryNetworkService context, BetSharingService betSharingService) {
    super(context);
    this.betSharingService = betSharingService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetSharingEntity> event) {
    String brand = event.getSource().getBrand();
    Optional<BetSharingEntity> content = betSharingService.getBetSharingByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
