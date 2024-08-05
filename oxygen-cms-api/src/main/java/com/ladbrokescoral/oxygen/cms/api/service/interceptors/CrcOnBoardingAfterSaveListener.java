package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class CrcOnBoardingAfterSaveListener extends BasicMongoEventListener<CrcOnBoarding> {

  private static final String PATH_TEMPLATE = "api/{0}/my-stable";
  private static final String FILE_NAME = "onboardings";

  private final OnBoardPublicService onBoardPublicService;

  protected CrcOnBoardingAfterSaveListener(
      DeliveryNetworkService context, OnBoardPublicService onBoardPublicService) {
    super(context);
    this.onBoardPublicService = onBoardPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<CrcOnBoarding> event) {
    String brand = event.getSource().getBrand();
    List<OnBoardDto> onBoardDtoList = Arrays.asList(onBoardPublicService.getOnBoard(brand));
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, onBoardDtoList);
  }
}
