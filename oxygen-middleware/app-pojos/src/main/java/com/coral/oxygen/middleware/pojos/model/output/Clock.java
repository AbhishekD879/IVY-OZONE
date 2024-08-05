package com.coral.oxygen.middleware.pojos.model.output;

import java.io.Serializable;
import lombok.Data;

@Data
public class Clock implements Serializable {
  private String sport; // - event.categoryCode.toLowerCase()
  private Long ev_id; // Number(latestPeriod.eventId)
  private String last_update; // - latestPeriod.periodClockState.lastUpdate
  private String period_code; // - latestPeriod.periodCode
  private String state; // - latestPeriod.periodClockState.state
  private String clock_seconds; // - latestPeriod.periodClockState.offset
  private String
      last_update_secs; // (new Date(periodClockState.lastUpdate).getTime() / 1000).toString(), // -
  // should be calculated
  private String start_time_secs; // (new Date(event.startTime).getTime() / 1000).toString(), // -
  // event.startTime - should be calculated
  private String
      offset_secs; // (parseInt(periodClockState.offset, 10) + deltaSeconds).toString() // - should
  // be calculated
}
