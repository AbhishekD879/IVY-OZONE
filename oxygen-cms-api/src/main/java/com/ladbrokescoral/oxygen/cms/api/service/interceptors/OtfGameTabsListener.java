package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfGameTabsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfGameTabPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class OtfGameTabsListener extends BasicMongoEventListener<OtfGameTabs> {
  private final OtfGameTabPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "otf-tab-config";

  public OtfGameTabsListener(
      final OtfGameTabPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<OtfGameTabs> event) {
    String brand = event.getSource().getBrand();
    List<OtfGameTabsDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
