package com.coral.oxygen.middleware.ms.liveserv.impl.incidents;

import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.Objects;

public abstract class Validator {

  private Validator next;

  protected Validator(Validator next) {
    this.next = next;
  }

  protected abstract boolean checkCondition(IncidentsEvent event);

  /**
   * This method is used to validate the Incidents Messages which is coming from Feed
   *
   * @param event
   * @return true or false
   */
  public boolean validate(IncidentsEvent event) {
    if (!checkCondition(event)) {
      return false;
    }
    if (Objects.isNull(next)) {
      return true;
    }
    return next.validate(event);
  }
}
