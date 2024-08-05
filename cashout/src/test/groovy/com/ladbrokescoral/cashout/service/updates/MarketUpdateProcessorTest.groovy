package com.ladbrokescoral.cashout.service.updates

import com.ladbrokescoral.cashout.model.context.SelectionPrice
import com.ladbrokescoral.cashout.model.safbaf.Market
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository
import com.ladbrokescoral.cashout.service.SelectionData
import reactor.core.publisher.Mono
import reactor.core.scheduler.Schedulers

class MarketUpdateProcessorTest extends UpdateProcessorsSpec {
  private UserUpdateTrigger suspensionTrigger = Mock(UserUpdateTrigger)
  private SelectionPriceRepository priceRepo = Mock(SelectionPriceRepository)
  private CashoutService cashoutOfferService=Mock(CashoutService)
  private SelectionDataAwareUpdateProcessor<Market> processor = new SelectionDataAwareUpdateProcessor<>(
  new MarketUpdateApplier(),
  suspensionTrigger,
  priceRepo,
  converter,
  2,
  cashoutOfferService
  )
  private UpdateProcessor<Market> marketUpdateProcessor = new MarketUpdateProcessor(processor)

  @Override
  void setup() {
    def prices = [
      new SelectionPrice("444", "5", "10")
    ]
    processor.setAfterPriceUpdateExecutor(Schedulers.immediate())
    priceRepo.multiGet(_) >> Mono.fromSupplier({prices})
    .subscribeOn(Schedulers.immediate())
  }

  def "Expect getBetDetail requested"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["222", "333", "444"]]),
      bet("2", [["222", "333", "555"]])
    ])
    userReqCtx.indexedData.getSelectionDataBySelectionId(555).get().changeLpPrice(1, 2)
    when:
    marketUpdateProcessor.process(userReqCtx, market)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    market << [
      marketWithHandicap(2.0, null),
      marketWithHandicap(null, 2.0),
      marketWithHandicap(2.0, 2.0),
    ]
  }

  def "Expect not getBetDetail requested"() {
    marketUpdateProcessor.process(userReqCtx, market)

    where:
    market << [
      market(333),
      new Market()
    ]
  }

  def "Expect no betDetail calls in case bet settled"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["222", "333", "444"]])
    ])
    userReqCtx.addSettledBets(["1"])
    when:
    marketUpdateProcessor.process(userReqCtx, market)

    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    market << [
      marketWithStatus(333, "Active", null),
      marketWithStatus(333, "Suspended", null)
    ]
  }

  def "When market is suspended then suspension is triggered for all bets where market's selections have competitive price and not resulted"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("212", [["222", "333", "444"]])
    ])
    def sel444 = userReqCtx.indexedData.getSelectionDataBySelectionId(444).get()

    sel444.changeLpPrice(1, 2)
    sel444.setEventActive(true)
    sel444.setMarketActive(true)
    sel444.setSelectionActive(true)

    when:
    marketUpdateProcessor.process(userReqCtx, marketWithStatus(333, "Suspended", null))
    then:
    sel444.getSelectionStatus() == SelectionData.SelectionStatus.SUSPENDED
  }

  def "When bet is already suspended then suspension of market doesn't trigger suspension"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("212", [["222", "333", "444"]])
    ])
    def sel444 = userReqCtx.indexedData.getSelectionDataBySelectionId(444).get()
    sel444.changeLpPrice(1, 2)
    sel444.setEventActive(true)
    sel444.setMarketActive(true)
    sel444.setSelectionActive(false)
    when:
    marketUpdateProcessor.process(userReqCtx, marketWithStatus(333, "Suspended", null))
    then:

    sel444.getSelectionStatus() == SelectionData.SelectionStatus.SUSPENDED
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def marketWithHandicap(Double handicapValue, Double handicapMakeup) {
    def market = market(333)
    market.handicapValue = handicapValue
    market.handicapMakeup = handicapMakeup
    return market
  }

  def marketWithStatus(int marketId, String status, String displayStatus) {
    def market = market(marketId)
    market.marketStatus = status
    return market
  }

  def market(int marketId) {
    def market = new Market()
    market.marketKey = marketId
    return market
  }
}
