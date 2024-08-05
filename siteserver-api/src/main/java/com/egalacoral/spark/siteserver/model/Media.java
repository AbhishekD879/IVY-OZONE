package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Media extends Identity {

  private String id;
  private String refRecordId;
  private String refRecordType;
  private String accessProperties;
  private String siteChannels;
  private String startTime;
}
