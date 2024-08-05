package com.ladbrokescoral.cashout.model.safbaf;

import lombok.Data;

@Data
public class Meta {
  private Integer categoryKey;
  private Integer classKey;
  private Integer typeKey;
  private Integer eventKey;
  private Integer marketKey;
  private String operation;
  private String messageType;
  private String parents;
  private String messageID;
  private String channel;
  private String source;
  private String recordModifiedTime;
  private String messageTimestamp;
  private String externalEventReference;
}
