package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OfferModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OfferPublicService;
import java.util.Arrays;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class OfferModuleAfterSaveListener extends BasicMongoEventListener<OfferModule> {

  private final OfferPublicService service;
  private static final String PATH_TEMPLATE = "api/v2/{0}/offers";

  public OfferModuleAfterSaveListener(
      final OfferPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<OfferModule> event) {
    List<String> deviceTypeList =
        event.getSource().getShowModuleOn().equals("both")
            ? Arrays.asList("tablet", "desktop")
            : Arrays.asList(event.getSource().getShowModuleOn());

    for (String deviceType : deviceTypeList) {
      String brand = event.getSource().getBrand();
      List<OfferModuleDto> content = getContent(brand, deviceType);
      uploadCollection(brand, PATH_TEMPLATE, deviceType, content);
    }
  }

  private List<OfferModuleDto> getContent(String brand, String deviceType) {
    return service.findByBrand(brand, deviceType);
  }
}
