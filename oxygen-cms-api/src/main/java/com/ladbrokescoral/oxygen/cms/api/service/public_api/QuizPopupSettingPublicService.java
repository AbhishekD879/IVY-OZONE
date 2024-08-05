package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizPopupSettingDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.QuizPopupGeneralSettingMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.QuizPopupSettingDetailsMapper;
import com.ladbrokescoral.oxygen.cms.api.service.QuestionEngineService;
import com.ladbrokescoral.oxygen.cms.api.service.QuizPopupSettingService;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class QuizPopupSettingPublicService {

  private final QuizPopupSettingService service;
  private final QuestionEngineService questionEngineService;

  public QuizPopupSettingPublicService(
      QuizPopupSettingService service, QuestionEngineService questionEngineService) {
    this.service = service;
    this.questionEngineService = questionEngineService;
  }

  public Optional<QuizPopupSettingDto> findGeneralSettingsByBrand(String brand) {
    return service
        .findActiveByBrand(brand)
        .flatMap(
            quizPopupSetting ->
                questionEngineService
                    .findOne(quizPopupSetting.getQuizId())
                    .map(
                        quiz ->
                            QuizPopupGeneralSettingMapper.INSTANCE
                                .toDto(quizPopupSetting)
                                .setSourceId(quiz.getSourceId())));
  }

  public Optional<QuizPopupSettingDetailsDto> findPopupDetailsByBrand(String brand) {
    return service.findActiveByBrand(brand).map(QuizPopupSettingDetailsMapper.INSTANCE::toDto);
  }
}
