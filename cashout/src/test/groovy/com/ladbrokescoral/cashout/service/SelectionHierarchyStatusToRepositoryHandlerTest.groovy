package com.ladbrokescoral.cashout.service


import com.ladbrokescoral.cashout.model.safbaf.Event
import com.ladbrokescoral.cashout.model.safbaf.HasStatus
import com.ladbrokescoral.cashout.model.safbaf.Market
import com.ladbrokescoral.cashout.model.safbaf.Selection
import com.ladbrokescoral.cashout.repository.EntityStatus
import com.ladbrokescoral.cashout.repository.SelectionHierarchyStatusRepository
import org.springframework.messaging.support.GenericMessage
import spock.lang.Specification

class SelectionHierarchyStatusToRepositoryHandlerTest extends Specification {
  private SelectionHierarchyStatusRepository statusRepository
  private SelectionHierarchyStatusToRepositoryHandler service

  void setup() {
    statusRepository = Mock(SelectionHierarchyStatusRepository)
    service = new SelectionHierarchyStatusToRepositoryHandler(statusRepository)
  }

  def "When event status is changed then repo is updated"() {
    when:
    service.handleUpdateMessage(new GenericMessage<>(eventWithStatus(123, updateStatus)))
    then:
    0 * this.selectionPriceRepository
    1 * this.statusRepository.updateEventStatus(new EntityStatus(123, updateStatus))
    0 * _
    where:
    updateStatus << [true, false]
  }

  def "When market status is changed then repo is updated"() {
    when:
    service.handleUpdateMessage(new GenericMessage<>(marketWithStatus(123, updateStatus)))
    then:
    0 * this.selectionPriceRepository
    1 * this.statusRepository.updateMarketStatus(new EntityStatus(123, updateStatus))
    0 * _
    where:
    updateStatus << [true, false]
  }

  def "When selection status is changed then repo is updated"() {
    when:
    service.handleUpdateMessage(new GenericMessage<>(selectionWithStatus(123, updateStatus)))
    then:
    0 * this.selectionPriceRepository
    1 * this.statusRepository.updateSelectionStatus(new EntityStatus(123, updateStatus))
    0 * this.statusRepository._
    where:
    updateStatus << [true, false]
  }

  def "When event update has no status changed then nothing is called"() {
    when:
    service.handleUpdateMessage(new GenericMessage<>(eventWithStatus(123, null)))
    then:
    0 * _
  }

  def "When selection update has not status or price change then nothing is called"() {
    def status = Mock(Selection)
    when:
    service.handleUpdateMessage(new GenericMessage<>(status))
    then:
    1 * status.statusChanged() >> false
    0 * _
  }

  Event eventWithStatus(int eventId, Boolean status) {
    def event = Mock(Event)
    event.getEventKey() >> eventId
    mockStatus(event, status)
    event
  }

  Market marketWithStatus(int marketId, Boolean status) {
    def market = Mock(Market)
    market.getMarketKey() >> marketId
    mockStatus(market, status)
    market
  }

  Selection selectionWithStatus(int selId, Boolean status) {
    def selection = Mock(Selection)
    selection.getSelectionKey() >> selId
    mockStatus(selection, status)
    selection.getLpPrice() >> Optional.empty()
    selection
  }

  def mockStatus(HasStatus update, Boolean status) {
    update.statusChanged() >> (status != null)
    update.isActivated() >> status
    update.isSuspended() >> !status
  }
}
