package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import lombok.Data;

@Data
public class QuizConfigurationDto {

  private boolean showSubmitPopup;
  private boolean showExitPopup;
  private boolean showSplashPage;
  private boolean showEventDetails;
  private boolean showProgressBar;
  private boolean showQuestionNumbering;
  private boolean showSwipeTutorial;
  private boolean showPreviousAndLatestTabs;
  private boolean useBackButtonToExitAndHideXButton;
}
