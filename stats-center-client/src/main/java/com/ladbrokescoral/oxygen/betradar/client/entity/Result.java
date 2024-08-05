package com.ladbrokescoral.oxygen.betradar.client.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Result {

  private String goalsString;

  private FullTime fullTime;
}
