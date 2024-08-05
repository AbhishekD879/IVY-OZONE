package com.ladbrokescoral.oxygen.notification.utils;

public class RedisKey {

  private static final String WINALERT_REDIS_KEY_PATTERN = "win_alert:%s:%s";
  private static final String HORSES_GREYHOUNDS_REDIS_KEY_PATTERN = "horses_greyhounds:%s:%s";

  public static String forWinAlert(String betKey, String platformName) {
    return String.format(WINALERT_REDIS_KEY_PATTERN, betKey, platformName);
  }

  public static String forRacing(long eventId, String platformName) {
    return String.format(HORSES_GREYHOUNDS_REDIS_KEY_PATTERN, eventId, platformName);
  }

  public static String forEvent(Long eventId) {
    return String.format("%s", eventId);
  }
}
