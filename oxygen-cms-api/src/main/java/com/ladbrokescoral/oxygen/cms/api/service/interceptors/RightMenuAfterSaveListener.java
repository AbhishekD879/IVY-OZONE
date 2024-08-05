package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RightMenuPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class RightMenuAfterSaveListener extends BasicInitialDataAfterSaveListener<RightMenu> {

  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String RIGHT_MENU_FILENAME = "right-menu";

  private final RightMenuPublicService rightMenuPublicService;

  public RightMenuAfterSaveListener(
      final RightMenuPublicService rightMenuPublicService,
      InitialDataService initialDataService,
      final DeliveryNetworkService deliveryNetworkService) {
    super(initialDataService, deliveryNetworkService);
    this.rightMenuPublicService = rightMenuPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<RightMenu> event) {
    String brand = event.getSource().getBrand();
    List content = rightMenuPublicService.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, RIGHT_MENU_FILENAME, content);
    super.upload(event);
  }
}
