package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import com.ladbrokescoral.oxygen.cms.api.service.MyStableService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class MyStableAfterSaveListener extends BasicMongoEventListener<MyStable> {

  private final MyStableService myStableService;
  private static final String PATH_TEMPLATE = "api/{0}/my-stable";
  private static final String FILE_NAME = "configuration";

  public MyStableAfterSaveListener(
      DeliveryNetworkService context, MyStableService myStableService) {
    super(context);
    this.myStableService = myStableService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<MyStable> event) {
    String brand = event.getSource().getBrand();
    List<MyStable> myStable = myStableService.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, myStable);
  }
}
