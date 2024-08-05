package com.coral.oxygen.middleware.ms.quickbet.impl;

import java.time.Duration;

public interface OnceExecutor {

  void executeOnceDuringTimePeriod(
      String identity, Runnable action, Runnable rejectedAction, Duration period);
}
