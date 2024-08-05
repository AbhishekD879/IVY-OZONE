package com.coral.oxygen.middleware.ms.quickbet.util;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import org.junit.jupiter.api.Test;

public class BetUtilsTest {

  @Test
  public void userStakeWithFreebet() {
    FreeBetRequest freeBetRequest = FreeBetRequest.builder().id(123L).stake("3").build();

    assertThat(BetUtils.calculateTotalStakeWithFreeBet("2", freeBetRequest)).isEqualTo("5");
  }

  @Test
  public void freeBetWithoutUserStake() {
    FreeBetRequest freebet = FreeBetRequest.builder().id(123L).stake("3").build();
    assertThat(BetUtils.calculateTotalStakeWithFreeBet(null, freebet)).isEqualTo("3");
  }

  @Test
  public void freeBetWithZeroUserStake() {
    FreeBetRequest freebet = FreeBetRequest.builder().id(123L).stake("3").build();
    assertThat(BetUtils.calculateTotalStakeWithFreeBet("0", freebet)).isEqualTo("3");
  }
}
