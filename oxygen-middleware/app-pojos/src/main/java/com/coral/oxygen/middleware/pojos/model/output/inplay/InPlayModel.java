package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class InPlayModel implements Serializable {

  private Collection<Long> eventsIds = new ArrayList<>();

  @SerializedName("eventsBySports")
  @JsonProperty("eventsBySports")
  private List<SportSegment> sportEvents = new ArrayList<>();

  private int eventCount;

  public Collection<Long> getEventsIds() {
    return eventsIds;
  }

  public void setEventsIds(Collection<Long> eventsIds) {
    this.eventsIds = eventsIds;
  }

  @ChangeDetect(compareList = true)
  public List<SportSegment> getSportEvents() {
    return sportEvents;
  }

  public void setEventCount(int eventCount) {
    this.eventCount = eventCount;
  }

  public int getEventCount() {
    return eventCount;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("InPlayModel{");
    sb.append("eventsIds=").append(eventsIds);
    sb.append(", eventCount=").append(eventCount);
    sb.append(", sportEvents=").append(sportEvents);
    sb.append('}');
    return sb.toString();
  }
}
