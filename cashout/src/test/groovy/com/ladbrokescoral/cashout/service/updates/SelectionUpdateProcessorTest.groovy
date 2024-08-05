package com.ladbrokescoral.cashout.service.updates

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest
import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetType
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Stake
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet
import com.ladbrokescoral.cashout.api.client.RemoteCashoutApi
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer
import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter
import com.ladbrokescoral.cashout.model.context.SelectionPrice
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse
import com.ladbrokescoral.cashout.model.response.UpdateDto
import com.ladbrokescoral.cashout.service.BetDetailMeta
import com.ladbrokescoral.cashout.service.BppService;
import com.ladbrokescoral.cashout.model.safbaf.DeadHeat
import com.ladbrokescoral.cashout.model.safbaf.Meta
import com.ladbrokescoral.cashout.model.safbaf.Price
import com.ladbrokescoral.cashout.model.safbaf.Prices
import com.ladbrokescoral.cashout.model.safbaf.Rule4
import com.ladbrokescoral.cashout.model.safbaf.Selection
import com.ladbrokescoral.cashout.payout.PayoutUpdatesPublisher
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository
import org.springframework.test.util.ReflectionTestUtils
import reactor.core.publisher.Mono
import reactor.core.scheduler.Schedulers
import spock.lang.Unroll

import java.time.Duration
import java.util.function.Function

class SelectionUpdateProcessorTest extends UpdateProcessorsSpec {

  private SelectionPriceRepository priceRepository = Mock(SelectionPriceRepository)
  private UserUpdateTrigger suspensionTrigger = Mock(UserUpdateTrigger)
  private PayoutUpdatesPublisher payoutUpdatesPublisher = Mock(PayoutUpdatesPublisher)
  private TwoUpUpdatesPublisher twoUpUpdatesPublisher = Mock(TwoUpUpdatesPublisher)
  private RemoteCashoutApi remoteCashoutApi=Mock(RemoteCashoutApi)
  private Function<CashoutOffer, UpdateDto> function=Mock(Function)
  private BetUpdatesTopic betUpdatesTopic = Mock(BetUpdatesTopic)
  private AsyncCashoutOfferService asyncCashoutOfferService = Mock(AsyncCashoutOfferService);
  private AsyncBetDetailService asyncBetDetailService = Mock(AsyncBetDetailService);
  private BppService bppService = new BppService() {
    @Override
    Mono<List<Bet>> getBetDetail(GetBetDetailRequest getBetDetailRequest) {
      return Mono.empty()
    }

    @Override
    Mono<InitialAccountHistoryBetResponse> accountHistory(AccountHistoryRequest accountHistoryRequest) {
      return null
    }

    @Override
    Mono<List<BetSummaryModel>> accountHistoryOpenBets(AccountHistoryRequest accountHistoryRequest) {
      return null
    }
  }
  private BetToCashoutOfferRequestConverter betToCashoutOfferRequestConverter=new BetToCashoutOfferRequestConverter()
  private CashoutService cashoutOfferService
  private SelectionDataAwareUpdateProcessor<Selection> processor
  private UpdateProcessor<Selection> selectionUpdateProcessor

  @Override
  def setup() {
    cashoutOfferService =new CashoutService(betToCashoutOfferRequestConverter,remoteCashoutApi,function,betUpdatesTopic,bppService, asyncCashoutOfferService, asyncBetDetailService)
    processor = new SelectionDataAwareUpdateProcessor<>(
        new SelectionUpdateApplier(),
        suspensionTrigger,
        priceRepository,
        converter,
        2,
        cashoutOfferService
        )
    selectionUpdateProcessor = new SelectionUpdateProcessor(processor,payoutUpdatesPublisher, twoUpUpdatesPublisher)

    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]]),
      bet("2", [["111", "222", "333"]]),
      bet("3", [["111", "222", "123"]]),
      bet("4", [
        ["111", "444", "4441"],
        ["111", "222", "4442"]
      ])
    ])
    processor.setAfterPriceUpdateExecutor(Schedulers.immediate())

    priceRepository.get(_) >> Mono.fromSupplier({ new SelectionPrice(null, "5", "10") })
    .subscribeOn(Schedulers.immediate())


    priceRepository.multiGet(_) >> Mono.empty()
  }

  def "When activation is received but event or market is suspended then nothing happens"() {
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    def selUpdate = selectionWithStatus("Active", null, null)
    def sel333 = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    sel333.changeEventStatus(false)
    sel333.changeMarketStatus(true)
    sel333.changeSelectionStatus(false)
    sel333.changeLpPrice(1, 2)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "When Selection Key is not present"() {
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    Selection selection = new Selection()
    Rule4 rule4 = new Rule4()
    rule4.setRule4Id(1234)
    rule4.setDeduction(2.3)
    Meta meta = new Meta()
    meta.setParents("c.21:cl.223:t.1892:e.3394569:m.49350814")
    selection.setMeta(meta)
    selection.setRule4(rule4)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "When Selection Key is not present AND Rule4 is not present"() {
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    Selection selection = new Selection()
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "When activation is received"() {
    given:
    DeadHeat deadHeat=new DeadHeat()
    deadHeat.setDeadHeatKey("123")
    deadHeat.setWinDen(2)
    deadHeat.setWinNum(1)
    def selUpdate = selectionWithStatusDeadHeat("Active", null, null,deadHeat)
    def sel333 = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    sel333.changeEventStatus(false)
    sel333.changeMarketStatus(true)
    sel333.changeSelectionStatus(false)
    sel333.changeLpPrice(1, 2)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "When selection is suspended or unknown then price change shouldn't trigger cashout offer update"() {
    def bet1 = bet("1", [["111", "222", "333"]])
    bet1.cashoutValue = "CASHOUT_SELN_SUSPENDED"
    given:
    userReqCtx = createCtxWithBets([bet1])
    def selUpdate = selectionWithPrice(333, ["LP"], 3, 4)
    def sel333 = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    sel333.changeEventStatus(true)
    sel333.changeMarketStatus(true)
    if (selActive != null) {
      sel333.changeSelectionStatus(selActive)
    }
    sel333.changeLpPrice(1, 2)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    interaction {
      0 * suspensionTrigger.triggerCashoutSuspension(_)
    }
    where:
    selActive << [false]
  }

  def "If selection is activated but price is unknown then cashoutOffer is requested anyway"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]])
    ])
    userReqCtx.indexedData.getSelectionDataBySelectionId(333).get()
        .changeSelectionStatus(false)
    List<CashoutOfferRequest> cashoutOfferRequests=new ArrayList<>();
    CashoutOfferRequest cashoutOfferRequest= CashoutOfferRequest.builder().cashoutOfferReqRef("123").build()
    cashoutOfferRequests.add(cashoutOfferRequest)
    CashoutRequest cashoutRequest=CashoutRequest.builder().cashoutOfferRequests(cashoutOfferRequests) .shouldActivate(false).build()
    converter.convert(any()) >> cashoutRequest
    def selUpdate = selectionWithStatus("Active", null, null)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "When selection is activated but other selection in bet has unknown price then cashoutOffer is requested anyway"() {
    def bet = trebbleBetWithAllPricesInContext()
    bet.cashoutValue = "2.1"
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    List<CashoutOfferRequest> cashoutOfferRequests=new ArrayList<>();
    CashoutOfferRequest cashoutOfferRequest=CashoutOfferRequest.builder().cashoutOfferReqRef("123").build()
    cashoutOfferRequests.add(cashoutOfferRequest)
    CashoutRequest cashoutRequest=CashoutRequest.builder().cashoutOfferRequests(cashoutOfferRequests).shouldActivate(true).build()
    converter.convert(any()) >> cashoutRequest
    userReqCtx = createCtxWithBets([bet])
    def sel102 = userReqCtx.indexedData.getSelectionDataBySelectionId(102).get()
    sel102.changeSelectionStatus(false)
    sel102.changeLpPrice(1, 2)
    def selUpdate = selectionWithStatus("Active", null, null)
    selUpdate.selectionKey = 102
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "Suspension of multiple where other selection has unknown price"() {
    given: "Active bet with 3 selections"
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    def bet = trebbleBetWithAllPricesInContext()
    def prices = [
      new SelectionPrice("101", "1", "2"),
      new SelectionPrice("103", "2", "3")
    ]
    bet.cashoutValue = "2.1"
    userReqCtx = createCtxWithBets([bet])
    def selUpdate = selectionWithStatus("Suspended", null, null)
    selUpdate.selectionKey = 102
    when: "One selection is suspended but prices are unknown"
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then: "Then prices are fetched and if they are unknown then getBetDetail requested"
    1 * priceRepository.multiGet({ it.size() == 3 && it.containsAll(["101", "102", "103"]) }) >>
    Mono.fromSupplier({ prices })
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "When suspended selection price becomes uncompetitive then getBetDetail is requested"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]])
    ])
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    def sel333 = userReqCtx.indexedData.getSelectionDataBySelectionId(333).get()
    sel333.changeLpPrice(1, 2)
    sel333.setSelectionActive(false)
    when:
    selectionUpdateProcessor.process(userReqCtx, selectionWithPrice(333, ["LP"], 1, 100))
    then:
    0 * priceRepository.multiGet(_);

    when:
    selectionUpdateProcessor.process(userReqCtx, selectionWithPrice(333, ["LP"], 1, 101))
    then:
    0 * priceRepository.multiGet(_);

    when:
    selectionUpdateProcessor.process(userReqCtx, selectionWithPrice(333, ["LP"], 1, 99))

    then:
    0 * priceRepository.multiGet(_);
  }

  def "When suspended selection price becomes competitive then suspension is triggered"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]])
    ])
    def sel333 = userReqCtx.indexedData.getSelectionDataBySelectionId(333).get()
    sel333.changeLpPrice(1, 100)
    sel333.setSelectionActive(false)
    when:
    selectionUpdateProcessor.process(userReqCtx, selectionWithPrice(333, ["LP"], 1, 2))
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  //  def "When selection is suspended and some other selection's price is unknown then it's fetched from redis and bet is suspended"() {
  //    given:
  //    def bet = trebbleBetWithAllPricesInContext()
  //    userReqCtx = createCtxWithBets([bet])
  //    bet.cashoutValue = "2.1"
  //    def sel102 = userReqCtx.indexedData.getSelectionDataBySelectionId(102).get()
  //    sel102.changeLpPrice(1, 2)
  //    def selUpdate = selectionWithStatus("Suspend", null, null, null)
  //    selUpdate.selectionKey = 102
  //    def prices = [new SelectionPrice("101", "5", "6"),
  //                  new SelectionPrice("103", "7", "8")]
  //    when:
  //    selectionUpdateProcessor.process(userReqCtx, selUpdate)
  //    then:
  //
  //    1 * priceRepository.multiGet({it.size() == 2 && it.contains("101") && it.contains("103")}) >>
  //        Mono.fromSupplier({prices})
  //    1 * suspensionTrigger.triggerCashoutSuspension(_)
  //    0 * asyncGetBetDetailService.acceptBetDetailRequest(_)
  //    0 * asyncCashoutOfferService.acceptCashoutOfferRequest(_)
  //  }

  /* def "If suspend received for selection with unknwon price then it's fetch from redis"() {
   given:
   userReqCtx = createCtxWithBets([
   bet("1", ["111", "222", "333"])
   ])
   def selUpdate = selectionWithStatus("Suspended", null, null)
   def prices = [
   new SelectionPrice("333", "1", "2")
   ]
   when:
   selectionUpdateProcessor.process(userReqCtx, selUpdate)
   then:
   1 * priceRepository.multiGet(_) >> Mono.fromSupplier({ prices })
   .subscribeOn(Schedulers.immediate())
   userReqCtx.indexedData.getSelectionDataBySelectionId(333).get().getLpPrice().get() == new SelectionDataPrice(1, 2)
   0 * asyncGetBetDetailService.acceptBetDetailRequest(_)
   1 * suspensionTrigger.triggerCashoutSuspension(_)
   }*/

  def "When selection was activated and cashout is available then cashout offer is requested"() {
    given:
    def selUpdate = selectionWithStatus("Active", null, null)
    def sel333 = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    sel333.eventActive = true
    sel333.marketActive = true
    sel333.selectionActive = false
    sel333.changeLpPrice(1, 2)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * priceRepository.multiGet(_);
  }

  @Unroll
  def "When saf result #safResultCode received then bet is updated to #betResultCode and selection resulted=#selResulted"() {
    given:
    def selection = selectionWithStatus("S", null, safResultCode)
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get();
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
    selData.parts.each {
      assert it.outcome[0].result.value == betResultCode

    }
    where:
    safResultCode     | betResultCode | selResulted
    "Win"             | "W"           | true
    "Lose"            | "L"           | true
    "Unset"           | "-"           | false
    "Handicap"        | "H"           | true
    "Place"           | "P"           | true
    "Void"            | "V"           | true
    "SomethingUknown" | "-"           | false // unchanged
  }

  def "When saf confirmed received for non handicap market then bet is updated to resultConfirmed"() {
    given:
    def selection = selection(4441)
    selection.setIsResultConfirmed(true)
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(4441).get();
    selData.setSelectionActive(false) // selection gets suspended on result update before confirmation
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
    selData.isConfirmed()
  }

  def "When saf confirmed received for handicap market  then bet is updated to resultConfirmed"() {
    given:
    def selection = selection(4441)
    selection.setIsResultConfirmed(true)
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(4441).get();
    selData.setHandicapMarket(true)
    selData.setSelectionActive(false) // selection gets suspended on result update before confirmation
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
    selData.isConfirmed()
  }

  def "When single bet selection is confirmed then bet isn't available for cashout"() {
    given:
    def selection = selection(123)
    selection.setIsResultConfirmed(true)
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(123).get();
    selData.setSelectionActive(false)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerBetSettled(_)
  }

  def "When multiple bet has all selections confirmed then bet isn't available for cashout"() {
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    def selection = selection(4442)
    selection.setIsResultConfirmed(true)
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(4441).get();
    selData.setSelectionActive(false)
    selData.setConfirmed(true)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "If bet has all legs confirmed then updates are ignored for it"() {
    given:
    def selection = selectionWithPrice(4442, ["LP"], 3, 4)
    userReqCtx.getIndexedData().getSelectionDataBySelectionId(4441).get().setConfirmed(true)
    userReqCtx.getIndexedData().getSelectionDataBySelectionId(4442).get().setConfirmed(true)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerBetSettled(_)
  }

  def "When saf resulted received without status then bet is updated only"() {
    given:
    def selection = selection(333)
    selection.setResultCode("Win")
    selection.correctScoreAway="1"
    selection.correctScoreHome="2"
    selection.selectionName="|Clement Tabur (FRA)|"
    selection.finalPosition=1
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get();
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
    selData.parts.each {
      assert it.outcome[0].result.value == "W"
    }
  }

  def "When Place result is received then place is updated as well"() {
    given:
    def selection = selectionWithStatus("S", null, "Place")
    selection.place = 2
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get();
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    selData.parts.each {
      assert it.outcome[0].result.value == "P"
      assert it.outcome[0].result.places == "2"
    }
  }

  def "When cashout was suspended and then selection was activated then getBetDetail should be requested"() {
    def bet1 = bet("1", [["111", "222", "333"]])
    bet1.cashoutValue = "CASHOUT_SELN_SUSPENDED"
    given:
    userReqCtx = createCtxWithBets([bet1])
    def selUpdate = selectionWithStatus("Active", null, null)
    when:
    selectionUpdateProcessor.process(userReqCtx, selUpdate)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "If price updated for banach bet, then betDetail is requested instead of cashoutOffer"() {
    given:
    userReqCtx = createCtxWithBets([
      banachBet("111", ["103", "102", "101"])
    ])

    def selection = selectionWithPrice(101, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }

  def "If selection is suspended then FE suspension is triggered"() {
    given:
    userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get().changeLpPrice(1, 2)
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    when:

    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    1 * suspensionTrigger.triggerCashoutSuspension({
      it.token == "123"
      it.betIds.size() == 2
      it.betIds[0] == "1"
      it.betIds[1] == "2"
    })

    where:
    selection << [
      selectionWithStatus("Suspended", null, null),
      selectionWithStatus("Suspended", null, null),
    ]
  }

  def "Expect cashoutOffer for single price change"() {
    given:
    userReqCtx = createCtxWithBets([singleBet()])

    def selection = selectionWithPrice(1000, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }

  def "Expect cashoutOffer on LP price change"() {
    given:
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    selData.changeLpPrice(3, 4)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:

    0 * priceRepository.multiGet(_);

    where:
    selection                                   | expectedLpNum | expectedLpDen
    selectionWithPrice(333, ["LP"], 4, 5)       | "4"           | "5"
    selectionWithPrice(333, ["SP", "LP"], 4, 5) | "4"           | "5"
  }

  def "Expect cashoutOffer on SP price change"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]], "S"),
      bet("2", [["111", "222", "333"]], "S")
    ])
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    selData.changeSpPrice(3, 4)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    selection                                   | expectedSpNum | expectedSpDen
    selectionWithPrice(333, ["SP"], 4, 5)       | "4"           | "5"
    selectionWithPrice(333, ["SP", "LP"], 4, 5) | "4"           | "5"
  }

  @Unroll
  def "Expect no cashout offer for bet on #betPriceType price when #updatePriceType price changes"() {
    given:
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "222", "333"]], betPriceType)
    ])


    selData.changeLpPrice(3, 4)
    selData.changeSpPrice(1, 2)

    when:
    def selection = selectionWithPrice(333, [updatePriceType], 99, 999)
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:

    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    betPriceType | updatePriceType
    "L"          | "SP"
    "S"          | "LP"
  }

  def "When price changes for multiple then other prices are taken from redis and cashoutOffer is requested"() {
    given:
    userReqCtx = createCtxWithBets([
      trebbleBetWithOnePriceKnownOnly()
    ])

    def selection = selectionWithPrice(101, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty().subscribeOn(Schedulers.immediate())

  }

  def "Processor shouldn't go to redis if prices already in context"() {
    given:
    userReqCtx = createCtxWithBets([
      trebbleBetWithOnePriceKnownOnly()
    ])

    userReqCtx.indexedData.getSelectionDataBySelectionId(101)
        .get().changeLpPrice(1, 2)
    userReqCtx.indexedData.getSelectionDataBySelectionId(102)
        .get().changeLpPrice(2, 3)
    userReqCtx.indexedData.getSelectionDataBySelectionId(103)
        .get().changeLpPrice(3, 4)

    Selection selection = selectionWithPrice(101, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    0 * priceRepository.multiGet(_);
  }

  def "No cashout offer if prices haven't changed"() {
    given:
    indexedData.getBetsWithSelection(101) >> [
      trebbleBetWithAllPricesInContext()
    ]

    Selection selection = selectionWithPrice(101, ["LP"], 1, 2)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    0 * priceRepository.multiGet(_);
  }

  //    def "Expect nothing requested"() {
  //      given:
  //      ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
  //      expect:
  //      interaction {
  //        expectNoGetBetDetailRequests()
  //      }
  //      selectionUpdateProcessor.process(userReqCtx, selection)
  //      where:
  //      selection << [
  //        selection(333),
  //        selectionWithStatus(null, null, null),
  //        selectionWithStatus(null, null, null),
  //        new Selection()
  //      ]
  //    }

  def "Expect no betDetail calls in case bet settled"() {
    given:
    userReqCtx.addSettledBets(["1", "2", "3"])
    selectionUpdateProcessor.process(userReqCtx, selection)

    where:
    selection << [
      selectionWithStatus("Active", null, null),
    ]

  }

  def "Expect no Cashout Offer request in case bet settled"() {
    given:
    userReqCtx = createCtxWithBets([singleBet()])
    userReqCtx.addSettledBets(["100"])
    def selection = selectionWithPrice(1000, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }
  def "Expect no Cashout Offer request in case bet settled price type S"() {
    given:
    ReflectionTestUtils.setField(cashoutOfferService,"cashoutOfferReqSize",4)
    userReqCtx = createCtxWithBets([singleBetpriceS()])
    userReqCtx.addSettledBets(["100"])
    def selection = selectionWithPrice(1000, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }
  def "Expect no Cashout Offer request in case bet settled price type null"() {
    given:
    userReqCtx = createCtxWithBets([singleBetpricenull()])
    userReqCtx.addSettledBets(["100"])
    def selection = selectionWithPrice(1000, ["LP"], 10, 15)

    when:
    selectionUpdateProcessor.process(userReqCtx, selection)

    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }

  def "When suspended selection price is changed to uncompetitive then getBetDetail is executed"() {
    given:
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    selData.changeLpPrice(3, 4)
    selData.setEventActive(true)
    selData.setMarketActive(true)
    selData.setSelectionActive(false)
    def selection = selectionWithPrice(333, ["LP"], 1, 100)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    priceRepository.multiGet(_) >> Mono.empty()
  }

  def "When suspended selection price is changed to competitive then suspension is triggered"() {
    given:
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    selData.changeLpPrice(1, 100)
    selData.setEventActive(true)
    selData.setMarketActive(true)
    selData.setSelectionActive(false)
    def selection = selectionWithPrice(333, ["LP"], 1, 99)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "When settled then ignore"() {
    given:
    def selData = userReqCtx.getIndexedData().getSelectionDataBySelectionId(333).get()
    selData.changeLpPrice(1, 100)
    selData.setEventActive(true)
    selData.setMarketActive(true)
    selData.setSelectionActive(false)
    def selection = selection(333)
    selection.setIsSettled(true)
    when:
    selectionUpdateProcessor.process(userReqCtx, selection)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def "sendBetUpdateIfNeeded"() {
    given:
    List<String> betIds=new ArrayList<>();
    betIds.add("231345")
    betIds.add("321221")
    BetDetailMeta betDetailMeta =BetDetailMeta.builder().username("betupdate")
        .tokenExpiresIn(Duration.ZERO)
        .token("2swaerdsdd")
        .betIds(betIds)
        .build()
    when:
    processor.sendBetUpdateIfNeeded(betDetailMeta)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "sendBetUpdateIfNeeded_empty"() {
    given:
    BetDetailMeta betDetailMeta =BetDetailMeta.builder().username("betupdate")
        .tokenExpiresIn(Duration.ZERO)
        .token("2swaerdsdd")
        .build()
    when:
    processor.sendBetUpdateIfNeeded(betDetailMeta)
    then:
    0 * priceRepository.multiGet(_);
  }

  def "Bet Details"() {
    ReflectionTestUtils.setField(cashoutOfferService,"betIdSize",4)
    UserRequestContextAccHistory userRequestContextAccHistory=UserRequestContextAccHistory
        .builder()
        .token("123")
        .username("devtest")
        .connectionDate(new Date())
        .tokenExpiresIn(Duration.ZERO)
        .build()
    Selection selection=new Selection()
    Set<String> betIds=new HashSet<>()
    betIds.add("213455")
    betIds.add("219029")
    when:
    processor.getBetDetail(userRequestContextAccHistory,selection,betIds)
    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)
  }

  def singleBet() {
    def sgl = new BetSummaryModel()
    def betTYpe = new BetType()
    betTYpe.code = "SGL"
    sgl.cashoutValue = "5.6"
    sgl.betType = betTYpe
    def stake = new Stake()
    stake.value = "2.0"
    sgl.stake = stake
    sgl.id = "100"
    sgl.leg = [
      legWithPrice("1000", "1", "2")
    ]
    return sgl
  }
  def singleBetpriceS() {
    def sgl = new BetSummaryModel()
    def betTYpe = new BetType()
    betTYpe.code = "SGL"
    sgl.cashoutValue = "5.6"
    sgl.betType = betTYpe
    def stake = new Stake()
    stake.value = "2.0"
    sgl.stake = stake
    sgl.id = "100"
    sgl.leg = [
      legWithPriceS("1000", "1", "2")
    ]
    return sgl
  }
  def singleBetpricenull() {
    def sgl = new BetSummaryModel()
    def betTYpe = new BetType()
    betTYpe.code = "SGL"
    sgl.cashoutValue = "5.6"
    sgl.betType = betTYpe
    def stake = new Stake()
    stake.value = "2.0"
    sgl.stake = stake
    sgl.id = "100"
    sgl.leg = [
      legWithPricenull("1000", "1", "2")
    ]
    return sgl
  }


  def trebbleBetWithAllPricesInContext() {
    def trebble = new BetSummaryModel()
    trebble.id = "9"
    def stake = new Stake()
    stake.value = "2.0"
    trebble.stake = stake
    def type = new BetType()
    type.code = "TBL"
    trebble.betType = type
    trebble.leg = [
      legWithPrice("101", "1", "2"),
      legWithPrice("102", "2", "3"),
      legWithPrice("103", "3", "4"),
    ]
    return trebble
  }

  def trebbleBetWithOnePriceKnownOnly() {
    def trebble = new BetSummaryModel()
    trebble.id = "9"
    def stake = new Stake()
    trebble.cashoutValue = "5.6"
    stake.value = "2.0"
    trebble.stake = stake
    def type = new BetType()
    type.code = "TBL"
    trebble.betType = type
    trebble.leg = [
      legWithPrice("101", "1", "2"),
      legWithPrice("102", "1", "2"),
      legWithPrice("103", "1", "2"),
    ]
    return trebble
  }

  def selection(int selectionId) {
    def selection = new Selection()
    selection.selectionKey = selectionId
    return selection
  }

  def selectionWithPrice(int selectionId, List<String> priceTypes, int num, int den) {
    def selection = selection(selectionId)
    def prices = new Prices()
    def priceList = priceTypes.collect {
      def price = new Price()
      price.numPrice = num
      price.denPrice = den
      price.selectionPriceType = it
      return price
    }
    prices.price = priceList
    selection.prices = prices
    return selection
  }

  def selectionWithStatus(String status, Boolean settled, String resultCode) {
    def selection = selection(333)
    selection.selectionStatus = status
    selection.isSettled = settled
    selection.resultCode = resultCode
    return selection
  }

  def selectionWithStatusDeadHeat(String status, Boolean settled, String resultCode,DeadHeat deadHeat) {
    def selection = selection(333)
    selection.selectionStatus = status
    selection.isSettled = settled
    selection.resultCode = resultCode
    selection.deadHeat = deadHeat
    return selection
  }

  def banachBet(String betId, List<String> hierarchy) {
    def bet = bet(betId, [hierarchy])
    bet.source = "e"
    bet.cashoutValue = "5.6"

    return bet
  }
}
