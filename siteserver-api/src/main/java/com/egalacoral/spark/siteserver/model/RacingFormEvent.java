package com.egalacoral.spark.siteserver.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class RacingFormEvent {

  private String distance;
  private String going;
  private String id;
  private String refRecordType;
  private String refRecordId;
  private String raceNumber;
  private String title;
  private String overview;

  @JsonProperty("class")
  private String className;

  private String prize;
}
