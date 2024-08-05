package com.ladbrokescoral.cashout.service

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Event
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Market
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part
import spock.lang.Specification

import java.time.Duration

class UserRequestContextBuilderTest extends Specification {

  def "Test bets are indexed"() {
    when:
    def builder = new UserRequestContextBuilder()
    def date = new Date()
    def bet1 = bet([leg(111, 1111, 11111)])
    def bet2 = bet([
      leg(222, 2221, 22211),
      leg(222, 2222, 22221),
      leg(333, 3331, 33311),
      leg(333, 3331, 33312),
      leg(111, 1111, 11111)
    ])
    def userReqCtx = builder.token("123")
        .username("test")
        .tokenExpiresIn(Duration.ofSeconds(10))
        .connectionDate(date)
        .userBets([
          bet1,
          bet2
        ])
        .build();
    def indexedData = userReqCtx.getIndexedData();
    then:
    //test wrappers created once for a leg and each event/market/selection has reference to single instance
    indexedData.getSelectionDataBySelectionId(11111).get().is(indexedData.getSelectionDataByMarketId(1111)[0])
    indexedData.getSelectionDataByMarketId(1111)[0].is(indexedData.getSelectionDataByEventId(111)[0])
    indexedData.getSelectionDataByEventId(111)[0].is(indexedData.getSelectionDataBySelectionId(11111).get())

    indexedData.getAllSelectionIds().size() == 5

    indexedData.getSelectionDataBySelectionId(11111).get().bets[0] == bet1
    indexedData.getSelectionDataBySelectionId(11111).get().bets[1] == bet2

    indexedData.getSelectionDataBySelectionId(22211).get().bets[0] == bet2
    indexedData.getSelectionDataBySelectionId(33311).get().bets[0] == bet2

    indexedData.getAllMarketIds().size() == 4

    indexedData.getSelectionDataByMarketId(1111).size() == 1
    indexedData.getSelectionDataByMarketId(1111)[0].bets[0] == bet1
    indexedData.getSelectionDataByMarketId(1111)[0].bets[1] == bet2
    indexedData.getSelectionDataByMarketId(3331).size() == 2
    indexedData.getSelectionDataByMarketId(3331)[0].bets[0] == bet2

    indexedData.getAllEventIds().size() == 3

    indexedData.getSelectionDataByEventId(111).size() == 1
    indexedData.getSelectionDataByEventId(111)[0].bets[0] == bet1
    indexedData.getSelectionDataByEventId(111)[0].bets[1] == bet2
    indexedData.getSelectionDataByEventId(222).size() == 2
    indexedData.getSelectionDataByEventId(222)[0].bets[0] == bet2

    userReqCtx.userBets == [bet1, bet2]
    userReqCtx.token == "123"
    userReqCtx.username == "test"
    userReqCtx.tokenExpiresIn == Duration.ofSeconds(10)
    userReqCtx.connectionDate == date
  }

  BetSummaryModel bet(List<Leg> legs) {
    def bet = new BetSummaryModel()
    bet.id = "123"
    bet.leg = legs
    return bet
  }

  Leg leg(int eventId, int marketId, int outcomeId) {
    def leg = new Leg()
    def part = new Part()
    def outcome = new Outcome()
    def event = new Event()
    event.id = eventId.toString()
    outcome.id = outcomeId.toString()
    outcome.event = event
    def market = new Market()
    market.id = marketId.toString()
    outcome.market = market
    part.outcome = [outcome]
    leg.part = [part]
    return leg
  }
}
