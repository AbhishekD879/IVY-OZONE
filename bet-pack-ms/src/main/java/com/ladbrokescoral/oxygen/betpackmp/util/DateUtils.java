package com.ladbrokescoral.oxygen.betpackmp.util;

import com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants;
import java.time.*;
import java.time.format.DateTimeFormatter;

public class DateUtils {
  private static final String myReg = "\\W|_";

  private DateUtils() {
    throw new IllegalStateException("DateUtils class");
  }

  public static Long minDiff(String date) {

    LocalDateTime localDateTime =
        LocalDateTime.parse(date, DateTimeFormatter.ofPattern(BetPackConstants.DATE_FORMAT));

    ZonedDateTime systemZoneDateTime = localDateTime.atZone(ZoneId.of("Europe/London"));
    ZonedDateTime utcDateTime = systemZoneDateTime.withZoneSameInstant(ZoneId.of("UTC"));

    Instant utcTimestamp = utcDateTime.toInstant();
    Instant currentUtcTimestamp = Instant.now();

    Duration res = Duration.between(currentUtcTimestamp, utcTimestamp);
    return res.toMinutes();
  }

  public static String scrub(String input) {
    String sanitized = alphanumericOnly(input);
    int[] codepoints = new int[sanitized.length()];
    for (int i = 0; i < sanitized.length(); ++i) {
      codepoints[i] = sanitized.codePointAt(i);
    }
    return new String(codepoints, 0, codepoints.length);
  }

  public static String alphanumericOnly(String input) {
    return input == null ? "" : input.replaceAll(myReg, "");
  }
}
