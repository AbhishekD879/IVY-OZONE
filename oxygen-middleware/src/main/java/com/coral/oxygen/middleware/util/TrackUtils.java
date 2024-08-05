package com.coral.oxygen.middleware.util;

import java.time.Instant;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Slf4j
public class TrackUtils {

  public static void logDuration(String metricName, long start) {
    long durationSeconds = (System.currentTimeMillis() - start) / 1000;
    if (durationSeconds >= 5) {
      log.info("{} took {}s", metricName, durationSeconds);
    }
  }

  public static void logExcecutionTime(String metricName, Instant startTime) {
    log.info("{} started at {}", metricName, startTime);
  }
}
