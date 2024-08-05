from voltron.pages.shared.components.byb_betslip import BYBBetslip
from voltron.pages.shared.components.byb_betslip import BYBQuickBetSelection
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.utils.waiters import wait_for_result


class LadbrokesDepositInfoMessage(InfoPanel):
    _text = 'xpath=.//*[@data-crlat="message"]'
    _info_icon = 'xpath=.//*[@data-crlat="infoIcon"]'

    @property
    def info_icon(self):
        return IconBase(selector=self._info_icon, context=self._we, timeout=2)


class LadbrokesBYBQuickBetSelection(BYBQuickBetSelection):
    _deposit_info_message = 'xpath=.//*[@data-crlat="infoMessage"]'

    @property
    def deposit_info_message(self):
        return LadbrokesDepositInfoMessage(selector=self._deposit_info_message, context=self._we, timeout=15)

    def wait_for_deposit_info_message(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._deposit_info_message, timeout=0) is not None and
                               self._find_element_by_selector(selector=self._deposit_info_message, timeout=0).is_displayed(),
                               name=f'{self.__class__.__name__} info panel displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)


class LadbrokesBYBBetslip(BYBBetslip):
    _quickbet_selection_type = LadbrokesBYBQuickBetSelection
