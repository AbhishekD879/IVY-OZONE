package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterLogoPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FooterLogosNativeAfterSaveListener extends BasicMongoEventListener<FooterLogo> {

  private final FooterLogoPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "footer-logos-native";

  public FooterLogosNativeAfterSaveListener(
      final FooterLogoPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FooterLogo> event) {
    String brand = event.getSource().getBrand();
    List<FooterLogoNativeDto> content = service.findNative(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
