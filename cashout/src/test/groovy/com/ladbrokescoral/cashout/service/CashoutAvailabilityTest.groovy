package com.ladbrokescoral.cashout.service

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Market
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part
import com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus
import spock.lang.Specification

import static com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus.*

class CashoutAvailabilityTest extends Specification {
  private selectionWithUnknownPrice
  void setup() {
    selectionWithUnknownPrice = mockSelection(SUSPENDED, false, Optional.empty(),"Match_betting")
  }

  def "When selection in single bet is active then cashout is available"() {
    given:
    def selection = selectionWithStatus(ACTIVE)
    BetWithSelectionsModel bet = betWithSelections([selection])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.YES
  }

  def "Banach bet has unknown cashout status always"() {
    given:
    BetWithSelectionsModel bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE)
    ])
    bet.banachBet = true;
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN
  }

  def "When all selections in bet are active then cashout is available"() {
    given:

    BetWithSelectionsModel bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.YES
  }

  def "When at least one selection status is Unknown then cashout status in unknown as well"() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(UNKNOWN),
      selectionWithStatus(ACTIVE)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN
  }

  def "When at least one selection in bet is suspended then cashout isn't available"() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(SUSPENDED),
      selectionWithStatus(ACTIVE)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.NO
  }

  def "When one selection is confirmed and suspended and others are active then cashout status is available"() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      confirmedSelectionWithStatus()
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.YES
  }

  def "When all legs are confirmed then cashout status is no_confirmed"() {
    given:
    def bet = betWithSelections([
      confirmedSelectionWithStatus(),
      confirmedSelectionWithStatus(),
      confirmedSelectionWithStatus()
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.NO_CONFIRMED
  }

  def "When one handicap selection is confirmed and suspended and others are active then cashout status is unknown"() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      confirmedHandicapSelection()
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN
  }

  def "When one selection is suspended and price is unknown then cashout availability is unknown"() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      this.selectionWithUnknownPrice
    ])

    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN_UNCOMPETITIVE
  }

  def 'When one selection has uncompetitive price then cashout availability is unknown even if selection is suspended'() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePrice(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN_UNCOMPETITIVE
  }

  def 'Unknown has bigger priority then unknown_uncompetitve'() {
    given:
    def bet = betWithSelections([
      selectionWithStatus(UNKNOWN),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePrice(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN
  }

  def 'When one confirmed and one uncompetitive and suspended then unknown_uncompetitve'() {
    given:
    def bet = betWithSelections([
      confirmedSelectionWithStatus(),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePrice(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,null)
    then:
    availability == CashoutAvailability.UNKNOWN_UNCOMPETITIVE
  }
  def 'Selction UnKnownUncompetative When 2 upmarket is Suspended'() {
    given:
    selectionWithUnknownPrice = mockSelection(SUSPENDED, false, Optional.empty(),"Coral2up")
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePriceWith2upMarket(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,Arrays.asList("Coral2up,Lad2up".split(",")))
    then:
    availability == CashoutAvailability.UNKNOWN_UNCOMPETITIVE
  }

  def 'Selction UnKnownUncompetative When Other market is Suspended'() {
    given:
    selectionWithUnknownPrice = mockSelection(SUSPENDED, false, Optional.empty(),"Coral2up")
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePriceWithOtherMARKET(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,Arrays.asList("Coral2up,Lad2up".split(",")))
    then:
    availability == CashoutAvailability.NO
  }

  def 'Selction confirmed is true When Other market is Suspended'() {
    given:
    selectionWithUnknownPrice = mockSelection(SUSPENDED, false, Optional.empty(),"Coral2up")
    def bet = betWithSelections([
      selectionWithStatus(ACTIVE),
      selectionWithStatus(ACTIVE),
      selectionWithUncompetitivePricefasleWithOtherMARKET(SUSPENDED)
    ])
    when:
    CashoutAvailability availability = CashoutAvailability.calculateCashoutAvailability(bet,Arrays.asList("Coral2up,Lad2up".split(",")))
    then:
    availability == CashoutAvailability.YES
  }



  private static BetWithSelectionsModel betWithSelections(List<BetWithSelectionsModel.SelectionDataLeg> selections) {
    BetWithSelectionsModel.builder()
        .legs(selections)
        .build()
  }

  def selectionWithStatus(SelectionStatus selectionStatus) {
    mockSelection(selectionStatus, false, true)
  }

  def confirmedSelectionWithStatus() {
    mockSelection(SUSPENDED, true, true)
  }

  def confirmedHandicapSelection() {
    mockSelection(SUSPENDED, true, true, true)
  }
  def selectionWithUncompetitivePriceWith2upMarket(SelectionStatus selectionStatus) {
    mock2upMarketSelection(selectionStatus, false, true)
  }
  def selectionWithUncompetitivePriceWithOtherMARKET(SelectionStatus selectionStatus) {
    mockSelection(selectionStatus, false, true)
  }

  def selectionWithUncompetitivePricefasleWithOtherMARKET(SelectionStatus selectionStatus) {
    mockSelection(selectionStatus, true, false)
  }
  def selectionWithUncompetitivePrice(SelectionStatus selectionStatus) {
    mockSelection(selectionStatus, false, false)
  }

  def mockSelection(SelectionStatus status, boolean isConfirmed, boolean isCompetitivePrice, boolean handicap = false) {
    def price = Mock(SelectionDataPrice)
    price.isCompetitive() >> isCompetitivePrice
    mockSelection(status, isConfirmed, handicap, Optional.of(price),"Match_betting")
  }

  def mock2upMarketSelection(SelectionStatus status, boolean isConfirmed, boolean isCompetitivePrice, boolean handicap = false) {
    def price = Mock(SelectionDataPrice)
    price.isCompetitive() >> isCompetitivePrice
    mockSelection(status, isConfirmed, handicap, Optional.of(price),"Coral2up")
  }

  def mockSelection(SelectionStatus status, boolean isConfirmed, boolean handicap = false, Optional<SelectionDataPrice> price,String marketName) {
    def legMock = Mock(BetWithSelectionsModel.SelectionDataLeg)
    def selectionMock = Mock(SelectionData)
    selectionMock.getSelectionStatus() >> status
    selectionMock.isConfirmed() >> isConfirmed
    selectionMock.isHandicapMarket() >> handicap
    selectionMock.getParts()>>getParts(marketName)
    legMock.getSelectionData() >> selectionMock
    legMock.getLegPrice() >> price
    legMock
  }

  List<Part> getParts(String marketName){
    List<Part> parts =new ArrayList<>()

    Market market=new Market()
    market.name=marketName;

    Outcome outcome=new Outcome()
    outcome.market=market;

    List<Outcome> outcomes=new ArrayList<>()
    outcomes.add(outcome)
    Part pat=new Part()
    pat.outcome=outcomes
    parts.add(pat)
    return parts
  }
}
