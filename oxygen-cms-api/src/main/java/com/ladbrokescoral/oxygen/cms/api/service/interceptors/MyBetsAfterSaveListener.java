package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MyBet;
import com.ladbrokescoral.oxygen.cms.api.service.MyBetsService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class MyBetsAfterSaveListener extends BasicMongoEventListener<MyBet> {
  private final MyBetsService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "my-bets";

  public MyBetsAfterSaveListener(
      final DeliveryNetworkService context, final MyBetsService service) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<MyBet> event) {
    String brand = event.getSource().getBrand();
    List<MyBet> myBet = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, myBet);
  }
}
