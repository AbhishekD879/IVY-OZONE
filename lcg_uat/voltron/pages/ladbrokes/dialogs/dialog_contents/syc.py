from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class SYC(Dialog):
    _syc_description = 'xpath=.//*[@class="SYT-Popup-text"]'
    _imin_button = 'xpath=.//*[@class="i-m-in"]'
    _remind_later_button = 'xpath=.//*[@class="remind-later"]'
    _dont_show_me_button = 'xpath=.//*[@class="dont-show-me"]'
    _team_color_icon = 'xpath=.//*[@class="SYT-Popup-img"]'

    @property
    def syc_description(self):
        return self._get_webelement_text(selector=self._syc_description, timeout=5)

    @property
    def imin_button(self):
        return ButtonBase(selector=self._imin_button, timeout=5)

    @property
    def remind_later_button(self):
        return ButtonBase(selector=self._remind_later_button, timeout=5)

    def has_remind_later_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._remind_later_button, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Remind Later Button status to be "{expected_result}"')

    @property
    def dont_show_me_button(self):
        return ButtonBase(selector=self._dont_show_me_button, timeout=5)

    @property
    def team_color_icon(self):
        return self._find_element_by_selector(selector=self._team_color_icon, timeout=5)

