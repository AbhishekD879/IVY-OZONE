package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@EqualsAndHashCode
public class QuizConfiguration {

  private boolean showSubmitPopup = true;
  private boolean showExitPopup = true;
  private boolean showSplashPage = true;
  private boolean showEventDetails = true;
  private boolean showProgressBar = true;
  private boolean showQuestionNumbering = true;
  private boolean showSwipeTutorial = true;
  private boolean useBackButtonToExitAndHideXButton = true;
  private boolean showPreviousAndLatestTabs = true;
}
