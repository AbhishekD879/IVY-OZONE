package com.ladbrokescoral.oxygen.hydra.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Response {

  @JsonProperty("x-forward-for")
  public String forwardFor;

  @JsonProperty("timestamp")
  public Long timestamp;

  public Response(String forwardFor, Long timestamp) {
    this.forwardFor = forwardFor;
    this.timestamp = timestamp;
  }
}
