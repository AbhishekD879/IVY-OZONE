package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.InitSignpostingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.InitSignpostingPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class InitSignpostingAfterSaveListener extends BasicMongoEventListener<Promotion> {

  private final InitSignpostingPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "init-signposting";

  public InitSignpostingAfterSaveListener(
      final InitSignpostingPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Promotion> event) {
    String brand = event.getSource().getBrand();
    List<InitSignpostingDto> content = service.find(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
