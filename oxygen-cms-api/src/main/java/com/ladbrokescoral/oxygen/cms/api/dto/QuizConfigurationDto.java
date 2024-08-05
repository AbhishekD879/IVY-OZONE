package com.ladbrokescoral.oxygen.cms.api.dto;

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
  private boolean useBackButtonToExitAndHideXButton;
  private boolean showPreviousAndLatestTabs;
}
