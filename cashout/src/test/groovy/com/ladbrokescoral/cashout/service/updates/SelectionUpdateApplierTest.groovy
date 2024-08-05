package com.ladbrokescoral.cashout.service.updates

import com.ladbrokescoral.cashout.model.ResultCode
import com.ladbrokescoral.cashout.model.safbaf.Price
import com.ladbrokescoral.cashout.model.safbaf.Selection
import com.ladbrokescoral.cashout.service.SelectionData
import spock.lang.Specification

import static com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo.ACTIVATED
import static com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo.LP_PRICE_CHANGED
import static com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo.CONFIRMED
import static com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo.SP_PRICE_CHANGED
import static com.ladbrokescoral.cashout.service.updates.SafUpdateApplier.ChangeInfo.SUSPENDED

class SelectionUpdateApplierTest extends Specification {
  def updateApplier = new SelectionUpdateApplier();

  def "Test update applied"() {
    given:
    def selectionData = Mock(SelectionData)
    def selectionUpdate = Spy(new Selection())
    def lpPrice = new Price()
    lpPrice.numPrice = 1
    lpPrice.denPrice = 2
    def spPrice = new Price()
    spPrice.numPrice = 3
    spPrice.denPrice = 4
    selectionUpdate.getLpPrice() >> Optional.of(lpPrice)
    selectionUpdate.getSpPrice() >> Optional.of(spPrice)
    selectionUpdate.getResultConfirmed() >> Optional.of(true)
    selectionUpdate.isActivated() >> false
    selectionUpdate.isSuspended() >> true
    selectionData.getSelectionStatus() >> SelectionData.SelectionStatus.SUSPENDED
    when:
    def change = updateApplier.applyChange(selectionData, selectionUpdate)
    then:
    1 * selectionData.changeLpPrice(1, 2) >> true
    1 * selectionData.changeSpPrice(3, 4) >> true
    1 * selectionData.changeSelectionStatus(false) >> true
    1 * selectionData.updateConfirmed(true) >> true

    change.size() == 4
    change.containsAll(
        EnumSet.of(
        LP_PRICE_CHANGED,
        SP_PRICE_CHANGED,
        CONFIRMED,
        SUSPENDED,
        )
        )
  }

  def "Active but not changed"() {
    given:
    def selectionData = Mock(SelectionData)
    def selectionUpdate = Spy(new Selection())
    selectionUpdate.getLpPrice() >> Optional.empty()
    selectionUpdate.getSpPrice() >> Optional.empty()
    selectionUpdate.getResultCode() >> Optional.empty()
    selectionUpdate.isActivated() >> true
    selectionUpdate.isSuspended() >> false
    selectionData.getSelectionStatus() >> SelectionData.SelectionStatus.ACTIVE
    when:
    def change = updateApplier.applyChange(selectionData, selectionUpdate)
    then:
    1 * selectionData.changeSelectionStatus(true) >> false

    change.size() == 0
  }

  def "Test activated"() {
    given:
    def selectionData = Mock(SelectionData)
    def selectionUpdate = Spy(new Selection())
    selectionUpdate.getLpPrice() >> Optional.empty()
    selectionUpdate.getSpPrice() >> Optional.empty()
    selectionUpdate.getResultCode() >> Optional.empty()
    selectionUpdate.isActivated() >> true
    selectionUpdate.isSuspended() >> false
    selectionData.getSelectionStatus() >> SelectionData.SelectionStatus.ACTIVE
    when:
    def change = updateApplier.applyChange(selectionData, selectionUpdate)
    then:
    1 * selectionData.changeSelectionStatus(true) >> true

    change.size() == 1
    change.contains(ACTIVATED)
  }

  def "test resulted"() {
    given:
    def selectionData = Mock(SelectionData)
    def selectionUpdate = Mock(Selection)
    selectionUpdate.getLpPrice() >> Optional.empty()
    selectionUpdate.getSpPrice() >> Optional.empty()
    selectionUpdate.getResultCode() >> Optional.of("win")
    selectionUpdate.getResultConfirmed() >> Optional.empty()
    selectionUpdate.isActivated() >> false
    selectionUpdate.isSuspended() >> false
    when:
    def change = updateApplier.applyChange(selectionData, selectionUpdate)
    then:
    0 * selectionData.changeLpPrice(_, _)
    0 * selectionData.changeSpPrice(_, _)
    0 * selectionData.changeSelectionStatus(_)
    1 * selectionData.updateResultCode(_, _)
    change.size() == 0
  }

  def "Test confirmed"() {
    given:
    def selectionData = Mock(SelectionData)
    def selectionUpdate = Spy(new Selection())
    selectionUpdate.getLpPrice() >> Optional.empty()
    selectionUpdate.getSpPrice() >> Optional.empty()
    selectionUpdate.getResultConfirmed() >> Optional.of(true)
    selectionUpdate.isActivated() >> true
    selectionUpdate.isSuspended() >> false
    selectionData.getSelectionStatus() >> SelectionData.SelectionStatus.ACTIVE
    when:
    def change = updateApplier.applyChange(selectionData, selectionUpdate)
    then:
    1 * selectionData.updateConfirmed(true) >> true

    change.size() == 1
    change.contains(CONFIRMED)
  }
}
