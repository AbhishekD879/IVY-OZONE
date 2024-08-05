package com.egalacoral.spark.timeform.api.connectivity;

public class SystemTimeProvider implements TimeProvider {
  @Override
  public long currentTime() {
    return System.currentTimeMillis();
  }
}
