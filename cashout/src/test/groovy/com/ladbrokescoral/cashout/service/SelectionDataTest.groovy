package com.ladbrokescoral.cashout.service

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.*
import com.ladbrokescoral.cashout.model.ResultCode
import spock.lang.Specification
import spock.lang.Unroll

import static com.ladbrokescoral.cashout.model.ResultCode.HANDICAP
import static com.ladbrokescoral.cashout.model.ResultCode.LOSE
import static com.ladbrokescoral.cashout.model.ResultCode.PLACE
import static com.ladbrokescoral.cashout.model.ResultCode.UNSET
import static com.ladbrokescoral.cashout.model.ResultCode.VOID
import static com.ladbrokescoral.cashout.model.ResultCode.WIN
import static com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus.*

class SelectionDataTest extends Specification {

  def "test Lp price changed"() {
    when:
    def data = new SelectionData(1, 2, 3)
    then:
    !data.getLpPrice().isPresent()
    data.changeLpPrice(1, 2)
    !data.changeLpPrice(1, 2)
    data.changeLpPrice(3, 4)
    data.getLpPrice().isPresent()
  }

  def "test Sp price change"() {
    when:
    def data = new SelectionData(1, 2, 3)
    then:
    !data.getSpPrice().isPresent()
    data.changeSpPrice(1, 2)
    !data.changeSpPrice(1, 2)
    data.changeSpPrice(3, 4)
    data.getSpPrice().isPresent()
  }

  @Unroll
  def "When statuses[e=#eventActive,m=#marketActive,s=#selectionActive] then whole status=#selDataStatus and unknowns=#hasUnknownStatus"() {
    given:
    def data = new SelectionData(1, 2, 3)
    if (eventActive != null) {
      data.changeEventStatus(eventActive)
    }
    if (marketActive != null) {
      data.changeMarketStatus(marketActive)
    }
    if (selectionActive != null) {
      data.changeSelectionStatus(selectionActive)
    }
    data.changeLpPrice(1, 2)
    expect:
    data.getSelectionStatus() == selDataStatus
    data.hasUnknownStatusOrLpPrice() == hasUnknownStatus

    where:
    eventActive | marketActive | selectionActive | selDataStatus | hasUnknownStatus
    false       | false        | false           | SUSPENDED     | false
    true        | false        | false           | SUSPENDED     | false
    true        | true         | false           | SUSPENDED     | false
    false       | true         | false           | SUSPENDED     | false
    false       | true         | true            | SUSPENDED     | false
    false       | false        | true            | SUSPENDED     | false
    false       | null         | null            | SUSPENDED     | true
    false       | null         | false           | SUSPENDED     | true
    false       | false        | null            | SUSPENDED     | true
    null        | false        | null            | SUSPENDED     | true
    null        | false        | false           | SUSPENDED     | true
    true        | true         | true            | ACTIVE        | false
    null        | null         | null            | UNKNOWN       | true
    null        | null         | true            | UNKNOWN       | true
    null        | true         | true            | UNKNOWN       | true
    true        | null         | null            | UNKNOWN       | true
    true        | true         | null            | UNKNOWN       | true
  }

  def "When all statuses are known but LP price is not then hasUnknownStatusOrPrice is true"() {
    given:
    def data = new SelectionData(1, 2, 3)
    data.changeEventStatus(true)
    data.changeMarketStatus(true)
    data.changeSelectionStatus(true)
    expect:
    data.hasUnknownStatusOrLpPrice();
  }

  def "When all statuses are known and LP price is known then hasUnknownStatusOrPrice is false"() {
    given:
    def data = new SelectionData(1, 2, 3)
    data.changeEventStatus(true)
    data.changeMarketStatus(true)
    data.changeSelectionStatus(true)
    data.changeLpPrice(1, 2)
    expect:
    !data.hasUnknownStatusOrLpPrice();
  }

  def "Test SP and LP price change reflects update in bet's parts"() {
    def partWithSpPrice = part("S")
    def partWithLpPrice = part("L")
    when:
    def data = new SelectionData(null, [
      partWithSpPrice,
      partWithLpPrice
    ], 1, 2, 3)
    data.changeLpPrice(1, 2)
    then:
    partWithLpPrice.price[0].currentPriceNum == String.valueOf(1)
    partWithLpPrice.price[0].currentPriceDen == String.valueOf(2)

    partWithSpPrice.price[0].priceStartingNum == null
    partWithSpPrice.price[0].priceStartingDen == null

    when:
    data.changeSpPrice(3, 4)
    then:
    partWithSpPrice.price[0].priceStartingNum == String.valueOf(3)
    partWithSpPrice.price[0].priceStartingDen == String.valueOf(4)

    partWithLpPrice.price[0].currentPriceNum == String.valueOf(1)
    partWithLpPrice.price[0].currentPriceDen == String.valueOf(2)
  }

  @Unroll
  def "When initCode=#initCode updates with[code=updateResultCode;place=#updatePlaces; then part is set to [code=expectedResultCode;places=expectedPlaces] and selection resulted=#isResulted"() {
    given:
    def part3 = partWithResult(3, initCode)
    def data = new SelectionData(null, [part3], 1, 2, 3)

    data.updateResultCode(updateResultCode, updatePlaces)
    expect:
    part3.outcome[0].result.value == expectedResultCode
    part3.outcome[0].result.places == expectedPlaces

    where:
    initCode | updateResultCode   | updatePlaces | expectedPlaces | expectedResultCode | isResulted
    "-"      | WIN                | null         | null           | "W"                | true
    "-"      | WIN                | 2            | null           | "W"                | true
    "-"      | LOSE               | null         | null           | "L"                | true
    "-"      | HANDICAP           | null         | null           | "H"                | true
    "-"      | VOID               | null         | null           | "V"                | true
    "-"      | PLACE              | null         | null           | "P"                | true
    "-"      | PLACE              | 2            | "2"            | "P"                | true
    "W"      | UNSET              | null         | ""             | "-"                | false
    "P"      | UNSET              | null         | ""             | "-"                | false
    "-"      | ResultCode.UNKNOWN | null         | null           | "-"                | false
  }

  def "When P is unset then places is removed as well"() {
    when:
    def part3 = partWithResult(3, "P")
    part3.outcome[0].result.places = "2"
    def data = new SelectionData(null, [part3], 1, 2, 3)

    data.updateResultCode(UNSET, null)
    then:
    part3.outcome[0].result.places == ""
    part3.outcome[0].result.value == "-"
  }

  Part part(String priceType) {
    def part = new Part()
    def price = new Price()
    def code = new Code()
    code.code = priceType
    price.priceType = code
    part.price = [price]

    part
  }

  Part partWithResult(int selId, String resultCode) {
    def part = new Part()

    def outcome = new Outcome()
    outcome.id = String.valueOf(selId)
    def result = new ConfirmingResult()
    result.value = resultCode
    outcome.result = result
    part.outcome = [outcome]
    part
  }
}
