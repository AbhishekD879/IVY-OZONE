package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;

@Data
public class QuestionDetails {
  private String topLeftHeader;
  private String topRightHeader;
  private String middleHeader;
  private String homeTeamName;
  private String homeTeamSvgFilePath;
  private String awayTeamName;
  private String awayTeamSvgFilePath;
  private String channelSvgFilePath;
  private String description;
  private String signposting;
}
