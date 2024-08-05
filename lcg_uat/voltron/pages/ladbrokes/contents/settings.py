from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared.contents.settings import Settings


class SettingsLadbrokes(Settings):
    _header_line = 'xpath=.//header[@data-crlat="header"]'
    _fractional_btn = 'xpath=.//*[@data-crlat="radioSwitch" and contains(text(), "Fractional")]'
    _decimal_btn = 'xpath=.//*[@data-crlat="radioSwitch" and contains(text(), "Decimal")]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._fractional_btn, context=self._context,
                                           bypass_exceptions=(NoSuchElementException))
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()
