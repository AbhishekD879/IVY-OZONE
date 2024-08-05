package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesNewGamingPopUpAfterSaveListener
    extends BasicMongoEventListener<FanzoneNewGamingPopUp> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-new-gaming-pop-up";

  private final FanzonesNewGamingPopUpService service;

  public FanzonesNewGamingPopUpAfterSaveListener(
      final FanzonesNewGamingPopUpService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneNewGamingPopUp> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzone-new-gaming-pop-up storing at s3 bucket{}", brand);
    List<FanzoneNewGamingPopUp> fanzoneNewGamingPopUps = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneNewGamingPopUps);
  }
}
