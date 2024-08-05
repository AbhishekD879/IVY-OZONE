package com.ladbrokescoral.aggregation.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Map;
import lombok.Data;

@Data
public class RaceInfo {

  @JsonProperty("Error")
  private boolean error;

  @JsonProperty("ErrorMessage")
  private String errorMessage;

  private Map<String, Event> document;
}
