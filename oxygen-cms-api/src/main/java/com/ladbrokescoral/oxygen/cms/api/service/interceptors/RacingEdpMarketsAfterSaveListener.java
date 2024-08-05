package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RacingEdpMarketPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

/** Class that listens {@link RacingEdpMarket}s mongo events. */
@Component
public class RacingEdpMarketsAfterSaveListener extends BasicMongoEventListener<RacingEdpMarket> {

  private final RacingEdpMarketPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "racing-edp-markets";

  public RacingEdpMarketsAfterSaveListener(
      final RacingEdpMarketPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  /*
   * Method that captures After save event and upload that collection to s3 bucket.
   */
  @Override
  public void onAfterSave(AfterSaveEvent<RacingEdpMarket> event) {
    String brand = event.getSource().getBrand();
    List<RacingEdpMarketDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
