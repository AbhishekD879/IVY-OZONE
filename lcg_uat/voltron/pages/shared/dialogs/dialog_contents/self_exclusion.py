from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class SelfExcludeButton(ButtonBase):

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=''):
        return wait_for_result(lambda: 'inactive' not in self.get_attribute('class').strip(' ').split(' '),
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=f'"Click here" button active status is: {expected_result}')


class SelfExclusion(Dialog):
    _dialog_title = 'xpath=.//*[@data-uat="popUpTitle"]'
    _self_exclusion_button = 'xpath=.//*[@data-uat="popUpButton"]'
    _static_block = 'xpath=.//*[@data-crlat="staticBlock"]'
    _self_exclusion_period_dropdown = 'xpath=.//*[@data-crlat="selfExclusionSelect"]'
    _self_exclusion_period_dropdown_type = SelectBase
    _password_input = 'xpath=.//*[@data-crlat="passwordInput"]'
    _invalid_password = 'xpath=.//*[@data-crlat="invalidPasswordMessage"]'

    _default_action = 'close_dialog'

    @property
    def self_exclusion_period_dropdown(self):
        return self._self_exclusion_period_dropdown_type(selector=self._self_exclusion_period_dropdown)

    @property
    def dialog_title(self):
        return self._find_element_by_selector(selector=self._dialog_title)

    @property
    def static_block(self):
        return self._find_element_by_selector(selector=self._static_block)

    @property
    def self_exclude_button(self):
        return SelfExcludeButton(selector=self._self_exclusion_button, context=self._we)

    @property
    def password(self):
        return InputBase(selector=self._password_input, context=self._we)

    @property
    def invalid_password_message(self):
        return self._get_webelement_text(selector=self._invalid_password, timeout=2)


class AccountSelfExcluded(Dialog):
    pass
