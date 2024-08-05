package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BybLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybLeaguePublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BybLeagueAfterSaveListener extends BasicMongoEventListener<BybLeague> {
  private final BybLeaguePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "byb-leagues";

  public BybLeagueAfterSaveListener(
      final BybLeaguePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BybLeague> bybLeagueDto) {
    String brand = bybLeagueDto.getSource().getBrand();
    List<BybLeagueDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
