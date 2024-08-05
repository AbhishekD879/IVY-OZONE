package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesNewSeasonAfterSaveListener extends BasicMongoEventListener<FanzoneNewSeason> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-new-season";
  private final FanzonesNewSeasonService service;

  public FanzonesNewSeasonAfterSaveListener(
      final FanzonesNewSeasonService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneNewSeason> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzone-new-season storing at s3 bucket{}", brand);
    List<FanzoneNewSeason> fanzoneNewSeasons = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneNewSeasons);
  }
}
