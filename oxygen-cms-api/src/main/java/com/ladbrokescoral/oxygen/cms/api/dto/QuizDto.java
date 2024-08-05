package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QEQuickLinks;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.QuizLoginRule;
import java.time.Instant;
import java.util.Map;
import lombok.Data;

@Data
public class QuizDto {

  private String id;
  /**
   * Id of the certain Quiz UI instance. Could be either some
   * url(.../quick-link/premiere-league-quiz) or some UUID.
   */
  private String sourceId;

  private String title;
  private String brand;
  private boolean active;
  private QuestionDto firstQuestion;
  private Instant displayFrom;
  private Instant displayTo;
  private Instant entryDeadline;
  private SplashPageDto splashPage;
  private QEQuickLinks qeQuickLinks;
  private QuizLoginRule quizLoginRule;
  private UpsellDto upsell;
  private String quizLogoSvgFilePath;
  private String quizBackgroundSvgFilePath;
  private QuestionDetailsDto defaultQuestionsDetails;
  private EndPageDto endPage;
  private Map<Integer, QuizPrizeDto> correctAnswersPrizes;
  private QuizPopupDto submitPopup;
  private QuizPopupDto exitPopup;
  private EventDetailsDto eventDetails;
  private QuizConfigurationDto quizConfiguration;
  private CoinDto coin;
}
