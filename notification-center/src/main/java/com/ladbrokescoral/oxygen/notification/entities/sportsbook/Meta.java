package com.ladbrokescoral.oxygen.notification.entities.sportsbook;

import lombok.Data;

@Data
public class Meta {
  private String operation;
  private String messageType;
  private String messageID;
  private String source;
  private String recordModifiedTime;
}
