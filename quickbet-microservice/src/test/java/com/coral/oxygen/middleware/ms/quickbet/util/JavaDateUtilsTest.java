package com.coral.oxygen.middleware.ms.quickbet.util;

import static org.assertj.core.api.Assertions.assertThat;

import org.joda.time.DateTime;
import org.junit.jupiter.api.Test;

public class JavaDateUtilsTest {

  @Test
  public void reformatToSeconds() {
    DateTime dateTime = JavaDateUtils.reformatToSeconds(new DateTime().withMillis(333), 1);
    assertThat(dateTime.getMillisOfSecond()).isEqualTo(0);
  }
}
