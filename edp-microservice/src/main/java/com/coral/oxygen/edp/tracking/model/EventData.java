package com.coral.oxygen.edp.tracking.model;

import com.coral.oxygen.edp.model.output.OutputEvent;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class EventData {
  private OutputEvent event;

  public EventData(OutputEvent event) {
    this.event = event;
  }
}
