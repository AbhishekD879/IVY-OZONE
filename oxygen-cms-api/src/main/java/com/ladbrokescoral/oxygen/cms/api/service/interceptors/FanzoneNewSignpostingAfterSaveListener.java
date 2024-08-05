package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FanzoneNewSignpostingAfterSaveListener
    extends BasicMongoEventListener<FanzoneNewSignposting> {

  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-new-signposting";
  private final FanzonesNewSignpostingService fanzonesNewSignpostingService;

  public FanzoneNewSignpostingAfterSaveListener(
      final FanzonesNewSignpostingService fanzonesNewSignpostingService,
      final DeliveryNetworkService context) {
    super(context);
    this.fanzonesNewSignpostingService = fanzonesNewSignpostingService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneNewSignposting> event) {
    String brand = event.getSource().getBrand();
    List<FanzoneNewSignposting> fanzoneNewSignpostings =
        fanzonesNewSignpostingService.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneNewSignpostings);
  }
}
