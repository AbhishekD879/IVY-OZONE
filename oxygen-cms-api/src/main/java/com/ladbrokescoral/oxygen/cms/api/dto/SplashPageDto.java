package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class SplashPageDto {

  private String title;
  private String brand;
  private String strapLine;
  private String paragraphText1;
  private String paragraphText2;
  private String paragraphText3;
  private String playForFreeCTAText;
  private String seeYourSelectionsCTAText;
  private String seePreviousSelectionsCTAText;
  private String loginToViewCTAText;
  private String backgroundSvgFilePath;
  private String backgroundSvgFilename;
  private String logoSvgFilePath;
  private String logoSvgFilename;
  private String footerSvgFilePath;
  private String footerSvgFilename;
  private String footerText;
  private boolean showPreviousGamesButton;
}
