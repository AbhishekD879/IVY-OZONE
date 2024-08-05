from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.header import BetSlipCounter
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import has_betslip_animation
from voltron.utils.waiters import wait_for_result


class AccaNotification(ComponentBase):
    # The ACCA Notification feature has been deprecated and replaced with the ACCA Bar feature.
    # Note that the ACCA Notification feature is applicable for Double or higher bets,
    # but the ACCA Bar feature is applicable for all the bet types(including single bets).
    # We have retained the original name here because it is already extensively used
    # in numerous test cases. Renaming it will have implications across existing test suite.
    _bet_type = 'xpath=.//*[@data-crlat="betType"]'
    _bet_slip_counter_value = 'xpath=.//*[@data-crlat="betSlipCounter"]'
    # _odds = 'xpath=.//*[@data-crlat="accaPrice"]'
    # _arrow = 'xpath=.//*[@data-crlat="arrowNext"]'
    _payout = 'xpath=.//*[@data-crlat="betReturn"]'
    _selection_name = 'xpath=.//*[contains(@class, "selection-name")]'

    def _wait_active(self, timeout=15):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._bet_type,
                                           bypass_exceptions=(NoSuchElementException,), timeout=1)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()

    @property
    def bet_type(self):
        return self._get_webelement_text(selector=self._bet_type)

    # @property
    # def odds(self):
    #     return ButtonBase(selector=self._odds, context=self._we)

    @property
    def counter_value(self):
        if has_betslip_animation():
            self.wait_for_betslip_animation_disappear()
        wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bet_slip_counter_value, timeout=0, context=get_driver()).get_attribute(
                'innerHTML') != '0',
            name='Betslip counter value to have value',
            bypass_exceptions=(StaleElementReferenceException, VoltronException, AttributeError),
            timeout=1)
        try:
            result = self._find_element_by_selector(selector=self._bet_slip_counter_value, timeout=0, context=get_driver()).get_attribute('innerHTML')
        except AttributeError:
            result = ''
        if result == '':
            self._logger.warning('*** As Betslip Counter Value is not present, assuming betslip counter value is 0')
            result = '0'
        return result

    @property
    def odds_value(self):
        return self._get_webelement_text(selector=self._payout, timeout=2).split('@')[1].strip()

    def wait_for_odds_change(self):
        value = self.odds_value
        wait_for_result(lambda: value != self.odds_value,
                        timeout=2,
                        name='Waiting for odds change. Was %s.' % value)

    @property
    def payout(self):
        return self._get_webelement_text(selector=self._payout, timeout=1)

    @property
    def selection_name(self):
        return self._get_webelement_text(selector=self._selection_name, context=self._we)

    # @property
    # def arrow(self):
    #     return ComponentBase(selector=self._arrow, context=self._we, timeout=3)
