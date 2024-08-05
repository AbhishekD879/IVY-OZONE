package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class QuizPopupDto {

  private String iconSvgPath;
  private String header;
  private String description;
  private String submitCTAText;
  private String closeCTAText;
}
