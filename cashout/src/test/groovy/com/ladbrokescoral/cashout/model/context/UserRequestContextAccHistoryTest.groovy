package com.ladbrokescoral.cashout.model.context

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel
import spock.lang.Specification

class UserRequestContextAccHistoryTest extends Specification {
  private UserRequestContextAccHistory ctx

  void setup() {
    ctx = UserRequestContextAccHistory.builder().build();
  }

  def "Empty context has no settled bets"() {
    expect:
    ctx.getSettledBets().isEmpty()
    !ctx.isBetSettled(betWithId("1"))
  }

  def "Bet can be added to settled"() {
    when:
    ctx.addSettledBets(["1", "2"])
    then:
    ctx.isBetSettled(betWithId("1"))
    ctx.isBetSettled(betWithId("2"))
    !ctx.isBetSettled(betWithId("3"))
    ctx.getSettledBets().size() == 2
  }

  def betWithId(String betId) {
    def bet = Mock(BetWithSelectionsModel)
    def betSummary = Mock(BetSummaryModel)
    bet.getOriginalBet() >> betSummary
    betSummary.getId() >> betId
    bet
  }
}
