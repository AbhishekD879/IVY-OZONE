package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.YcStaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.YourCallStaticBlockPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class YcStaticBlockAfterSaveListener extends BasicMongoEventListener<YourCallStaticBlock> {
  private final YourCallStaticBlockPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "yc-static-block";
  private static final String FIVE_A_FILE_NAME = "5a-side-static-block";

  public YcStaticBlockAfterSaveListener(
      YourCallStaticBlockPublicService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<YourCallStaticBlock> event) {
    String brand = event.getSource().getBrand();
    List<YcStaticBlockDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);

    List<YcStaticBlockDto> content5A = service.findByBrandAnd5A(brand);
    uploadCollection(brand, PATH_TEMPLATE, FIVE_A_FILE_NAME, content5A);
  }
}
