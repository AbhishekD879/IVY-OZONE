from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.waiters import wait_for_result


class Settings(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/settings'
    _fractional_btn = 'xpath=.//*[@data-crlat="buttonSwitch" and *[contains(text(), "Fractional")]]'
    _decimal_btn = 'xpath=.//*[@data-crlat="buttonSwitch" and *[contains(text(), "Decimal")]]'
    _odd_format_label = 'xpath=.//*[@data-crlat="oddsFormatLabel"]'
    _allow_quick_bet_switch = 'xpath=.//*[@data-crlat="toggleSwitch"]'
    _timeline_button = 'xpath=.//*[@data-crlat="allowTimelineSwitch"]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._fractional_btn, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,))
            page_title = 'PREFERENCES'
            wait_for_result(lambda: page_title.upper() == self.header_line.page_title.sport_title.upper(),
                            timeout=1,
                            name=f'Page title: "{page_title}" displayed, '
                                 f'current page title is: "{self.header_line.page_title.sport_title}"')
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()

    @property
    def fractional_btn(self):
        return ButtonBase(selector=self._fractional_btn, context=self._we)

    @property
    def decimal_btn(self):
        return ButtonBase(selector=self._decimal_btn, context=self._we)

    @property
    def odd_format_label(self):
        return self._find_element_by_selector(selector=self._odd_format_label, context=self._we)

    @property
    def allow_quick_bet(self):
        return ButtonBase(selector=self._allow_quick_bet_switch)

    @property
    def timeline_button(self):
        return ButtonBase(selector=self._timeline_button)
