package com.coral.oxygen.middleware.ms.quickbet.util;

import static org.assertj.core.api.Assertions.assertThat;

import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import org.junit.jupiter.api.Test;

class BettingApiBetUtilsTest {

  @Test
  void testIsConfirmed() {
    Bet confirmedBet = new Bet();
    confirmedBet.setIsConfirmed(YesNo.Y);

    Bet notConfirmedBet = new Bet();
    notConfirmedBet.setIsConfirmed(YesNo.N);

    Bet isConfirmedNull = new Bet();
    isConfirmedNull.setIsConfirmed(null);

    assertThat(BettingApiBetUtils.isConfirmed(confirmedBet)).isTrue();
    assertThat(BettingApiBetUtils.isConfirmed(notConfirmedBet)).isFalse();
    assertThat(BettingApiBetUtils.isConfirmed(isConfirmedNull)).isTrue();
  }

  @Test
  void testIsBetOverask() {
    Bet overaskBet = new Bet();
    overaskBet.setIsConfirmed(YesNo.N);
    overaskBet.setIsReferred(YesNo.Y);

    Bet overaskBetConfirmed = new Bet();
    overaskBetConfirmed.setIsConfirmed(YesNo.Y);

    Bet notOveraskBet = new Bet();
    notOveraskBet.setIsConfirmed(YesNo.N);
    notOveraskBet.setIsReferred(YesNo.N);

    assertThat(BettingApiBetUtils.isBetOverask(overaskBet)).isTrue();
    assertThat(BettingApiBetUtils.isBetOverask(notOveraskBet)).isFalse();
    assertThat(BettingApiBetUtils.isBetOverask(overaskBetConfirmed)).isFalse();
  }

  @Test
  void testBetInRun() {
    Bet betInRun = new Bet();
    betInRun.setConfirmationExpectedAt("10");
    betInRun.setIsConfirmed(YesNo.N);
    betInRun.setProvider(BetUtils.OPEN_BET_BIR_PROVIDER);

    Bet betNotConfirmed = new Bet();
    betNotConfirmed.setIsConfirmed(YesNo.Y);

    Bet betOtherProvider = new Bet();
    betOtherProvider.setIsConfirmed(YesNo.N);
    betOtherProvider.setProvider("Other");

    Bet betConfirmationExpectedAtBlank = new Bet();
    betConfirmationExpectedAtBlank.setIsConfirmed(YesNo.N);
    betConfirmationExpectedAtBlank.setProvider(BetUtils.OPEN_BET_BIR_PROVIDER);
    betConfirmationExpectedAtBlank.setConfirmationExpectedAt("");

    assertThat(BettingApiBetUtils.isBetInRun(betInRun)).isTrue();
    assertThat(BettingApiBetUtils.isBetInRun(betNotConfirmed)).isFalse();
    assertThat(BettingApiBetUtils.isBetInRun(betOtherProvider)).isFalse();
    assertThat(BettingApiBetUtils.isBetInRun(betConfirmationExpectedAtBlank)).isFalse();
  }

  @Test
  void testIsCancelled() {
    Bet cancelledBet = new Bet();
    cancelledBet.setIsCancelled(YesNo.Y);

    Bet notCancelledBet = new Bet();
    notCancelledBet.setIsCancelled(YesNo.N);

    assertThat(BettingApiBetUtils.isCancelled(cancelledBet)).isTrue();
    assertThat(BettingApiBetUtils.isCancelled(notCancelledBet)).isFalse();
  }
}
