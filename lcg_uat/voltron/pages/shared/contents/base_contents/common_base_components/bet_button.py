from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import has_betslip_animation
from voltron.utils.waiters import wait_for_result


class BetButton(ButtonBase):
    _outcome_price = 'xpath=.//*[@data-crlat="oddsPrice"]'
    _handicap = 'xpath=.//*[@class="handicap-btn"]'

    @property
    def selection_id(self):
        return self.get_attribute('id').replace('bet-', '')

    @property
    def handicap_value(self):
        return ButtonBase(selector=self._handicap, timeout=0.5)

    @property
    def outcome_price_text(self):
        return self._get_webelement_text(selector=self._outcome_price, timeout=0.5)

    def click(self, scroll_to=True):
        self._logger.debug('*** Clicking on bet button... %s' % self.outcome_price_text)
        if not self.is_safari:
            self.scroll_to_we() if scroll_to else None
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException('Can not click on %s. %s' % (self.__class__.__name__, e))
        if has_betslip_animation():
            self.wait_for_betslip_animation_disappear()

    def is_price_changed(self,
                         expected_price: str,
                         timeout: int = 1,
                         poll_interval: float = 0.5,
                         bypass_exceptions: tuple = (NoSuchElementException, StaleElementReferenceException)) -> bool:
        """
        Waiting for price on Bet Button to be changed
        :param expected_price: Price that is expected
        :param timeout: Max time to wait for expected price
        :param poll_interval: Frequency of checking the price
        :param bypass_exceptions: Exceptions to bypass
        :return: True if price changed, False otherwise
        """
        result = wait_for_result(lambda: all((self.outcome_price_text,
                                              self.outcome_price_text == expected_price)),
                                 expected_result=True,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name='Bet button price to change',
                                 bypass_exceptions=bypass_exceptions)
        return result

    @property
    def is_price_up(self):
        result = wait_for_result(lambda: 'bet-up' in self.get_attribute('class'),
                                 expected_result=True,
                                 name='Bet button price up',
                                 timeout=3)
        return result

    @property
    def is_price_down(self):
        result = wait_for_result(lambda: 'bet-down' in self.get_attribute('class'),
                                 expected_result=True,
                                 name='Bet button price down',
                                 timeout=3)
        return result


class RacingBetButton(BetButton):

    @property
    def name(self):
        return self.outcome_price_text

    @property
    def outcome_price(self):
        return TextBase(selector=self._outcome_price, context=self._we, timeout=2)
