package com.coral.oxygen.edp.tracking;

public interface UpdateScheduler {
  void setTracker(Tracker tracker);

  void schedule(long milliseconds);
}
