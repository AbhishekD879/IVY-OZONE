from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class SpinnerButtonBase(ComponentBase):
    _local_spinner = 'xpath=.//*[contains(@class, "spinner")] ' \
                     '|.//*[local-name()="svg"][contains(@class, "spinner")] ' \
                     '| .//*[@data-crlat="spinner.loader"]'

    def has_spinner_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._local_spinner,
                                                   timeout=0) is not None,
            name=f'Spinner status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def click(self):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
        self._spinner_wait()

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=1)

    @property
    def href(self):
        return self.get_attribute('href')


class ButtonBase(SpinnerButtonBase):
    _icon = 'xpath=.//*[local-name(), "svg"]'
    _new_icon = 'xpath=.//*[@data-crlat="new-icon-popular"]'

    @property
    def has_new_icon(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._new_icon, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'"{self.__class__.__name__}" YourCall icon status to be {expected_result}')

    def _wait_active(self, timeout=0):
        """
        Internal method to wait till button/icon is active before clicking it
        """
        try:
            self._we = self._find_myself(timeout=self._timeout)
            self._wait_button_to_be_displayed()
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=2)
            self._wait_button_to_be_displayed()

    def _wait_button_to_be_displayed(self, timeout=2):
        """
        Internal method to be used on _wait_active
        Created to reduce code duplication
        """
        self.scroll_to_we()
        wait_for_result(lambda: self._we.is_displayed(),
                        name=f'{self.__class__.__name__} Button to be displayed',
                        timeout=timeout)

    def click(self, scroll_to=True):
        if scroll_to:
            self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def has_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def is_filled(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: 'filled' in self.get_attribute('class'),
                               name=f'{self.__class__.__name__} filled status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)


class QuickBetButtonBase(SpinnerButtonBase):

    def _wait_active(self, timeout=0):
        """
        Internal method to wait till button/icon is active before clicking it
        """
        try:
            self._we = self._find_myself(timeout=self._timeout)
            self._wait_button_to_be_displayed()
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=2)
            self._wait_button_to_be_displayed()

    def _wait_button_to_be_displayed(self, timeout=2):
        """
        Internal method to be used on _wait_active
        Created to reduce code duplication
        """
        self.scroll_to_we()
        wait_for_result(lambda: self._we.is_displayed(),
                        name=f'{self.__class__.__name__} Button to be displayed',
                        timeout=timeout)

    def click(self):
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')


class ButtonNoScrollBase(ButtonBase):

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass


class ImageIconBase(ButtonBase):

    @property
    def is_hyperlinked(self):
        return bool(self.href)


class IconBase(ButtonBase):

    def click(self, scroll_to=True):
        """
        Overridden as normally icons are not clickable
        """
        pass

    def _wait_active(self, timeout=0):
        """
        Internal method to wait till button/icon is active before clicking it
        """
        pass


class FavouritesIcon(ButtonBase):
    _svg = 'xpath=.//*[local-name()="svg"]'

    def is_selected(self, expected_result=True, timeout=1, poll_interval=0.5, name=None):
        button = ButtonBase(selector=self._svg, context=self._we, timeout=2)
        return button.is_selected(expected_result=expected_result,
                                  timeout=timeout,
                                  poll_interval=poll_interval,
                                  name=f'"{self.__class__.__name__}" selected state to be {expected_result}')


class DefaultBetButton(ButtonBase):
    _output_price = 'xpath=.//*[contains(@data-crlat, "combinedOutcome")]//*[@data-crlat="oddsPrice"] | .//span[not(contains(@class,"ng-hide"))]'

    @property
    def output_price(self):
        return self._get_webelement_text(selector=self._output_price, timeout=1)


class DepositSubmitButton(SpinnerButtonBase):

    def click(self, wait_for_success=True):
        self.scroll_to_we()
        click(self._we)
        self._spinner_wait() if wait_for_success else self._spinner_wait(timeout=2)


class BetNowButton(SpinnerButtonBase):
    _local_spinner = 'xpath=.//span[contains(@class, "btn-spinner")] ' \
                     '|.//*[local-name()="svg"][contains(@class, "spinner")] ' \
                     '| .//*[@data-crlat="spinner.loader"]' \
                     '| .//*[contains(@class,"betnow-spinner")]'
    _context_timeout = 5

    def click(self, timeout=_context_timeout):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')
        self._spinner_wait(timeout=timeout)

    def _spinner_wait(self, timeout=_context_timeout, expected_result=False):
        """
       Waits for spinner to disappear. Looks for spinner within current context (web element or web driver)
       :param timeout:
       :return:
       """

        def check_spinner_displayed():
            try:
                spinner = self._find_element_by_selector(selector=self._local_spinner,
                                                         context=self._context,
                                                         bypass_exceptions=(),
                                                         timeout=0)
                if spinner is None:
                    return False
                self.scroll_to_we(spinner)
                return spinner.is_displayed()
            except NoSuchElementException:
                return False
            except StaleElementReferenceException:
                return False
            except VoltronException:
                return False

        return wait_for_result(lambda: check_spinner_displayed(),
                               name=f'Local spinner displayed. Context "{self.__class__.__name__}"',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_spinner_icon(self, timeout=1, expected_result=False):
        """
        Verifies whether button spinner is located inside of button depending on expected result

        :param timeout: timeout to wait for expected result
        :param expected_result: specifies expected result for availability of icon
        :return: Spinner icon availability for button
        """

        def check_spinner_displayed():
            try:
                spinner = self._find_element_by_selector(selector=self._local_spinner,
                                                         context=self._we,
                                                         bypass_exceptions=(),
                                                         timeout=0)
                if spinner is None:
                    return False
                self.scroll_to_we(spinner)
                return spinner.is_displayed()
            except (NoSuchElementException, StaleElementReferenceException, VoltronException):
                return False

        return wait_for_result(lambda: check_spinner_displayed(),
                               name=f'Local spinner displayed. Context "{self.__class__.__name__}"',
                               expected_result=expected_result,
                               timeout=timeout)
