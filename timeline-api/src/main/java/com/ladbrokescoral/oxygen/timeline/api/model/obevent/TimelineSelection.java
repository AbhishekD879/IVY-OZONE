package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import lombok.Data;

@Data
public class TimelineSelection {

  private SelectionStatus selectionStatus;
  private EventStatus eventStatus;
  private MarketStatus marketStatus;
  private Price price;

  private Long selectionId;
  private Long marketId;
  private Long eventId;
}
