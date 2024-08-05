package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;

@Data
public class QuizPopup {
  private String iconSvgPath;
  private String header;
  private String description;
  private String submitCTAText;
  private String closeCTAText;
}
