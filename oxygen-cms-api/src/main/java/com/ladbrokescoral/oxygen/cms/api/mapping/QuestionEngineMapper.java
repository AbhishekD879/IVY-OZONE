package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuestionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizDto;
import com.ladbrokescoral.oxygen.cms.api.dto.QuizPrizeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Question;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizPrize;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QuestionEngineMapper {
  static QuestionEngineMapper getInstance() {
    return QuestionEngineMapperInstance.INSTANCE;
  }

  @Mapping(
      target = "splashPage",
      expression = "java(QuizSplashPageMapper.getInstance().toDto(source.getSplashPage()))")
  @Mapping(
      target = "quizLogoSvgFilePath",
      expression =
          "java(source.getQuizLogoSvg() != null ? source.getQuizLogoSvg().relativePath() : null)")
  @Mapping(
      target = "quizBackgroundSvgFilePath",
      expression =
          "java(source.getQuizBackgroundSvg() != null ? source.getQuizBackgroundSvg().relativePath() : null)")
  @Mapping(
      target = "defaultQuestionsDetails",
      expression =
          "java(QuestionDetailsMapper.getInstance().toDto(source.getDefaultQuestionsDetails()))")
  @Mapping(
      target = "upsell",
      expression = "java(UpsellMapper.getInstance().toDto(source.getUpsell()))")
  @Mapping(
      target = "endPage",
      expression = "java(EndPageMapper.getInstance().toDto(source.getEndPage()))")
  @Mapping(
      target = "submitPopup",
      expression = "java(QuizPopupMapper.getInstance().toDto(source.getSubmitPopup()))")
  @Mapping(
      target = "exitPopup",
      expression = "java(QuizPopupMapper.getInstance().toDto(source.getExitPopup()))")
  @Mapping(target = "correctAnswersPrizes", expression = "java(toPrizes(source))")
  @Mapping(
      target = "eventDetails",
      expression = "java(QuizEventDetailsMapper.getInstance().toDto(source.getEventDetails()))")
  @Mapping(
      target = "quizConfiguration",
      expression =
          "java(QuizConfigurationMapper.getInstance().toDto(source.getQuizConfiguration()))")
  QuizDto toDto(Quiz source);

  @Mapping(
      target = "questionDetails",
      expression = "java(QuestionDetailsMapper.getInstance().toDto(source.getQuestionDetails()))")
  QuestionDto toQuestionDto(Question source);

  default Map<Integer, QuizPrizeDto> toPrizes(Quiz source) {
    List<QuizPrize> prizes = source.getCorrectAnswersPrizes();
    return prizes != null
        ? prizes.stream()
            .collect(
                Collectors.toMap(
                    QuizPrize::getCorrectSelections,
                    prize ->
                        new QuizPrizeDto()
                            .setAmount(prize.getAmount())
                            .setCurrency(prize.getCurrency())
                            .setPrizeType(prize.getPrizeType())
                            .setPromotionId(prize.getPromotionId())))
        : Collections.emptyMap();
  }

  final class QuestionEngineMapperInstance {
    private static final QuestionEngineMapper INSTANCE =
        Mappers.getMapper(QuestionEngineMapper.class);

    private QuestionEngineMapperInstance() {}
  }
}
