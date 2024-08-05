package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.EdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.EdpMarketPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class EdpMarketsAfterSaveListener extends BasicMongoEventListener<EdpMarket> {
  private final EdpMarketPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "edp-markets";

  public EdpMarketsAfterSaveListener(
      final EdpMarketPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<EdpMarket> event) {
    String brand = event.getSource().getBrand();
    List<EdpMarketDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
