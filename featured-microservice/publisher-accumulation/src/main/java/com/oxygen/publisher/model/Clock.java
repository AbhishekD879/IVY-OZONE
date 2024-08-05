package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Represents the Clock model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Clock {

  private String sport;

  @JsonProperty("ev_id")
  private Long evId;

  @JsonProperty("last_update")
  private String lastUpdate;

  @JsonProperty("period_code")
  private String periodCode;

  private String state;

  @JsonProperty("clock_seconds")
  private String clockSeconds;

  @JsonProperty("last_update_secs")
  private String lastUpdateSecs;

  @JsonProperty("start_time_secs")
  private String startTimeSecs;

  @JsonProperty("offset_secs")
  private String offsetSecs;
}
