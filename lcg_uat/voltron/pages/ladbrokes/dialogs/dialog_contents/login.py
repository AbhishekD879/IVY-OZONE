from voltron.pages.shared.dialogs.dialog_contents.login import LogIn
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class LadbrokesLogInDialog(LogIn):
    _join_us_button = 'xpath=.//button[contains(text(), "REGISTER")]'
    _connect_card_toggle = 'xpath=.//a[contains(text(),"Grid")]'

    @property
    def online_toggle(self):
        return LadbrokesLoginToggleButton(selector=self._online_toggle, context=self._we)

    @property
    def connect_card_toggle(self):
        return LadbrokesLoginToggleButton(selector=self._connect_card_toggle, context=self._we)


class LadbrokesLoginToggleButton(ButtonBase):

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: '2px solid rgb(43, 43, 43)' in self.css_property_value('border'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result
