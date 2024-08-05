from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.waiters import wait_for_result


class RegistrationInput(ComponentBase):
    _input = 'xpath=.//input[not (contains(@type, "hidden"))]'
    _input_type = InputBase
    _validation_message = 'xpath=.//*[(@class="m2-validation-message")]'

    @property
    def input(self):
        return self._input_type(selector=self._input, context=self._we)

    def has_error_message(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(self._validation_message, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Error message to be {expected_result}')

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._validation_message)


class RegistrationInputWithToggleIcon(RegistrationInput):
    _toggle_icon = 'xpath=.//*[contains(@class, "toggle-password-button")]'
    _toggle_icon_type = ButtonBase

    @property
    def toggle_icon_button(self):
        return self._toggle_icon_type(selector=self._toggle_icon, context=self._we)
