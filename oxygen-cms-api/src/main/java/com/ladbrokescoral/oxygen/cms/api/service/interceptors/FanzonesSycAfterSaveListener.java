package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesSycAfterSaveListener extends BasicMongoEventListener<FanzoneSyc> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-syc";
  private final FanzonesSycService service;

  public FanzonesSycAfterSaveListener(
      final FanzonesSycService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneSyc> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzone-syc storing at s3 bucket{}", brand);
    List<FanzoneSyc> fanzonesyc = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzonesyc);
  }
}
