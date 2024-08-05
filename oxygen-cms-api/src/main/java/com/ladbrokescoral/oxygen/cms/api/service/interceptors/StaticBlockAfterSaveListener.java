package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticBlockPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class StaticBlockAfterSaveListener extends BasicMongoEventListener<StaticBlock> {

  private final StaticBlockPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/static-block";

  public StaticBlockAfterSaveListener(
      final StaticBlockPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<StaticBlock> event) {
    String uri = event.getSource().getUri();
    String brand = event.getSource().getBrand();
    Optional<StaticBlockDto> content = service.find(brand, uri);
    if (content.isPresent()) {
      uploadOptional(brand, PATH_TEMPLATE, uri, content);
    } else {
      uploadOptional(brand, PATH_TEMPLATE, uri, Optional.of(new StaticBlockDto()));
    }
  }
}
