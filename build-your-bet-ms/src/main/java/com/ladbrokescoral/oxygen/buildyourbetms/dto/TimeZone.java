package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import java.math.BigDecimal;
import java.security.InvalidParameterException;
import org.springframework.util.ObjectUtils;

public class TimeZone {

  public static final int SECONDS_PER_HOUR = 3600;
  private final BigDecimal value;

  public TimeZone(BigDecimal hours) {
    this.value = hours;
  }

  public static TimeZone from(String hours) {
    TimeZone zone;
    if (ObjectUtils.isEmpty(hours)) {
      throw new InvalidParameterException("hours should't be null or empty");
    } else {
      zone = new TimeZone(new BigDecimal(hours));
    }
    return zone;
  }

  public int toSeconds() {
    return (int) (value.doubleValue() * SECONDS_PER_HOUR);
  }

  @Override
  public String toString() {
    return value.toString();
  }
}
