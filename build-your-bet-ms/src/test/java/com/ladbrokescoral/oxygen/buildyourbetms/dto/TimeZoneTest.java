package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import static org.assertj.core.api.Assertions.assertThat;

import java.security.InvalidParameterException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class TimeZoneTest {

  @Test
  void fromNotNull() {
    TimeZone zone = TimeZone.from("2");
    Assertions.assertNotNull(zone);
  }

  @Test
  void fromNull() {
    InvalidParameterException expectedException =
        Assertions.assertThrows(
            InvalidParameterException.class,
            () -> {
              TimeZone.from(null);
            });
    assertThat(expectedException).isNotNull();
  }

  @Test
  void fromNotNumber() {
    NumberFormatException expectedException =
        Assertions.assertThrows(
            NumberFormatException.class,
            () -> {
              TimeZone.from("dgwddd");
            });
    assertThat(expectedException).isNotNull();
  }

  @Test
  void from5Dot5() {
    TimeZone zone = TimeZone.from("5.5");
    Assertions.assertEquals(5 * 3600 + 1800, zone.toSeconds());
  }

  @Test
  void from2Dot2() {
    TimeZone zone = TimeZone.from("2.2");
    Assertions.assertEquals(2 * 3600 + 720, zone.toSeconds());
  }

  @Test
  void from2Dot20() {
    TimeZone zone = TimeZone.from("2.20");
    Assertions.assertEquals(2 * 3600 + 720, zone.toSeconds());
  }

  @Test
  void from2() {
    TimeZone zone = TimeZone.from("2");
    Assertions.assertEquals(2 * 3600, zone.toSeconds());
  }
}
