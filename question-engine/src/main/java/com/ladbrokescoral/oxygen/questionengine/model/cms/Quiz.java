package com.ladbrokescoral.oxygen.questionengine.model.cms;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.Instant;
import java.util.Map;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class Quiz {
  private String id;
  private String sourceId;
  private String title;
  private boolean active;
  private Question firstQuestion;
  private Instant displayFrom;
  private Instant displayTo;
  private Instant entryDeadline;
  private SplashPage splashPage;
  private QEQuickLinks qeQuickLinks;
  private QuizLoginRule quizLoginRule;

  @JsonProperty("upsell")
  private UpsellConfiguration upsellConfiguration;
  private String quizLogoSvgFilePath;
  private String quizBackgroundSvgFilePath;
  private QuestionDetails defaultQuestionsDetails;
  private EndPage endPage;
  private QuizPopup submitPopup;
  private QuizPopup exitPopup;
  private Map<Integer, Prize> correctAnswersPrizes;
  private EventDetails eventDetails;
  private QuizConfiguration quizConfiguration;
  private Coin coin;

  public boolean isNotEmpty() {
    return firstQuestion != null;
  }
}
