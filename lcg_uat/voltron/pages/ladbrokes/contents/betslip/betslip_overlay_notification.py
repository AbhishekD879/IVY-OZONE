from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class BetSlipOverlayNotification(ComponentBase):
    _error_message = 'xpath=.//*[@data-crlat="stake.errorMessage"]'

    @property
    def error(self):
        return self._get_webelement_text(selector=self._error_message)

    def wait_for_error(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self.error,
                               name='BetslipStake Top Overlay error message to show up/hide',
                               expected_result=expected_result,
                               timeout=timeout)
