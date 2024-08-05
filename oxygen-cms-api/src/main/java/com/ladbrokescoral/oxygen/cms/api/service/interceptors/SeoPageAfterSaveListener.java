package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoPagePublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SeoPageAfterSaveListener extends BasicMongoEventListener<SeoPage> {
  private final SeoPagePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/seo-page";

  public SeoPageAfterSaveListener(
      final SeoPagePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SeoPage> event) {
    String seoPageId = event.getSource().getId();
    String brand = event.getSource().getBrand();
    Optional<SeoPageDto> updatedSeoPage = service.find(brand, seoPageId);
    uploadOptional(brand, PATH_TEMPLATE, seoPageId, updatedSeoPage);
  }
}
