from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.registration.primitives.input import RegistrationInputWithToggleIcon


class ChangePasswordHeader(ComponentBase):
    _close_button = 'xpath=.//*[contains(@class,"ui-close")]'
    _back_button = 'xpath=.//*[contains(@class,"ui-back")]'
    _title = 'xpath=//*[contains(@class,"navigation-layout-page-title")] | .//*[contains(@class,"header-ctrl-txt")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def title(self):
        return TextBase(selector=self._title, context=self._we)


class ChangePassword(BaseContent):
    _url_pattern = '^http[s]?:\/\/.+\/changepassword'
    _submit_password_button = 'xpath=.//*[contains(text()," Submit ")]'
    _old_password = 'xpath=.//*[@id="oldpassword"]'
    _new_password = 'xpath=.//*[@id="newpassword"]'
    _confirm_password_changed_msg = 'xpath=.//*[@class="cms-container"]|.//vn-message-panel[@class="cms-container"]'
    _header = 'xpath=.//lh-header-bar | .//*[@id="navigation-layout-page"] | .//vn-header-bar[@class]'
    _header_type = ChangePasswordHeader
    _verify_spinner = True

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we)

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit_password_button, context=self._we)

    @property
    def old_password(self):
        return RegistrationInputWithToggleIcon(selector=self._old_password, context=self._we)

    @property
    def new_password(self):
        return RegistrationInputWithToggleIcon(selector=self._new_password, context=self._we)

    @property
    def confirm_password_changed_message(self):
        return self._wait_for_not_empty_web_element_text(selector=self._confirm_password_changed_msg, timeout=1)
