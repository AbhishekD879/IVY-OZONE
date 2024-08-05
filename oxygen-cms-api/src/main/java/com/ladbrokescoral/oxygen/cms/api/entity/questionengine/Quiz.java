package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.AssertTrue;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.validation.annotation.Validated;

@Validated
@Data
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
@Document(collection = "quiz")
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class Quiz extends AbstractEntity implements HasBrand {

  @NotBlank private String title;
  /**
   * Id of the certain Quiz UI instance. Could be either some
   * url(.../quick-link/premiere-league-quiz) or some UUID.
   */
  @NotBlank private String sourceId;

  @NotBlank private String brand;

  private Question firstQuestion;

  @NotNull private Instant displayFrom;

  @NotNull private Instant displayTo;

  @NotNull private Instant entryDeadline;

  private boolean active;

  private Filename quizLogoSvg = new Filename();
  private Filename quizBackgroundSvg = new Filename();

  private SplashPage splashPage;

  private QEQuickLinks qeQuickLinks;

  private QuizLoginRule quizLoginRule;

  private QuestionDetails defaultQuestionsDetails = new QuestionDetails();

  @Valid private Upsell upsell;

  private EndPage endPage;

  private Coin coin;

  private QuizPopup submitPopup = new QuizPopup();
  private QuizPopup exitPopup = new QuizPopup();

  private List<QuizPrize> correctAnswersPrizes;
  private EventDetails eventDetails = new EventDetails();
  private QuizConfiguration quizConfiguration = new QuizConfiguration();

  @AssertTrue(
      message =
          "Entry deadline has not to be null and to be between displayFrom and displayTo dates")
  private boolean isValidEntryDeadline() {
    return this.getEntryDeadline() != null
        && this.getEntryDeadline().isAfter(this.getDisplayFrom())
        && this.getEntryDeadline().isBefore(this.getDisplayTo());
  }
}
