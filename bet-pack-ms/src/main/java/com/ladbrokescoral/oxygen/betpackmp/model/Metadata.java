package com.ladbrokescoral.oxygen.betpackmp.model;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class Metadata {

  private EventType eventType;

  private EventSource eventSource;

  public Metadata(final EventSource eventSource, final EventType eventType) {
    this.eventType = eventType;
    this.eventSource = eventSource;
  }
}
