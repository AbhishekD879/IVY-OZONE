package com.ladbrokescoral.cashout.api.client.entity

import com.ladbrokescoral.cashout.TestUtil
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest
import spock.lang.Specification
import spock.lang.Unroll

class TestModels extends Specification {

  @Unroll
  def "#betTypeCashout cashout model test"() {

    expect:
    String inputJson = TestUtil.readFromFile("api/" + betTypeCashoutFilePath).replaceAll("\n", "").replaceAll(" ", "")
    CashoutRequest request = TestUtil.deserializeWithJackson("api/" + betTypeCashoutFilePath, CashoutRequest.class);
    CashoutRequest inputJsonRequest = TestUtil.serializeWithJackson(inputJson, CashoutRequest.class);
    inputJsonRequest == request

    where:
    betTypeCashout               | betTypeCashoutFilePath
    "SGL"                        | "body-SGL.json"
    "TBL"                        | "body-TBL.json"
    "TBL-with-resulted-legs"     | "body-TBL-with-resulted-legs.json"
    "Multiple"                   | "body-Multiple.json"
    "DBL-bet-missing-parameters" | "body-DBL-bet-missing-parameters.json"
    "DBL-bet-with-a-losing-leg"  | "body-DBL-bet-with-a-losing-leg.json"
    "with-free-bets"             | "body-with-free-bets.json"
    "Horse-racing-ACC5"          | "body-Horse-racing-ACC5.json"
  }
}
