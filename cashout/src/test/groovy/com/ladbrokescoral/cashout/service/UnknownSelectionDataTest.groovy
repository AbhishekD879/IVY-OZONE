package com.ladbrokescoral.cashout.service

import com.ladbrokescoral.cashout.model.context.IndexedSportsData
import spock.lang.Specification

class UnknownSelectionDataTest extends Specification {
  private static final SelectionDataPrice priceOneToTwo = new SelectionDataPrice(1, 2)

  def "Updating with id that not exists does not cause an exception"() {
    given:
    def idx = Mock(IndexedSportsData)
    idx.getAllSelectionData() >> []
    idx.getSelectionDataByEventId(_) >> []
    idx.getSelectionDataByMarketId(_) >> []
    idx.getSelectionDataBySelectionId(_) >> []
    when:
    def unknownSelectionData = createUnknownData(idx)
    then:
    unknownSelectionData.updateEventStatus(1, true)
    unknownSelectionData.updateMarketStatus(1, true)
    unknownSelectionData.updateSelectionStatus(1, true)
  }

  def "When empty selection data list is supplied then unknown entities are empty"() {
    given:
    def idx = Mock(IndexedSportsData)
    idx.getAllSelectionData() >> []
    when:
    def unknownSelectionData = createUnknownData(idx)
    then:
    unknownSelectionData.getMarketIdsOfUnknownItems().isEmpty()
    unknownSelectionData.getUnknownEntitiesOnly().getEventIds().isEmpty()
    unknownSelectionData.getUnknownEntitiesOnly().getMarketIds().isEmpty()
    unknownSelectionData.getUnknownEntitiesOnly().getSelectionIds().isEmpty()
  }

  def "If there are no selection with unknown statuses or price, then redis and siteserver isn't called"() {
    given:
    def unknownSelectionData = createUnknownData([
      selData([1: true], [2: true], [3: true], priceOneToTwo)
    ])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds().isEmpty()
    unknownEntities.getMarketIds().isEmpty()
    unknownEntities.getSelectionIds().isEmpty()
  }

  def "If price is unknown then selectionId is present in unknown set"() {
    given:
    def selData = selData([1: true], [2: true], [3: true], null)
    selData.hasUnknownStatusOrLpPrice() >> true
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds().isEmpty()
    unknownEntities.getMarketIds().isEmpty()
    unknownEntities.getSelectionIds()[0] == 3
  }

  def "If selection data has unknown status or price then selectionId is present in unknown set"() {
    given:
    def selData = selData([1: true], [2: true], [3: null], priceOneToTwo)
    selData.hasUnknownStatusOrLpPrice() >> true
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds().isEmpty()
    unknownEntities.getMarketIds().isEmpty()
    unknownEntities.getSelectionIds()[0] == 3
  }

  def "If market status is unknown then marketId is present in unknown set"() {
    given:
    def selData = selData([1: true], [2: null], [3: true], priceOneToTwo)
    selData.hasUnknownStatusOrLpPrice() >> true
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds().isEmpty()
    unknownEntities.getMarketIds()[0] == 2
    unknownEntities.getSelectionIds().isEmpty()
  }

  def "if every status is unknown then all entities are in unknown set"() {
    given:
    def selData = selData([1: null], [2: null], [3: null], priceOneToTwo)
    selData.hasUnknownStatusOrLpPrice() >> true
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds()[0] == 1
    unknownEntities.getMarketIds()[0] == 2
    unknownEntities.getSelectionIds()[0] == 3
  }

  def "If event status is unknown then eventId is present in unknown set"() {
    given:
    def selData = selData([1: null], [2: true], [3: true], priceOneToTwo)
    selData.hasUnknownStatusOrLpPrice() >> true
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds()[0] == 1
    unknownEntities.getMarketIds().isEmpty()
    unknownEntities.getSelectionIds().isEmpty()
  }

  def "If does not have unknown statuses or price then unknown entities are empty"() {
    given:
    def selData = Mock(SelectionData)
    selData.hasUnknownStatusOrLpPrice() >> false
    def unknownSelectionData = createUnknownData([selData])
    when:
    def unknownEntities = unknownSelectionData.getUnknownEntitiesOnly();
    then:
    unknownEntities.getEventIds().isEmpty()
    unknownEntities.getMarketIds().isEmpty()
    unknownEntities.getSelectionIds().isEmpty()
  }

  def "When selection data has unknown status or price then its marketId is returned"() {
    given:
    def unknownSelectionData = createUnknownData([selData123(true)])
    when:
    def marketIds = unknownSelectionData.getMarketIdsOfUnknownItems();
    then:
    marketIds[0] == 2
  }

  def "When selection data does not have unknown status or price then its marketIds list is empty"() {
    given:
    def unknownSelectionData = createUnknownData([
      selData123(false)
    ])
    when:
    def marketIds = unknownSelectionData.getMarketIdsOfUnknownItems();
    then:
    marketIds.size() == 0
  }

  def "Event status is updated"() {
    given:
    def idx = Mock(IndexedSportsData)
    def selList = [
      selData([1: true], [11: true], [111: true], priceOneToTwo),
      selData([1: false], [12: true], [121: true], priceOneToTwo)
    ]
    idx.getSelectionDataByEventId(1) >> selList
    def unknownData = createUnknownData(idx)
    when:
    unknownData.updateEventStatus(1, true)
    then:
    1 * selList[0].changeEventStatus(true)
    1 * selList[1].changeEventStatus(true)
  }

  def "Market status is updated"() {
    given:
    def idx = Mock(IndexedSportsData)
    def selList = [
      selData([1: true], [11: true], [111: true], priceOneToTwo),
      selData([1: false], [11: true], [112: true], priceOneToTwo),
    ]
    idx.getSelectionDataByMarketId(11) >> selList
    def unknownData = createUnknownData(idx)
    when:
    unknownData.updateMarketStatus(11, false)
    then:
    1 * selList[0].changeMarketStatus(false)
    1 * selList[1].changeMarketStatus(false)
  }

  def "Selection status is updated"() {
    given:
    def idx = Mock(IndexedSportsData)
    def selList = [
      selData([1: true], [11: true], [111: true], priceOneToTwo),
    ]
    idx.getSelectionDataBySelectionId(111) >> selList
    def unknownData = createUnknownData(idx)
    when:
    unknownData.updateSelectionStatus(111, true)
    then:
    1 * selList[0].changeSelectionStatus(true)
  }

  def "Prices are updated"() {
    given:
    def idx = Mock(IndexedSportsData)
    def selList = [
      selData([1: true], [11: true], [111: true], priceOneToTwo),
    ]
    idx.getSelectionDataBySelectionId(111) >> selList
    def unknownData = createUnknownData(idx)
    when:
    unknownData.updatePrice(111, 3, 4)
    then:
    1 * selList[0].changeLpPrice(3, 4)
  }

  SelectionData selData(Map<Integer, Boolean> eventStatus, Map<Integer, Boolean> marketStatus, Map<Integer, Boolean> selectionStatus, SelectionDataPrice selectionDataPrice) {
    def selData = Mock(SelectionData)
    selData.getEventId() >> eventStatus.entrySet()[0].key
    selData.getEventActive() >> eventStatus.entrySet()[0].value
    selData.getMarketId() >> marketStatus.entrySet()[0].key
    selData.getMarketActive() >> marketStatus.entrySet()[0].value
    selData.getSelectionId() >> selectionStatus.entrySet()[0].key
    selData.getSelectionActive() >> selectionStatus.entrySet()[0].value
    selData.getLpPrice() >> Optional.ofNullable(selectionDataPrice)
    return selData
  }

  SelectionData selData123(boolean hasUnknownStatusesOrLpPrice) {
    def selData = Mock(SelectionData)
    selData.getEventId() >> 1
    selData.getMarketId() >> 2
    selData.getSelectionId() >> 3
    selData.hasUnknownStatusOrLpPrice() >> hasUnknownStatusesOrLpPrice
    return selData
  }

  def createUnknownData(IndexedSportsData indexedSportsData) {
    UnknownSelectionData.create(indexedSportsData)
  }

  def createUnknownData(List<SelectionData> selectionDataList) {
    def idx = Mock(IndexedSportsData)
    idx.getAllSelectionData() >> selectionDataList
    UnknownSelectionData.create(idx)
  }
}
