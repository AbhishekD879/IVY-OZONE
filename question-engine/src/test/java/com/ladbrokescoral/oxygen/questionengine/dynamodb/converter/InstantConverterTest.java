package com.ladbrokescoral.oxygen.questionengine.dynamodb.converter;

import org.junit.Test;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;


public class InstantConverterTest {
  private final InstantConverter instantConverter = new InstantConverter();

  @Test
  public void convert() {
    Long actual = instantConverter.convert(Instant.parse("2018-12-25T00:00:00Z"));

    assertThat(actual).isEqualTo(1545696000000L);
  }

  @Test
  public void unconvert() {
    Instant actual = instantConverter.unconvert(1545696000000L);

    assertThat(actual).isEqualTo(Instant.parse("2018-12-25T00:00:00Z"));
  }
}
