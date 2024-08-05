package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuickLinkPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class QuickLinksAfterSaveListener extends BasicMongoEventListener<QuickLink> {

  private final QuickLinkPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/quick-links";

  public QuickLinksAfterSaveListener(
      final QuickLinkPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<QuickLink> event) {
    String raceType = event.getSource().getRaceType();
    String brand = event.getSource().getBrand();
    List<QuickLinkDto> content = service.findByBrand(brand, raceType);
    uploadCollection(brand, PATH_TEMPLATE, raceType, content);
  }
}
