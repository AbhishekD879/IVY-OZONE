package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import com.ladbrokescoral.oxygen.cms.api.service.GameMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class GameMenuAfterSaveListener extends BasicMongoEventListener<GameMenu> {
  private final GameMenuService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "game-menu";

  public GameMenuAfterSaveListener(GameMenuService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<GameMenu> event) {
    String brand = event.getSource().getBrand();
    List<GameMenu> links = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, new ArrayList(links));
  }
}
