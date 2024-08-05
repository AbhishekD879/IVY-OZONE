package com.ladbrokescoral.cashout.service.updates

import com.ladbrokescoral.cashout.model.safbaf.betslip.Bet
import com.ladbrokescoral.cashout.model.safbaf.betslip.Bets
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip

class BetslipUpdateProcessorTest extends UpdateProcessorsSpec {
  private UserUpdateTrigger userUpdateTrigger = Mock(UserUpdateTrigger)
  private UpdateProcessor<Betslip> betslipUpdateProcessor = new BetslipUpdateProcessor(userUpdateTrigger)

  def "BetSlip updates settled=false and stake=null are ignored"() {
    when:
    betslipUpdateProcessor.process(userReqCtx, betslip)
    then:
    0 * _
    where:
    betslip << [
      null,
      new Betslip(),
      settled(betslipWithBet1(), false)
    ]
  }

  def "When settled bet received then context is updated"() {
    given:
    def bet1 = betslipWithBet1()
    bet1.getIsSettled() >> true
    when:
    betslipUpdateProcessor.process(userReqCtx, bet1)
    then:
    1 * userReqCtx.addSettledBets(new HashSet<>(["1"]))
    1 * userUpdateTrigger.triggerBetSettled(UserUpdateTriggerDto.builder()
        .betIds(["1"] as Set)
        .token("123")
        .build())
  }

  def "When settled bet received then context is updated with new bets"() {
    given:
    def bet1 = betslipWithBet1()
    bet1.getIsSettled() >> true
    when:
    betslipUpdateProcessor.process(userReqCtx, bet1)
    then:
    1 * userReqCtx.addSettledBets(new HashSet<>(["1"]))
  }

  def "Bet stake change after partial cashout updates the model"() {
    given:
    def bet1 = betslipWithBet1();
    bet1.bets.bet[0].getStake() >> "0.5"
    when:
    betslipUpdateProcessor.process(userReqCtx, bet1)
    then:
    userReqCtx.getUserBets()[0].getStake().getValue() == "0.5"
  }

  def settled(Betslip betslip, boolean isSettled) {
    betslip.getIsSettled() >> isSettled
    betslip
  }

  def betslipWithBet1() {
    def betslip = Mock(Betslip)
    def bets = Mock(Bets)
    def bet = Mock(Bet)
    bet.getBetKey() >> "1"
    bets.getBet() >> [bet]
    betslip.getBets() >> bets
    return betslip
  }
}
