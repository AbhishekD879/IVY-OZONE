package com.coral.oxygen.edp.model.mapping

import com.coral.oxygen.edp.TestUtil
import com.coral.oxygen.edp.model.mapping.converter.MarketGroupAndSortConverter
import com.coral.oxygen.edp.model.output.OutputEvent
import com.coral.oxygen.edp.model.output.OutputOutcome
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import spock.lang.Specification

import static com.coral.oxygen.edp.TestUtil.deserializeWithJackson

class SimpleEventMapperSpec extends Specification {

  def mockEventRaw = deserializeWithJackson("/virtuals/event_with_shuffled_outcomes_raw.json", Event.class)
  def mockEventRawCorrupted = deserializeWithJackson("/virtuals/event_virtual_raw.json", Event.class)
  def mockEventCorruptedPrice = deserializeWithJackson("/virtuals/event_with_corrupted_price.json", OutputEvent.class)
  def mockEventMapped = deserializeWithJackson("/virtuals/event_with_sorted_outcomes.json", OutputEvent.class)
  def mockEventMappedShuffledOutcomes = deserializeWithJackson("/virtuals/event_with_shuffled_outcomes.json", OutputEvent.class)

  def marketMapper = Mock(MarketMapper)
  def marketConverter = new MarketGroupAndSortConverter()

  def eventMapper = new SimpleEventMapper(marketMapper, marketConverter, TestUtil.virtualRacingIds())

  def setup() {

    marketMapper.map(mockEventRaw, _ as Market) >>
        mockEventMappedShuffledOutcomes.getMarkets().get(0)

    marketMapper.map(mockEventRawCorrupted, _ as Market) >>
        mockEventCorruptedPrice.getMarkets().get(0)
  }

  def "Mapper sorts event's outcomes in correct order"() {
    when: 'map the raw event'
    OutputEvent result = eventMapper.map(new OutputEvent(), mockEventRaw)
    def mockOutcomes = getOutcomes(mockEventMapped)
    def mappedOutcomes = getOutcomes(result)

    then: 'outcomes are sorted by price, ascending'
    checkOutcomeOrder(mockOutcomes, mappedOutcomes)
  }

  def "Mapper handles if PriceDen is equal to 0"() {
    when: 'map the raw event'
    eventMapper.map(new OutputEvent(), mockEventRawCorrupted)

    then: 'no exception is thrown'
    noExceptionThrown()
  }

  /**
   * Check if the element orders of both parameters are equal by id
   */

  def checkOutcomeOrder(List<OutputOutcome> mappedOutcomes, List<OutputOutcome>  mockOutcomes) {

    for (int i = 0; i < mappedOutcomes.size(); i++) {
      if (mappedOutcomes.get(i).getId() != mockOutcomes.get(i).getId()) {
        return false
      }
    }
    return true
  }

  def getOutcomes(OutputEvent event) {
    return event.getMarkets().get(0).getOutcomes()
  }
}
