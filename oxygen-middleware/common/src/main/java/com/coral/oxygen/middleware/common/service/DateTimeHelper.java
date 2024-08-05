package com.coral.oxygen.middleware.common.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class DateTimeHelper {

  private final DateTimeZone timeZone;

  @Autowired
  public DateTimeHelper(@Value("${time.zone:GMT}") String timeZone) {
    this.timeZone = DateTimeZone.forID(timeZone);
  }

  public DateTime nowTrimmedToTenSeconds() {
    return trimToTenSeconds(DateTime.now(timeZone));
  }

  /**
   * Modify seconds and milliseconds to the format s0.000
   *
   * @param dateTime
   * @return date to the format yyyy-MM-dd'T'HH:mm:s0.000Z
   */
  public static DateTime trimToTenSeconds(DateTime dateTime) {

    int round = (int) Math.floor(dateTime.getSecondOfMinute() / 10.0) * 10;

    return dateTime.secondOfMinute().roundFloorCopy().withSecondOfMinute(round);
  }

  public static LocalDateTime trimToTenSeconds(LocalDateTime dateTime) {
    int round = (int) Math.floor(dateTime.getSecond() / 10.0) * 10;
    return dateTime.withSecond(round).withNano(0);
  }

  public static String toString(LocalDateTime dateTime) {
    return dateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS"));
  }
}
