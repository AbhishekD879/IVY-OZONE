package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticTextOtfDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticTextOtfPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class StaticTextOtfAfterSaveListener extends BasicMongoEventListener<StaticTextOtf> {

  private final StaticTextOtfPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "static-texts";

  public StaticTextOtfAfterSaveListener(
      final StaticTextOtfPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<StaticTextOtf> event) {
    String brand = event.getSource().getBrand();
    List<StaticTextOtfDto> content = service.findEnabledByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
