package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import com.ladbrokescoral.oxygen.cms.api.service.PreferenceCentresService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class PreferenceCentresAfterSaveListener extends BasicMongoEventListener<PreferenceCentre> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-preference-center";
  private final PreferenceCentresService service;

  public PreferenceCentresAfterSaveListener(
      final PreferenceCentresService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PreferenceCentre> event) {
    String brand = event.getSource().getBrand();
    log.info("PreferenceCentres storing at s3 bucket{}", brand);
    List<PreferenceCentre> preferenceCentre = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, preferenceCentre);
  }
}
