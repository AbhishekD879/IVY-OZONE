package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import lombok.Data;

@Data
public class QuestionDetails {

  private String topLeftHeader;
  private String topRightHeader;
  private String middleHeader;
  private String homeTeamName;
  private Filename homeTeamSvg = new Filename();
  private String awayTeamName;
  private Filename awayTeamSvg = new Filename();
  private Filename channelSvg = new Filename();
  private String description;
  private String signposting;
}
