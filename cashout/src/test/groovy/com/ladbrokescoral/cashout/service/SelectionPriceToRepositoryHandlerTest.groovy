package com.ladbrokescoral.cashout.service

import com.ladbrokescoral.cashout.model.context.SelectionPrice
import com.ladbrokescoral.cashout.model.safbaf.Price
import com.ladbrokescoral.cashout.model.safbaf.Selection
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository
import reactor.core.publisher.Mono
import spock.lang.Specification

class SelectionPriceToRepositoryHandlerTest extends Specification {
  private SelectionPriceRepository selectionPriceRepository = Mock(SelectionPriceRepository)
  def handler = new SelectionPriceToRepositoryHandler(selectionPriceRepository)

  def "When selection update has LP prices then they are saved to repository"() {
    given:
    def selection = Mock(Selection)
    selection.getLpPrice() >> Optional.of(price(49, 50))
    selection.getSelectionKey() >> 519997063
    selection.statusChanged() >> false
    SelectionPrice selectionPrice = SelectionPrice.builder()
        .priceDen("50")
        .priceNum("49")
        .outcomeId("519997063")
        .build()
    when:
    handler.handleUpdateMessage(selection)
    then:
    1 * this.selectionPriceRepository.save("519997063", selectionPrice) >> Mono.empty()
    0 * selectionPriceRepository._
  }

  def "Selection update without LP price change is ignored"() {
    when:
    handler.handleUpdateMessage(new Selection())
    then:
    0 * this.selectionPriceRepository._
  }

  def price(int num, int den) {
    def price = new Price()
    price.numPrice = num
    price.denPrice = den
    price
  }
}
