package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class QuizPopupSettingDetailsDto {
  private String id;

  private String popupTitle;
  private String popupText;
  private String quizId;
  private String yesText;
  private String remindLaterText;
  private String dontShowAgainText;
}
