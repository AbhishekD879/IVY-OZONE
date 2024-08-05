package com.coral.oxygen.edp.model.output;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Clock {

  private String sport; // - event.categoryCode.toLowerCase()

  @JsonProperty("ev_id")
  private Long evId; // Number(latestPeriod.eventId)

  @JsonProperty("last_update")
  private String lastUpdate; // - latestPeriod.periodClockState.lastUpdate

  @JsonProperty("period_code")
  private String periodCode; // - latestPeriod.periodCode

  private String state; // - latestPeriod.periodClockState.state

  @JsonProperty("clock_seconds")
  private String clockSeconds; // - latestPeriod.periodClockState.offset

  @JsonProperty("last_update_secs")
  private String
      lastUpdateSecs; // (new Date(periodClockState.lastUpdate).getTime() / 1000).toString(), should
  // be calculated

  @JsonProperty("start_time_secs")
  private String
      startTimeSecs; // (new Date(event.startTime).getTime() / 1000).toString(), event.startTime -
  // should be calculated

  @JsonProperty("offset_secs")
  private String
      offsetSecs; // (parseInt(periodClockState.offset, 10) + deltaSeconds).toString() // - should
  // be calculated
}
