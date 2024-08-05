package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardingGuideDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardingGuidePublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class OnBoardingGuidesAfterSaveListener extends BasicMongoEventListener<OnBoardingGuide> {

  private final OnBoardingGuidePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "on-boarding-guide";

  public OnBoardingGuidesAfterSaveListener(
      OnBoardingGuidePublicService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<OnBoardingGuide> event) {
    String brand = event.getSource().getBrand();
    List<OnBoardingGuideDto> content = service.getOnBoardingGuides(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
