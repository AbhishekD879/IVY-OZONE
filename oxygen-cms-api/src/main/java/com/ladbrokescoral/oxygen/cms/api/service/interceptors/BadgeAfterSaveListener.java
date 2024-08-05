package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BadgeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Badge;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BadgePublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BadgeAfterSaveListener extends BasicMongoEventListener<Badge> {
  private final BadgePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "badge";

  public BadgeAfterSaveListener(
      final BadgePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Badge> event) {
    String brand = event.getSource().getBrand();
    List<BadgeDto> content = service.findAllByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
