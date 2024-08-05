package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import lombok.Data;

@Data
public class QuestionDetailsDto {
  private String topLeftHeader;
  private String topRightHeader;
  private String middleHeader;
  private String homeTeamName;
  private String homeTeamSvgFilePath;
  private String awayTeamName;
  private String channelSvgFilePath;
  private String awayTeamSvgFilePath;
  private String signposting;
  private String description;
}
