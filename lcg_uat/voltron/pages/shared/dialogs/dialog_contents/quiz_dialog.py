from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class QuizDialogOnLogin(Dialog):
    _default_action = 'click_dont_show_again'
    _name = 'xpath=.//*[@data-crlat="dTitle"]'
    _remind_me_later = 'xpath=.//*[@data-crlat="button.Remind me later"]'
    _yes_button = 'xpath=.//*[@data-crlat="button.Yes"]'
    _dont_show_again = 'xpath=.//*[@data-crlat="button.Don\'t show me again"]'
    _dialog_content = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we).replace('\n\n', ' ').replace(
            '\n', ' ')

    @property
    def dont_show_again(self):
        return ButtonBase(selector=self._dont_show_again, context=self._we)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=3)

    @property
    def remind_me_later(self):
        return ButtonBase(selector=self._remind_me_later, context=self._we)

    @property
    def yes_button(self):
        return ButtonBase(selector=self._yes_button, context=self._we)
