package com.coral.oxygen.middleware.scheduler;

public abstract class ConsumeScheduledTask {
  protected volatile long lastTimeLaunched = System.currentTimeMillis();
  public static final int MILLISEC_1000 = 1000;

  public long getLastTimeLaunched() {
    return lastTimeLaunched;
  }

  public abstract void process() throws InterruptedException;
}
