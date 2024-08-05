package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.QuizPopupSettingRepository;
import java.time.Instant;
import java.util.Optional;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class QuizPopupSettingService extends AbstractService<QuizPopupSetting> {
  private final QuizPopupSettingRepository quizPopupRepository;
  private final QuestionEngineService questionEngineService;

  public QuizPopupSettingService(
      QuizPopupSettingRepository quizPopupRepository,
      @Lazy QuestionEngineService questionEngineService) {
    super(quizPopupRepository);
    this.quizPopupRepository = quizPopupRepository;
    this.questionEngineService = questionEngineService;
  }

  @Override
  public QuizPopupSetting save(QuizPopupSetting entity) {
    if (quizPopupRepository.existsByBrand(entity.getBrand())) {
      throw new IllegalArgumentException(
          String.format(
              "Only one QuizPopupSetting could exist per brand: '%s'", entity.getBrand()));
    }
    return assignQuiz(entity);
  }

  @Override
  public QuizPopupSetting update(QuizPopupSetting existingEntity, QuizPopupSetting updateEntity) {
    if (!existingEntity.getBrand().equals(updateEntity.getBrand())) {
      throw new IllegalArgumentException(
          "Brand cannot be cannot be changed once QuizPopup is created");
    }
    updateEntity.setExpirationDate(existingEntity.getExpirationDate());
    if (isQuizReassigned(existingEntity, updateEntity)) {
      return quizPopupRepository.save(assignQuiz(updateEntity));
    }
    return quizPopupRepository.save(updateEntity);
  }

  public Optional<QuizPopupSetting> findActiveByBrand(String brand) {
    return quizPopupRepository
        .findOneByBrand(brand)
        .filter(QuizPopupSetting::isEnabled)
        .filter(quizPopupSetting -> quizPopupSetting.getExpirationDate() != null)
        .filter(quizPopupSetting -> quizPopupSetting.getExpirationDate().isAfter(Instant.now()));
  }

  public QuizPopupSetting getByBrand(String brand) {
    return quizPopupRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }

  private boolean isQuizReassigned(QuizPopupSetting existingEntity, QuizPopupSetting updateEntity) {
    return !existingEntity.getQuizId().equals(updateEntity.getQuizId());
  }

  private QuizPopupSetting assignQuiz(QuizPopupSetting entity) {
    return questionEngineService
        .findOne(entity.getQuizId())
        .map(quiz -> super.save(entity.setExpirationDate(quiz.getDisplayTo())))
        .orElseThrow(
            () ->
                new NotFoundException(
                    String.format("Quiz with id '%s' not found", entity.getQuizId())));
  }
}
