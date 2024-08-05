package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesComingBackAfterSaveListener
    extends BasicMongoEventListener<FanzoneComingBack> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-coming-back";
  private final FanzonesComingBackService service;

  public FanzonesComingBackAfterSaveListener(
      final FanzonesComingBackService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneComingBack> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzone-coming-back storing at s3 bucket{}", brand);
    List<FanzoneComingBack> fanzoneComingBacks = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneComingBacks);
  }
}
