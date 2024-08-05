package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import lombok.Data;

@Data
public class QuizPopup {

  private Filename icon = new Filename();
  private String header;
  private String description;
  private String submitCTAText;
  private String closeCTAText;
}
