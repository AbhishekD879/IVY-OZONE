package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideCampaign;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideCampaignPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FreeRideCampaignAfterSaveListener extends BasicMongoEventListener<FreeRideCampaign> {
  private final FreeRideCampaignPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "freeride-campaign";

  public FreeRideCampaignAfterSaveListener(
      final FreeRideCampaignPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FreeRideCampaign> event) {
    String brand = event.getSource().getBrand();
    List<FreeRidePublicCampaignDto> campaignList = service.getAllCampaignByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILENAME, campaignList);
  }
}
