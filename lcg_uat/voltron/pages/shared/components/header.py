import logging
import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

from voltron.pages.shared import get_driver, get_platform, get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import has_betslip_animation
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class BrandLogo(ComponentBase):

    def scroll_to_we(self, web_element=None):
        if web_element is None:
            self._logger.debug(f'*** Nothing passed to scroll function, '
                               f'scrolling to current web element "{self.__class__.__name__}"')
            web_element = self._we
        scroll_to_center_of_element(web_element)

    # we don't need to scroll to Coral logo webelement as it is always present in view
    def click(self):
        self.scroll_to_we()
        self.perform_click()


class BetSlipCounter(ComponentBase):
    _bet_slip_counter_value = 'xpath=.//*[@data-crlat="betSlipCounter"]'
    _logger = logging.getLogger('voltron_logger')
    def __init__(self, *args, **kwargs):
        # Patch for Skipped Component Base
        print('*** Construct new betSlipCounter object Skipped Component Base ***')

    @property
    def is_safari(self):
        if get_platform() == 'ios':
            return True
        else:
            return (get_device_properties()['browser'].lower() in ['safari', 'chromium'] and
                    'iphone' in get_device_properties()['device'].lower())

    def scroll_to_we(self, web_element=None):
        if web_element is None:
            self._logger.debug(f'*** Nothing passed to scroll function, scrolling to current web element "{self.__class__.__name__}"')
            web_element = self._we
        scroll_to_center_of_element(web_element)

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)) -> bool:
        _betslip_notification = 'xpath=.//*[contains(@class,"betslip-notification")]'
        self._we = ComponentBase(selector=_betslip_notification, context=get_driver(), timeout=5)._we
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        self.scroll_to_we() if scroll_to else None
        if self.is_safari:
            return True if self._we else False
        result = wait_for_result(lambda: self._we.is_displayed(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=bypass_exceptions,
                                 name=name)
        return result


    @property
    def counter_value(self):
        counter = get_driver().execute_script("return JSON.parse(localStorage.getItem('OX.betSelections'))")
        if not counter:
            return "0"
        else:
            return str(len(counter))
        # This patch Represent BetSlipCounter Not Working in new release
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

    def click(self):
        _betslip_notification = 'xpath=.//*[contains(@class,"betslip-notification")]'
        return ComponentBase(selector=_betslip_notification, context=get_driver(), timeout=5).click()


class ShowRightMenuButton(ButtonBase):
    _amount = 'xpath=.//*[contains(@data-crlat, "balanceAmount")]'
    _has_freebet_icon = 'xpath=.//*[@data-crlat="freeBetIcon"]'
    _context_timeout = 1

    @property
    def amount(self):
        return self.parsed_amount[1]

    @property
    def parsed_amount(self):
        matched = re.match(r'^(£|\$|€|Kr|US\$)([0-9.,]+)$', self.amount_str, re.U)
        if matched is not None and matched.group(2) is not None:
            currency_symbol = matched.group(1)
            amount = float(matched.group(2))
            return currency_symbol, amount
        else:
            raise VoltronException(f'Failed parsing amount string: "{self.amount_str}"')

    def has_amount(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._amount_we is not None and self._amount_we.is_displayed(),
            name=f'Amount status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def amount_str(self):
        self.has_amount(timeout=20)
        return self._amount_we.get_attribute('innerHTML')

    @property
    def _amount_we(self):
        amount_we = self._find_element_by_selector(selector=self._amount, timeout=2)
        if not amount_we:
            raise VoltronException('Cannot get Amount value')
        return amount_we

    def is_amount_truncated(self):
        return self.is_truncated(selector=self._amount)

    @property
    def currency_symbol(self):
        return self.parsed_amount[0]

    def click(self, scroll_to=True):
        self.scroll_to_we() if scroll_to else None
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
        time.sleep(2)

    @property
    def has_freebet_icon(self):
        return self._find_element_by_selector(selector=self._has_freebet_icon, timeout=1, context=self._we) is not None


class GlobalHeader(ComponentBase):
    _brand_logo = 'xpath=.//*[@data-crlat="headerLogo"]'
    _brand_logo_type = BrandLogo
    _sign_in = 'xpath=.//*[@data-crlat="signInButton"]'
    _join_us = 'xpath=.//*[@data-crlat="joinNowButton"]'
    _bet_slip_counter = 'xpath=.//*[@data-uat="betSlipBtn"]'
    _show_right_menu_button = 'xpath=.//*[@data-crlat="rightMenuBtn"]'
    _show_right_menu_button_type = ShowRightMenuButton
    _avatar = 'xpath=.//*[local-name() = "svg"][@data-crlat="accountIcon"]'
    _my_bets = 'xpath=.//*[@data-crlat="myBetsBtn"]'
    _betslip_notification = 'xpath=.//*[contains(@class,"betslip-notification")]'
    _freebet_info = 'xpath=.//*[contains(@class,"badge-circle") and contains(text(),"FB")] | //span[contains(text(), "FB")]'
    _freebet_info_type = IconBase

    @property
    def brand_logo(self):
        return self._brand_logo_type(selector=self._brand_logo, context=self._we, timeout=2)

    @property
    def sign_in(self):
        context = ButtonBase(selector=self._sign_in, context=self._we, timeout=15)
        context.is_displayed()
        return context

    @property
    def join_us(self):
        context = ButtonBase(selector=self._join_us, context=self._we, timeout=3)
        context.is_displayed()
        return context

    @property
    def right_menu_button(self):
        return self._show_right_menu_button_type(selector=self._show_right_menu_button, context=self._we, timeout=0.5)

    @property
    def user_balance(self):
        return self.right_menu_button.amount

    def has_right_menu(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_right_menu_button, timeout=0.5) is not None,
            name=f'{self.__class__.__name__} Right Menu status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def bet_slip_counter(self):
        try:
            bet_slip_counter = BetSlipCounter(selector=self._betslip_notification, timeout=5, context=get_driver())
        except VoltronException:
            bet_slip_counter = BetSlipCounter(selector=self._betslip_notification, timeout=5, context=get_driver())
        return bet_slip_counter

    def has_bet_slip_counter(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_right_menu_button, timeout=0).is_displayed(),
            name=f'{self.__class__.__name__} Betslip counter status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def avatar(self):
        return ComponentBase(selector=self._avatar, context=self._we, timeout=2)

    @property
    def my_bets(self):
        return ButtonBase(selector=self._my_bets, timeout=2, context=self._we)

    def has_log_in_button(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._sign_in, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'{self.__class__.__name__} Login Button displayed status to be {expected_result}')

    @property
    def freebet_info(self):
        return self._freebet_info_type(selector=self._freebet_info, context=self._we, timeout=0.5)

    def has_freebets(self, expected_result=True, timeout=5, on_betslip=False):
        result = wait_for_result(lambda: self.freebet_info.is_displayed(timeout=0),
                                 name=f'Freebet info display status to become "{expected_result}"',
                                 expected_result=expected_result,
                                 bypass_exceptions=(VoltronException, AttributeError, StaleElementReferenceException, NoSuchElementException),
                                 timeout=timeout)
        if not expected_result and on_betslip:  # to handle case when we need to check that freebet info in app header is not visible when betslip is opened
            try:
                self.freebet_info.click()
            except Exception as e:
                if 'element click intercepted' in str(e):
                    return False
                else:
                    raise VoltronException(e)
        else:
            return result

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        wait_for_result(lambda: self._we.is_displayed(),
                        name='Waiting for header to be visible',
                        timeout=5)
