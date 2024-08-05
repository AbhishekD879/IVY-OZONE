package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneClub;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesClubAfterSaveListener extends BasicMongoEventListener<FanzoneClub> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-club";
  private final FanzonesClubService service;

  public FanzonesClubAfterSaveListener(
      final FanzonesClubService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneClub> event) {
    String brand = event.getSource().getBrand();
    log.info("FanzonesClub storing at s3 bucket{}", brand);
    List<FanzoneClub> fanzoneClub = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneClub);
  }
}
