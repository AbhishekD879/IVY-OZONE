package com.ladbrokescoral.cashout.service.updates

import com.coral.bpp.api.model.bet.api.oxi.CashoutLadder
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.*
import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter
import com.ladbrokescoral.cashout.model.context.IndexedSportsData
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory
import com.ladbrokescoral.cashout.service.SelectionData
import com.ladbrokescoral.cashout.payout.PayoutService
import com.ladbrokescoral.cashout.payout.helper.PayoutServiceRequest
import spock.lang.Specification

class UpdateProcessorsSpec extends Specification {
  protected UserRequestContextAccHistory userReqCtx = Mock(UserRequestContextAccHistory)
  protected IndexedSportsData indexedData
  protected BetToCashoutOfferRequestConverter converter = new BetToCashoutOfferRequestConverter()

  protected static UserRequestContextAccHistory createCtxWithBets(List<BetSummaryModel> bets) {
    return UserRequestContextAccHistory.builder()
        .userBets(bets)
        .connectionDate(new Date())
        .token("123")
        .build()
  }

  void setup() {
    indexedData = Mock(IndexedSportsData)
    def bet1 = bet("1", [["111", "222", "333"]])
    def bet2 = bet("2", [["111", "222", "333"]])
    def bet3 = bet("3", [["123", "222", "999"]])

    def selectionData = new SelectionData(1, 1, 1)

    indexedData.getBetsWithEventId(111) >> [bet1, bet2]
    indexedData.getBetsWithEventId(123) >> [bet3]

    indexedData.getBetsWithMarketId(222) >> [bet1, bet2]
    indexedData.getBetsWithMarketId(123) >> [bet3]

    indexedData.getSelectionDataByEventId(111) >> [selectionData]

    userReqCtx.getToken() >> "123"
    userReqCtx.getUserBets() >> [bet1, bet2, bet3]
    userReqCtx.getIndexedData() >> indexedData
    userReqCtx.isBetSettled(_) >> false
    userReqCtx.getConnectionDate() >> new Date()
  }

  def legWithPrice(String selectionId, String strikePriceNum, String strikePriceDen) {
    legWithPrice(selectionId, strikePriceNum, strikePriceDen, "L")
  }
  def legWithPriceS(String selectionId, String strikePriceNum, String strikePriceDen) {
    legWithPrice(selectionId, strikePriceNum, strikePriceDen, "S")
  }
  def legWithPricenull(String selectionId, String strikePriceNum, String strikePriceDen) {
    legWithPrice(selectionId, strikePriceNum, strikePriceDen, "")
  }
  def legWithPrice(String selectionId, String strikePriceNum, String strikePriceDen, String priceType) {
    def leg = new Leg()
    def betType = new BetType()
    betType.code = "Whatever"
    leg.legType = betType
    leg.legSort = betType
    def part = new Part()
    def outcome = new Outcome()
    outcome.id = selectionId
    def event = new Event()
    event.id = selectionId + "11"
    event.flags = "RVA,AVD"
    outcome.event = event
    def market = new Market()
    market.id = selectionId + "22"
    outcome.market = market
    def eventCategory = new IdName()
    eventCategory.id=event.id
    outcome.eventCategory=eventCategory
    def result = new ConfirmingResult()
    result.value = "-"
    outcome.result = result
    part.outcome = [outcome]
    def price = new Price()
    //price with which user made the bet
    if (priceType == "S") {
      price.priceStartingNum = strikePriceNum
      price.priceStartingDen = strikePriceDen
    } else if (priceType == "L") {
      price.priceNum = strikePriceNum
      price.priceDen = strikePriceDen
    }
    def code = new Code()
    code.code = priceType
    price.priceType = code
    part.price = [price]
    def ladder = new CashoutLadder()
    ladder.value = "STABLE"
    ladder.type = "2.0"
    part.cashoutLadder = ladder
    leg.part = [part]
    leg
  }

  BetSummaryModel bet(String betId, List<List<String>> hierarchy) {
    bet(betId, hierarchy, "L")
  }

  BetSummaryModel bet(String betId, List<List<String>> hierarchy, String priceType) {
    def bet = new BetSummaryModel()
    def stake = new Stake()
    stake.value = "1.0"
    bet.cashoutValue = "5.6"
    bet.cashoutProfile="NO_LOSS"
    bet.stake = stake
    bet.id = betId
    def type = new BetType()
    type.code = "SGL"
    bet.betType = type

    def legs = hierarchy.collect {
      def leg = legWithPrice(it[2], "3", "4", priceType)
      leg.part[0].outcome[0].market.id = it[1]
      leg.part[0].outcome[0].event.id = it[0]
      leg.part[0].outcome[0].eventCategory.id = it[0]
      leg.part[0].price[0].priceStartingNum = "1"
      leg.part[0].price[0].priceStartingDen = "2"
      leg
    }

    bet.leg = legs
    return bet
  }
}
