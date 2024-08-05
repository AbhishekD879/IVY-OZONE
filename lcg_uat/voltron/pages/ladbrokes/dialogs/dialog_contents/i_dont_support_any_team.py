from voltron.pages.ladbrokes.dialogs.dialog_contents.team_Confirmation import TeamConfirmation
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.js_functions import mouse_event_click as safari_click
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.base import ComponentBase


class IDontSupportAnyTeam(TeamConfirmation):
    _custom_team_name_input = 'xpath=.//*[@name="customTeamName"]'
    _exit_button = 'xpath=.//*[contains(@class,"SYC-Popup__ctaButton--ctaPrimaryBtn")]'
    _login_to_confirm = 'xpath=.//*[contains(@class,"SYC-Popup__ctaButton--ctaSecondaryBtn")]'

    @property
    def exit_button(self):
        return ButtonBase(selector=self._exit_button, timeout=5)

    @property
    def login_to_confirm_button(self):
        return ButtonBase(selector=self._login_to_confirm, timeout=5)

    @property
    def select_custom_team_name_input(self):
        return self._find_element_by_selector(selector=self._custom_team_name_input, context=self._we)

    @select_custom_team_name_input.setter
    def select_custom_team_name_input(self, value):
        we = self._find_element_by_selector(selector=self._custom_team_name_input, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    def is_underscored_red(self, expected_result=True):
        free_text_box = ComponentBase(selector=self._custom_team_name_input, context=self._we, timeout=1)
        result = wait_for_result(lambda: free_text_box.css_property_value('border-bottom') == '1px solid rgb(240, 30, 40)',
                                 name=f'{self.__class__.__name__} – free text box is highlighted in red',
                                 expected_result=expected_result,
                                 timeout=2)
        return result
