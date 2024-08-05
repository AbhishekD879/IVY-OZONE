package com.ladbrokescoral.cashout.service.updates

import com.ladbrokescoral.cashout.model.context.SelectionPrice
import com.ladbrokescoral.cashout.model.safbaf.Event
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository
import org.springframework.test.util.ReflectionTestUtils
import reactor.core.publisher.Mono
import reactor.core.scheduler.Schedulers
import spock.lang.Unroll

class EventUpdateProcessorTest extends UpdateProcessorsSpec {
  private UserUpdateTrigger suspensionTrigger = Mock(UserUpdateTrigger)
  private SelectionPriceRepository priceRepo = Mock(SelectionPriceRepository)
  private EventUpdatePublisher eventUpdatePublisher = Mock(EventUpdatePublisher)
  private CashoutService cashoutOfferService=Mock(CashoutService)
  private SelectionDataAwareUpdateProcessor<Event> processor = new SelectionDataAwareUpdateProcessor<>(
  new EventUpdateApplier(),
  suspensionTrigger,
  priceRepo,
  converter,
  2,
  cashoutOfferService
  )
  private UpdateProcessor<Event> eventUpdateProcessor = new EventUpdateProcessor(processor, eventUpdatePublisher)

  @Override
  void setup() {
    def prices = [
      new SelectionPrice("444", "5", "10"),
      null
    ]
    processor.setAfterPriceUpdateExecutor(Schedulers.immediate())
    priceRepo.multiGet(_) >> Mono.fromSupplier({ prices })
    .subscribeOn(Schedulers.immediate())
  }


  @Unroll
  def "When event activation activates whole bet then cashout offer is requested"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "333", "444"]]),
      bet("2", [["111", "333", "555"]]),
      bet("3", [["111", "333", "666"]])
    ])
    userReqCtx.indexedData.getSelectionDataByEventId(111)
        .forEach({
          it.setEventActive(false)
        })
    userReqCtx.indexedData.getSelectionDataBySelectionId(555).get().changeLpPrice(1, 2)
    def deactivatedSelection = userReqCtx.indexedData.getSelectionDataBySelectionId(666).get()
    deactivatedSelection.changeLpPrice(6, 10)
    deactivatedSelection.setSelectionActive(false)
    when:
    eventUpdateProcessor.process(userReqCtx, event)

    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    event << [
      eventWithStatus("Active", null),
      eventWithStatus("Active", "NotDisplayed"),
      eventWithStatus("Active", null),
    ]
  }

  def "Expect not getBetDetail requested"() {
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [event()]
  }


  def "update selectionData based on isEventStarted false"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "333", "11"]]),
    ])

    def selectionData = userReqCtx.indexedData.getSelectionDataBySelectionId(11).get()
    selectionData.selectionId =12
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventWithisEventStarted("false")
    ]
  }


  def "selectionData data is null and isEventStarted false"() {
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      event2WithIsEventStarted("false")
    ]
  }

  def "update selectionData based on isEventStarted true"() {
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventWithisEventStarted("true")
    ]
  }
  def "update selectionData based on isEventStarted null"() {
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [event()]
  }
  def "Expect no betDetail calls in case bet settled"() {
    given:
    userReqCtx = createCtxWithBets([
      bet("1", [["222", "333", "444"]])
    ])
    userReqCtx.addSettledBets(["1"])
    when:
    eventUpdateProcessor.process(userReqCtx, event)

    then:
    0 * suspensionTrigger.triggerCashoutSuspension(_)

    where:
    event << [
      eventWithStatus("Active", "NotDisplayed"),
      eventWithStatus("Suspended", "Any")
    ]
  }

  def "Expect event update requested"() {
    given:
    ReflectionTestUtils.setField(eventUpdateProcessor,"eventUpdateFlags","AVD,PVD")
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "333", "444"]]),
      bet("2", [["111", "333", "555"]]),
      bet("3", [["111", "333", "666"]])
    ])
    userReqCtx.indexedData.getSelectionDataByEventId(111)
        .forEach({
          it.setEventActive(false)
          it.getBets().forEach({ b ->
            b.getLeg().forEach({ l ->
              l.getPart().forEach({ p ->
                p.getOutcome().forEach({ o ->
                  o.getEvent().setFlags("AVD")
                })
              })
            })
          })
        })
    userReqCtx.indexedData.getSelectionDataBySelectionId(555).get().changeLpPrice(1, 2)
    def deactivatedSelection = userReqCtx.indexedData.getSelectionDataBySelectionId(666).get()
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventUpdateWithFlags("false")
    ]
  }

  def "Expect event update request denied due to missing flags"() {
    given:
    ReflectionTestUtils.setField(eventUpdateProcessor,"eventUpdateFlags","AVD,PVD")
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "333", "444"]]),
      bet("2", [["111", "333", "555"]]),
      bet("3", [["111", "333", "666"]])
    ])
    userReqCtx.indexedData.getSelectionDataByEventId(111)
        .forEach({
          it.setEventActive(false)
          it.getBets().forEach({ b ->
            b.getLeg().forEach({ l ->
              l.getPart().forEach({ p ->
                p.getOutcome().forEach({ o ->
                  o.getEvent().setFlags("ASD")
                })
              })
            })
          })
        })
    userReqCtx.indexedData.getSelectionDataBySelectionId(555).get().changeLpPrice(1, 2)
    def deactivatedSelection = userReqCtx.indexedData.getSelectionDataBySelectionId(666).get()
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventUpdateWithFlags("false")
    ]
  }

  def "Expect event update request denied"() {
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventUpdateWithAVDMissingInFlags("false")
    ]
  }

  def "Expect event update request denied due to empty selection data"() {
    userReqCtx = createCtxWithBets([
      bet("1", [["111", "333", "444"]]),
      bet("2", [["111", "333", "555"]]),
      bet("3", [["111", "333", "666"]])
    ])
    userReqCtx.indexedData.getSelectionDataByEventId(11)
        .forEach({
          it.setEventActive(false)
        })
    eventUpdateProcessor.process(userReqCtx, event)

    where:
    event << [
      eventUpdateUnfinishedEvent("false")
    ]
  }

  def event() {
    def eventUpdate = new Event()
    eventUpdate.eventKey = 111
    return eventUpdate
  }
  def event2() {
    def eventUpdate = new Event()
    eventUpdate.eventKey = 112
    return eventUpdate
  }

  def event3() {
    def eventUpdate = new Event()
    eventUpdate.eventKey = 11
    return eventUpdate
  }

  def eventWithStatus(String status, String displayStatus) {
    def event = event()
    event.eventStatus = status
    event.isEventStarted = "true"
    return event
  }
  def eventWithisEventStarted(String isEventStarted) {
    def eventObj = event()
    eventObj.isEventStarted = isEventStarted
    return eventObj
  }
  def event2WithIsEventStarted(String isEventStarted) {
    def eventObj = event2()
    eventObj.isEventStarted = isEventStarted
    return eventObj
  }

  def eventUpdateWithFlags(String isEventStarted) {
    def eventObj = event()
    eventObj.isEventStarted = isEventStarted
    eventObj.eventFinished = true
    return eventObj
  }

  def eventUpdateWithAVDMissingInFlags(String isEventStarted) {
    def eventObj = event()
    eventObj.isEventStarted = isEventStarted
    eventObj.eventFinished = false
    return eventObj
  }

  def eventUpdateUnfinishedEvent(String isEventStarted) {
    def eventObj = event3()
    eventObj.isEventStarted = isEventStarted
    eventObj.eventFinished = true
    return eventObj
  }
}
