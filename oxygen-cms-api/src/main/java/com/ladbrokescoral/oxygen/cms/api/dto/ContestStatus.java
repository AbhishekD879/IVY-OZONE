package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class ContestStatus {
  private String contestId;
  private String eventId;
  private boolean reportGenerated;
  private int entriesSize;
  private boolean isStarted;
  private boolean isRegularTimeFinished;
}
