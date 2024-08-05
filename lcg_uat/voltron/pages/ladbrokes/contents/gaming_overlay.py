from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.helpers import switch_to_iframe, switch_to_main_page
from voltron.utils.waiters import wait_for_result


class LadbrokesGamingHeader(ComponentBase):
    _close_btn = 'xpath=.//*[contains(@class, "theme-close-button")]'
    _title = 'xpath=.//*[contains(@class, "game-overlay")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_btn, timeout=5, context=self._we)

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)


class LadbrokesGamingOverlay(ComponentBase):
    _header = 'xpath=.//*[contains(@class, "sports-header-title-overlay")]'
    _iframe = 'xpath=.//iframe[contains(@class, "isVisible")]'
    _gaming_spinner = 'xpath=.//spinner[contains(@class, "ng-star-inserted")]'

    def stick_to_iframe(self):
        switch_to_iframe(self._iframe, timeout=20)
        return self

    @staticmethod
    def switch_to_main_page():
        switch_to_main_page()

    @property
    def header(self):
        return LadbrokesGamingHeader(selector=self._header, timeout=5)

    def wait_for_gaming_spinner_to_hide(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._gaming_spinner,
                                                   timeout=0) is None,
            name=f'Spinner should be hidden "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
