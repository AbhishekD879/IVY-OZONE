package com.ladbrokescoral.oxygen.questionengine.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.*;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizLoginRule;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.time.Instant;
import java.util.Map;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public abstract class AbstractQuizDto {

  private String id;
  /**
   * Id of the certain Quiz UI instance. Could be either some url(.../quick-link/premiere-league-quiz)
   * or some UUID.
   */
  private String sourceId;
  private Instant displayFrom;
  private Instant displayTo;
  private Instant entryDeadline;
  private String title;
  private SplashPageDto splashPage;
  private QEQuickLinksDto qeQuickLinks;
  private QuizLoginRule quizLoginRule;

  @JsonIgnore
  private UpsellConfigurationDto upsellConfiguration;

  private String quizLogoSvgFilePath;
  private String quizBackgroundSvgFilePath;
  private QuestionDetailsDto defaultQuestionsDetails;
  private EndPageDto endPage;
  private QuizPopupDto submitPopup;
  private QuizPopupDto exitPopup;
  private UpsellDto upsell;

  private Map<Integer, PrizeDto> correctAnswersPrizes;
  private EventDetailsDto eventDetails;
  private QuizConfigurationDto quizConfiguration;
  private CoinDto coin;
  
  public abstract AbstractQuestionDto firstQuestion();
}
