package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StreamAndBetPublicService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class StreamAndBetAfterSaveListener extends BasicMongoEventListener<StreamAndBet> {

  private final StreamAndBetPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "stream-and-bet";

  public StreamAndBetAfterSaveListener(
      StreamAndBetPublicService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<StreamAndBet> event) {
    String brand = event.getSource().getBrand();
    service
        .findByBrand(brand)
        .ifPresent(value -> uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, value));
  }
}
