package com.egalacoral.spark.timeform.model;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Type;

public class LostEvent {
  private final Type type;
  private final Event event;

  public LostEvent(Type type, Event event) {
    this.type = type;
    this.event = event;
  }

  public Type getType() {
    return type;
  }

  public Event getEvent() {
    return event;
  }
}
