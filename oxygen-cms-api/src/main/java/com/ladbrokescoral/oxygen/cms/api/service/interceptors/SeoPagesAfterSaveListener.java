package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeoPagePublicService;
import java.util.Map;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SeoPagesAfterSaveListener extends BasicMongoEventListener<SeoPage> {
  private final SeoPagePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "seo-pages";

  public SeoPagesAfterSaveListener(
      final SeoPagePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SeoPage> event) {
    String eventBrand = event.getSource().getBrand();
    Map<String, String> content = service.find(eventBrand);
    uploadMap(eventBrand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
