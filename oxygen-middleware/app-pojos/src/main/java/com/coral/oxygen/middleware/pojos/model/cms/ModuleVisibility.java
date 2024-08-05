package com.coral.oxygen.middleware.pojos.model.cms;

import org.joda.time.DateTime;

public class ModuleVisibility {

  private DateTime displayFrom;
  private DateTime displayTo;
  private boolean enabled;

  public DateTime getDisplayFrom() {
    return displayFrom;
  }

  public void setDisplayFrom(DateTime displayFrom) {
    this.displayFrom = displayFrom;
  }

  public DateTime getDisplayTo() {
    return displayTo;
  }

  public void setDisplayTo(DateTime displayTo) {
    this.displayTo = displayTo;
  }

  public boolean isEnabled() {
    return enabled;
  }

  public void setEnabled(boolean enabled) {
    this.enabled = enabled;
  }
}
