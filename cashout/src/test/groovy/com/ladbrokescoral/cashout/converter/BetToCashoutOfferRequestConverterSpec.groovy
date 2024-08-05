package com.ladbrokescoral.cashout.converter

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel
import com.ladbrokescoral.cashout.TestUtil
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest
import spock.lang.Specification
import spock.lang.Unroll

class BetToCashoutOfferRequestConverterSpec extends Specification {

  BetToCashoutOfferRequestConverter converter

  def setup() {
    converter = new BetToCashoutOfferRequestConverter()
  }

  @Unroll
  def "converting OpenBet #betJson to cashoutOffer request object for OpenBet cashout service v4"() {

    expect:
    List<BetSummaryModel> bets = TestUtil.deserializeListWithJackson("converter/cashoutoffer/accountHistory/" + betJson, BetSummaryModel.class)
    CashoutRequest expectedResult = TestUtil.deserializeWithJackson("converter/cashoutoffer/" + cashoutOfferJson, CashoutRequest.class)

    CashoutRequest result = converter.convert(bets)

    result == expectedResult

    where:
    betJson                          | cashoutOfferJson
    "singleBet.json"                 | "singleBetCashoutOffer.json"
    "singleBetWithUpdatedPrice.json" | "singleBetWithUpdatedPriceCashoutOffer.json"
    //    "handicapBet.json"               | "handicapBetCashoutOffer.json"
    "eachWayBet.json"                | "eachWayBetCashoutOffer.json"
    "startPriceBet.json"             | "startPriceBetCashoutOffer.json"
    "deductionBet.json"              | "deductionBetCashoutOffer.json"
    "noDeductionBet.json"            | "noDeductionBetCashoutOffer.json"
    "doubleBetWithSpPrice.json"      | "doubleBetWithSpPriceCashoutOffer.json"
    "ACC4.json"                      | "ACC4CashoutOffer.json"
  }
}
