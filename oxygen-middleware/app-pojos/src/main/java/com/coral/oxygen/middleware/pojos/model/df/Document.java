package com.coral.oxygen.middleware.pojos.model.df;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class Document implements Serializable {

  private Map<Long, RaceEvent> eventMap = new HashMap<>();
  private static final long serialVersionUID = 3290753506809689792L;

  @JsonAnyGetter
  public Map<Long, RaceEvent> getEventMap() {
    return this.eventMap;
  }

  @JsonAnySetter
  public void setEventMap(String eventId, RaceEvent raceEvent) {
    this.eventMap.put(Long.valueOf(eventId), raceEvent);
  }

  public Document withEvent(Long eventId, RaceEvent value) {
    this.eventMap.put(eventId, value);
    return this;
  }
}
