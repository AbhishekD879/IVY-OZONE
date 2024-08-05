package com.egalacoral.spark.siteserver.model;

import lombok.Data;

@Data
public class Aggregation {

  private String aggregatedRecordType;
  private Integer count;
  private Long id;
  private Long refRecordId;
  private String refRecordType;
}
