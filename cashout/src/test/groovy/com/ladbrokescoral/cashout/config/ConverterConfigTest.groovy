package com.ladbrokescoral.cashout.config

import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer
import com.ladbrokescoral.cashout.model.Code
import com.ladbrokescoral.cashout.model.response.UpdateDto
import com.ladbrokescoral.cashout.model.response.CashoutData
import com.ladbrokescoral.cashout.model.response.ErrorCashout
import spock.lang.Specification
import spock.lang.Unroll

import java.util.function.Function

class ConverterConfigTest extends Specification {
  public static final String CASHOUT_UNAVAIL = "Cashout unavailable: This bet does not have cashout available"
  public static final String CASHOUT_SERVICE_FAILED = Code.OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR.toString()
  ConverterConfig config = new ConverterConfig()

  @Unroll
  def "When message=#message and status=#status and value=#value then cashoutValue=#cashoutValue and cashoutStatus=#cashoutStatus"() {
    expect:
    def offer = CashoutOffer.builder()
        .message(message)
        .cashoutOfferReqRef("123")
        .cashoutValue(value)
        .status(status)
        .build()
    CashoutData cashoutData = config.cashoutOfferToCashoutData().apply(offer)
    cashoutData.cashoutValue == cashoutValue
    cashoutData.cashoutStatus == cashoutStatus
    where:
    message              | status                 | value | cashoutValue | cashoutStatus
    "Something is wrong" | null                   | null  | null         | Code.OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR.toString()
    CASHOUT_UNAVAIL      | null                   | null  | null         | Code.CASHOUT_BET_NO_CASHOUT.toString()
    null                 | null                   | null  | null         | CASHOUT_SERVICE_FAILED
    null                 | null                   | 2.2   | "2.2"        | null
    null                 | CASHOUT_SERVICE_FAILED | null  | null         | CASHOUT_SERVICE_FAILED
  }

  def "If cashout value is present then normal betUpdate is returned"() {
    given:
    CashoutData cashoutData = CashoutData.builder()
        .cashoutValue("2.0")
        .build()
    when:
    UpdateDto betUpdate = config.cashoutDataToBetUpdate().apply(cashoutData)
    then:
    betUpdate.cashoutData == cashoutData
  }

  def "If cashout value is absent but status is bet_no_cashout then normal betUpdate is returned "() {
    given:
    def cashoutData = CashoutData.builder()
        .cashoutStatus(Code.CASHOUT_BET_NO_CASHOUT.toString())
        .build()
    when:
    def betUpdate = config.cashoutDataToBetUpdate().apply(cashoutData)
    then:
    betUpdate.cashoutData == cashoutData
  }

  def "if cashout value is absent then betUpdate with error is returned"() {
    given:
    def cashoutData = CashoutData.builder()
        .cashoutStatus("some error")
        .build()
    when:
    def betUpdate = config.cashoutDataToBetUpdate().apply(cashoutData)
    then:
    betUpdate.error == new ErrorCashout("some error")
  }

  def "Offer to BetUpdate"() {
    def f1 = Spy(Function)
    def f2 = Mock(Function)
    def offer = CashoutOffer.builder().build()
    def cashoutData = CashoutData.builder().build()
    def betUpdate = UpdateDto.builder().build()
    when:
    def result = config.cashoutOfferToBetUpdate(f1, f2).apply(offer)
    then:
    1 * f1.apply(offer) >> cashoutData
    1 * f2.apply(cashoutData) >> betUpdate
  }
}
