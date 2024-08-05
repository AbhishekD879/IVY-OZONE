package com.coral.oxygen.middleware.ms.quickbet.util;

import org.joda.time.DateTime;

public final class JavaDateUtils {

  private JavaDateUtils() {}

  /**
   * Modify seconds and milliseconds to the format s0.000
   *
   * @param dateTime
   * @return date to the format yyyy-MM-dd'T'HH:mm:s0.000Z
   */
  public static DateTime reformatToSeconds(DateTime dateTime, int seconds) {

    int round = (int) Math.floor(dateTime.getSecondOfMinute() / (seconds * 1.0)) * seconds;

    return dateTime.secondOfMinute().roundFloorCopy().withSecondOfMinute(round);
  }
}
