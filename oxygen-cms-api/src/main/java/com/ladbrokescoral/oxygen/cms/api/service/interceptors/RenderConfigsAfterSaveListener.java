package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.RenderConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RenderConfig;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RenderConfigPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class RenderConfigsAfterSaveListener extends BasicMongoEventListener<RenderConfig> {

  private final RenderConfigPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "render-config";

  public RenderConfigsAfterSaveListener(
      RenderConfigPublicService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<RenderConfig> event) {
    String brand = event.getSource().getBrand();
    List<RenderConfigDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
