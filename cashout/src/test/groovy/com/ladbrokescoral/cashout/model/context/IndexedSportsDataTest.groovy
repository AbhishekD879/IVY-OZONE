package com.ladbrokescoral.cashout.model.context

import com.coral.bpp.api.model.bet.api.common.placeBetV2.PriceType
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.*
import com.ladbrokescoral.cashout.service.SelectionData
import spock.lang.Specification

class IndexedSportsDataTest extends Specification {

  def 'When no bets supplied, index is empty'() {
    when:
    def idx = IndexedSportsData.constructIndexedData(Collections.emptyList());
    then:
    idx.getAllEventIds().isEmpty()
    idx.getAllMarketIds().isEmpty()
    idx.getAllSelectionIds().isEmpty()
    idx.getBetsWithSelection(1).isEmpty()
    idx.getBetsWithMarketId(2).isEmpty()
    idx.getBetsWithEventId(3).isEmpty()
    idx.getSelectionDataByEventId(1).isEmpty()
    idx.getSelectionDataByMarketId(2).isEmpty()
    !idx.getSelectionDataBySelectionId(3).isPresent()
  }

  def 'Single bet'() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([[1, 2, 3]])
    ])
    then:
    idx.getAllEventIds().size() == 1
    idx.getAllMarketIds().size() == 1
    idx.getAllSelectionIds().size() == 1
    idx.getSelectionDataBySelectionId(3).isPresent()
    idx.getSelectionDataByMarketId(2).size() == 1
    idx.getSelectionDataByEventId(1).size() == 1

    marketHasSelection(idx, 2, 3)
    eventHasSelection(idx, 1, 3)
  }

  def "SelectionData created once"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([
        [1, 2, 3],
        // not real case I suppose
        [1, 2, 3]
      ])
    ])
    then:
    idx.getAllEventIds().size() == 1
    idx.getAllMarketIds().size() == 1
    idx.getAllSelectionIds().size() == 1
    idx.getSelectionDataBySelectionId(3).isPresent()
    idx.getSelectionDataByMarketId(2).size() == 1
    idx.getSelectionDataByEventId(1).size() == 1

    marketHasSelection(idx, 2, 3)
    eventHasSelection(idx, 1, 3)
  }

  def "Selection are grouped by market and event"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([
        [1, 2, 3],
        [1, 2, 4],
        [1, 3, 5],
        [22, 33, 44]
      ])
    ])
    then:
    idx.getAllSelectionIds().size() == 4
    idx.getAllMarketIds().size() == 3
    idx.getAllEventIds().size() == 2
  }

  def "SelectionData is created correctly"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([[1, 2, 3]])
    ])
    then:
    def selection = idx.getSelectionDataBySelectionId(3).get()
    selection.eventId == 1
    selection.marketId == 2
    selection.selectionId == 3
    selection.parts.size() == 1
    selection.bets.size() == 1
    selection.bets[0].leg[0].part[0].is(selection.parts[0])

    idx.getSelectionDataByMarketId(2)[0].is(selection)
    idx.getSelectionDataByEventId(1)[0].is(selection)
  }

  def "Two bets on same selection"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([[1, 2, 3]]),
      createBet([[1, 2, 3]])
    ])
    then:
    idx.getAllEventIds().size() == 1
    idx.getAllMarketIds().size() == 1
    idx.getAllSelectionIds().size() == 1
    idx.getSelectionDataBySelectionId(3).isPresent()
    idx.getSelectionDataByMarketId(2).size() == 1
    idx.getSelectionDataByEventId(1).size() == 1

    marketHasSelection(idx, 2, 3)
    eventHasSelection(idx, 1, 3)

    def selection = idx.getSelectionDataBySelectionId(3).get()
    selection.eventId == 1
    selection.marketId == 2
    selection.selectionId == 3
    selection.parts.size() == 2
    selection.bets.size() == 2
    selection.bets[0].leg[0].part[0].is(selection.parts[0])
    !selection.bets[0].is(selection.bets[1])

    idx.getSelectionDataByMarketId(2)[0].is(selection)
    idx.getSelectionDataByEventId(1)[0].is(selection)
  }

  def "Find other selections for single bet returns empty list"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([[1, 2, 3]])
    ])
    then:
    idx.getBetsWithSelection(3)[0].is(idx.getSelectionDataBySelectionId(3).get().bets[0])
    idx.findOtherSelectionsInBet(idx.getBetsWithSelection(3)[0], 3).isEmpty()
  }

  def "Find other selection for multiple returns all except provided id"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([
        [
          BigInteger.valueOf(1),
          BigInteger.valueOf(2),
          BigInteger.valueOf(3)
        ],
        [
          BigInteger.valueOf(4),
          BigInteger.valueOf(5),
          BigInteger.valueOf(6)
        ],
        [
          BigInteger.valueOf(7),
          BigInteger.valueOf(5),
          BigInteger.valueOf(9)
        ]
      ]),
      createBet([
        [
          BigInteger.valueOf(1),
          BigInteger.valueOf(2),
          BigInteger.valueOf(3)
        ],
        [
          BigInteger.valueOf(44),
          BigInteger.valueOf(55),
          BigInteger.valueOf(66)
        ]
      ])
    ])
    then:
    def bet1 = idx.getBetsWithSelection(BigInteger.valueOf(3))[0]
    def bet2 = idx.getBetsWithSelection(BigInteger.valueOf(3))[1]
    def otherSelectionsInBet1 = idx.findOtherSelectionsInBet(bet1, BigInteger.valueOf(3))
    otherSelectionsInBet1.size() == 2
    otherSelectionsInBet1.find { it.selectionId == 6 } != null
    otherSelectionsInBet1.find { it.selectionId == 9 } != null

    def otherSelectionsInBet2 = idx.findOtherSelectionsInBet(bet2, BigInteger.valueOf(3))
    otherSelectionsInBet2.size() == 1
    otherSelectionsInBet2.find { it.selectionId == 66 } != null
  }

  def "Event/market/selection is set to active when cashout value is present "() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setCashoutValue(createBet([[1, 2, 3]]), "2.0"),
      setCashoutValue(createBet([[1, 2, 3]]), "CASHOUT_SELN_SUSPENDED")
    ])
    then:
    idx.getSelectionDataBySelectionId(3).get().getSelectionStatus() == SelectionData.SelectionStatus.ACTIVE
  }

  def "Event/market/selction status is unknown when cashout value isn't present"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setCashoutValue(createBet([[1, 2, 3]]), "CASHOUT_SELN_SUSPENDED")
    ])
    def selection = idx.getSelectionDataBySelectionId(3).get()
    then:
    selection.getSelectionStatus() == SelectionData.SelectionStatus.UNKNOWN
  }

  def "Selection confirmed flag is set when at least one selection has confirm"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setConfirm(createBet([[1, 2, 3]]), 3, "-"),
      setConfirm(createBet([[1, 2, 3]]), 3, "Y"),
      setConfirm(createBet([[1, 2, 3]]), 3, "-")
    ])
    then:
    def selection = idx.getSelectionDataBySelectionId(3).get()
    selection.isConfirmed()
  }

  def "Selection confirmed flag isn't set when all selections aren't confirmed"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setConfirm(createBet([[1, 2, 3]]), 3, "-"),
      setConfirm(createBet([[1, 2, 3]]), 3, "-"),
      setConfirm(createBet([[1, 2, 3]]), 3, "-")
    ])
    then:
    def selection = idx.getSelectionDataBySelectionId(3).get()
    !selection.isConfirmed()
  }

  def "Selection marked as handicap when marketSort is MH"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setMarketSort(createBet([[1, 2, 3]]), 3, "-"),
      setMarketSort(createBet([[1, 2, 3]]), 3, "MH"),
      setMarketSort(createBet([[1, 2, 3]]), 3, "-")
    ])
    then:
    def selection = idx.getSelectionDataBySelectionId(3).get()
    selection.isHandicapMarket()
  }

  def "Selection marked as none handicap when marketSort is M"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      setMarketSort(createBet([[1, 2, 3]]), 3, "-"),
      setMarketSort(createBet([[1, 2, 3]]), 3, "-"),
      setMarketSort(createBet([[1, 2, 3]]), 3, "-")
    ])
    then:
    def selection = idx.getSelectionDataBySelectionId(3).get()
    !selection.isHandicapMarket()
  }

  def "Selection has only parts with its id"() {
    when:
    def idx = IndexedSportsData.constructIndexedData([
      createBet([[1, 2, 3]]),
      createBet([
        [1, 2, 3],
        [88, 77, 66],
        [1, 2, 7]
      ]),
      createBet([[4, 5, 6]])
    ])
    def parts = idx.getSelectionDataBySelectionId(3).get().getParts()
    then:
    parts.size() == 2
    parts.each {it.outcome[0].id == String.valueOf(3)}
  }

  def "when cashout value is Suspended "() {
    given:
    def idx = IndexedSportsData.constructIndexedData([
      setCashoutValue(createBet([[1, 2, 3]]), "CASHOUT_SELN_SUSPENDED")
    ])
    def bet1=idx.getBetsWithSelection(3)[0]
    def price=new Price()
    def code=new Code()
    code.setCode("L")
    price.setPriceType(code)
    def outcome=new Outcome()
    outcome.setId("3")
    bet1.setCashoutValue("CASHOUT_SELN_SUSPENDED")
    bet1.getLeg().get(0).getPart().get(0).setPrice([price])
    bet1.getLeg().get(0).getPart().get(0).setOutcome([outcome])
    when:
    def val= idx.getBetWithSelectionModels(3)
    then:
    val.size()==1
  }

  def "when cashout value is not Suspended "() {
    given:
    def idx = IndexedSportsData.constructIndexedData([
      setCashoutValue(createBet([[1, 2, 3]]), null)
    ])
    def bet1 = idx.getBetsWithSelection(3)[0]
    def price = new Price()
    def code = new Code()
    code.setCode("L")
    price.setPriceType(code)
    def outcome = new Outcome()
    outcome.setId("3")
    def idName = new IdName()
    idName.setId("123")
    outcome.setEventCategory(idName)
    bet1.setCashoutValue(null)
    bet1.getLeg().get(0).getPart().get(0).setPrice([price])
    bet1.getLeg().get(0).getPart().get(0).setOutcome([outcome])
    when:
    def val = idx.getBetWithSelectionModels(3)
    then:
    val.size() == 0
  }

  def "when cashout value is not Suspended AND HR Subscription"() {
    given:
    def idx = IndexedSportsData.constructIndexedData([
      setCashoutValue(createBet([[1, 2, 3]]), null)
    ])
    def bet1 = idx.getBetsWithSelection(3)[0]
    def price = new Price()
    def code = new Code()
    code.setCode("L")
    price.setPriceType(code)
    def outcome = new Outcome()
    outcome.setId("3")
    def idName = new IdName()
    idName.setId("21")
    outcome.setEventCategory(idName)
    bet1.setCashoutValue("CASHOUT_SELN_NO_CASHOUT")
    bet1.getLeg().get(0).getPart().get(0).setPrice([price])
    bet1.getLeg().get(0).getPart().get(0).setOutcome([outcome])
    when:
    def val = idx.getBetWithSelectionModels(3)
    then:
    val.size() == 1
  }

  private static boolean marketHasSelection(IndexedSportsData idx, int marketId, int selectionId) {
    def selcn = idx.getSelectionDataBySelectionId(selectionId).get()
    def selcnForMarket = idx.getSelectionDataByMarketId(marketId)
    return selcnForMarket.contains(selcn)
  }

  private static boolean eventHasSelection(IndexedSportsData idx, int eventId, int selectionId) {
    def selcn = idx.getSelectionDataBySelectionId(selectionId).get()
    def selcnForEvent = idx.getSelectionDataByEventId(eventId)
    return selcnForEvent.contains(selcn)
  }

  private static BetSummaryModel setCashoutValue(BetSummaryModel bet, String cashoutValue) {
    bet.setCashoutValue(cashoutValue)
    bet
  }

  private static BetSummaryModel setConfirm(BetSummaryModel bet, int selectionId, String confirmed) {
    def result = new ConfirmingResult()
    result.confirmed = confirmed;
    bet.leg.collectMany { it.part }
    .find { it.outcome[0].id == String.valueOf(selectionId) }
    .outcome[0].result = result

    bet
  }

  private static BetSummaryModel setMarketSort(BetSummaryModel bet, BigInteger selectionId, String code) {
    def result = new Code()
    result.setCode(code);
    bet.leg.collectMany { it.part }
    .find { it.outcome[0].id == String.valueOf(selectionId) }
    .outcome[0].market.setMarketSort(result)

    bet
  }

  private static BetSummaryModel createBet(List<List<BigInteger>> outcomes) {
    def bet = new BetSummaryModel()
    bet.leg = []

    outcomes.collect {
      def leg = new Leg()
      def part = new Part()
      def outcome = new Outcome()
      def event = new Event()
      event.id = it[0]
      def market = new Market()
      market.id = it[1]
      outcome.event = event
      outcome.market = market
      outcome.id = String.valueOf(it[2])
      part.outcome = [outcome]
      leg.part = [part]
      leg
    }.each {
      bet.leg.add(it)
    }
    bet
  }
}
