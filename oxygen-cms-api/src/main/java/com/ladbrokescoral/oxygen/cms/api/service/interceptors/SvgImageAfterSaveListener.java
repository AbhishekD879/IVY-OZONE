package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SvgSpriteDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SvgImagePublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SvgImageAfterSaveListener extends BasicInitialDataAfterSaveListener<SvgImage> {

  private final SvgImagePublicService svgImagePublicService;
  private static final String PATH_TEMPLATE = "api/{0}/svg-images/sprite";

  public SvgImageAfterSaveListener(
      SvgImagePublicService svgImagePublicService,
      InitialDataService initialDataService,
      DeliveryNetworkService deliveryService) {
    super(initialDataService, deliveryService);
    this.svgImagePublicService = svgImagePublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SvgImage> event) {
    SvgImage svg = event.getSource();
    for (SvgSprite spriteOption : SvgSprite.values()) {
      SvgSpriteDto sprite =
          svgImagePublicService.getSvgSprite(svg.getBrand(), spriteOption.getSpriteName());
      uploadOptional(svg.getBrand(), PATH_TEMPLATE, sprite.getName(), Optional.of(sprite));
    }
    super.upload(event);
  }
}
