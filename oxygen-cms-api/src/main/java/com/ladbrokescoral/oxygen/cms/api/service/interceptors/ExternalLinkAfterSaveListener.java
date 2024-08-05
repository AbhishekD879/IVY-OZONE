package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.ExternalLink;
import com.ladbrokescoral.oxygen.cms.api.service.ExternalLinkService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.ArrayList;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class ExternalLinkAfterSaveListener extends BasicMongoEventListener<ExternalLink> {
  private final ExternalLinkService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "external-link";

  public ExternalLinkAfterSaveListener(
      ExternalLinkService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<ExternalLink> event) {
    String brand = event.getSource().getBrand();
    List<ExternalLink> links = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, new ArrayList(links));
  }
}
