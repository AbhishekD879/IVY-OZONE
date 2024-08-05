package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BybMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybMarketPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BybMarketAfterSaveListener extends BasicMongoEventListener<BybMarket> {

  private final BybMarketPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "byb-markets";

  public BybMarketAfterSaveListener(
      final BybMarketPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BybMarket> bybLeagueDto) {
    String brand = bybLeagueDto.getSource().getBrand();
    List<BybMarketDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
