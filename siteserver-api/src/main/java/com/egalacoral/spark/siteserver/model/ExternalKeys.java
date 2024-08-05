package com.egalacoral.spark.siteserver.model;

import lombok.Data;

@Data
public class ExternalKeys {

  private String id;
  private String externalKeyTypeCode;
  private String mappings;
  private String refRecordType;
}
