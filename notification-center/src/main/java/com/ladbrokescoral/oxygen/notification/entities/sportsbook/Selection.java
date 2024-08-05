package com.ladbrokescoral.oxygen.notification.entities.sportsbook;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Selection extends SportsBookEntity {
  private String selectionKey;
  private String selectionName;
  private String selectionNameTranslated;
  private String selectionStatus;
  private String runnerStatus;
  private String resultCode;
}
