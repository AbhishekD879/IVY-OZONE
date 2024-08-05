package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.DesktopQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DesktopQuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.DesktopQuickLinkPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class DesktopQuickLinksAfterSaveListener extends BasicMongoEventListener<DesktopQuickLink> {

  private final DesktopQuickLinkPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "desktop-quick-links";

  public DesktopQuickLinksAfterSaveListener(
      final DesktopQuickLinkPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<DesktopQuickLink> event) {
    String brand = event.getSource().getBrand();
    List<DesktopQuickLinkDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
