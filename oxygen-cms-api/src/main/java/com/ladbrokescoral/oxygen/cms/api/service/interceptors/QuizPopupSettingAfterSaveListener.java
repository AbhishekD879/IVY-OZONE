package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuizPopupSettingPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class QuizPopupSettingAfterSaveListener
    extends BasicInitialDataAfterSaveListener<QuizPopupSetting> {
  private final QuizPopupSettingPublicService quizPopupPublicService;

  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "quiz-popup-setting-details";

  public QuizPopupSettingAfterSaveListener(
      final QuizPopupSettingPublicService quizPopupPublicService,
      final InitialDataService initialDataService,
      final DeliveryNetworkService deliveryNetworkService) {
    super(initialDataService, deliveryNetworkService);
    this.quizPopupPublicService = quizPopupPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<QuizPopupSetting> event) {
    String brand = event.getSource().getBrand();
    Optional<QuizPopupSettingDetailsDto> contentDetails =
        quizPopupPublicService.findPopupDetailsByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, contentDetails);
    super.upload(event);
  }
}
