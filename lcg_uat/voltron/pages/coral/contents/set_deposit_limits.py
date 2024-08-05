from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.text_labels import TextBase, LinkBase
from voltron.pages.coral.menus.right_menu import CoralRightMenuHeader
from voltron.utils.waiters import wait_for_result


class CoralDepositLimitsField(ComponentBase):
    _label = 'xpath=.//label[contains(@class, "form-group-label") and contains(@class, "floating-label")]'
    _input_field = 'xpath=.//input[contains(@class, "form-control-f-w")]'
    _icon = 'xpath=.//i[contains(@class, "ui-icon")]'
    _current_limit = 'xpath=.//*[contains(@class, "current-limit")]'
    _warning = 'xpath=.//*[contains(@class, "custom-warning")]'

    @property
    def current_limit(self):
        return TextBase(selector=self._current_limit, context=self._we)

    @property
    def warning_message(self):
        return TextBase(selector=self._warning, context=self._we)

    @property
    def input_field(self):
        return InputBase(selector=self._input_field, context=self._we)


class CoralSetDepositLimitsPopUp(ComponentBase):
    _popup_header = 'xpath=.//div[@class="cms-container"]//h3'
    _popup_message = 'xpath=.//div[@class="cms-container"]'
    _popup_link = 'xpath=.//div[@class="cms-container"]//a'

    def _wait_active(self, timeout=3):
        self._we = self._find_myself(timeout=timeout)
        wait_for_result(lambda: self._we.size.get('height') > 30 and self._we.size.get('width') > 75,
                        timeout=timeout,
                        name='Set Deposit Limits pop-up to appear in loaded size')

    @property
    def header(self):
        return TextBase(selector=self._popup_header, context=self._we)

    @property
    def popup_text(self):
        text_with_header = self._get_webelement_text(selector=self._popup_message, context=self._we)
        text_without_header = text_with_header.split('\n')[-1]  # removing header part
        text_to_return = text_without_header.split(' Cancel')[0]  # removing link part
        return text_to_return

    @property
    def link(self):
        return LinkBase(selector=self._popup_link, context=self._we)


class CoralSetDepositLimitsSuccessPopup(ComponentBase):
    _popup_message = 'xpath=.//*[contains(@class, "theme-check")]'

    @property
    def message(self):
        return TextBase(selector=self._popup_message, context=self._we)


class CoralCancelLimitChangeRequest(ComponentBase):
    _header = 'xpath=.//*[contains(@class, "header-ctrl-wrapper")]'
    _text = 'xpath=.//mat-dialog-content[@class="mat-dialog-content"]'
    _yes_button = 'xpath=.//*[contains(@class, "btn-primary") and contains(text(), "Yes")]'
    _no_button = 'xpath=.//*[contains(@class, "btn-light") and contains(text(), "No")]'

    @property
    def header(self):
        return TextBase(selector=self._header, context=self._we)

    @property
    def message(self):
        return TextBase(selector=self._text, context=self._we)

    @property
    def yes_button(self):
        return ButtonBase(selector=self._yes_button, context=self._we)

    @property
    def no_button(self):
        return ButtonBase(selector=self._no_button, context=self._we)


class CoralSetDepositLimits(CoralRightMenuHeader):

    _url_pattern = '^http[s]?:\/\/.+\/depositlimits'
    _header = 'xpath=.//*[@class="set-limits-header"]'
    _text_info = 'xpath=.//*[@class="limit-text-info"]'
    _deposit_limit_daily = 'xpath=.//*[contains(@class, "DAILY") and contains(@class, "deposit-limit")]'
    _deposit_limit_weekly = 'xpath=.//*[contains(@class, "WEEKLY") and contains(@class, "deposit-limit")]'
    _deposit_limit_monthly = 'xpath=.//*[contains(@class, "MONTHLY") and contains(@class, "deposit-limit")]'
    _save_button = 'xpath=.//button[contains(@class, "w-100") and contains(@class, "save")]'
    _message_popup = 'xpath=.//div[contains(@class, "message-panel")]/div[contains(@class, "theme-info-i")]'
    _success_popup = 'xpath=.//*[contains(@class, "message-panel")][.//div[contains(@class, "theme-check")]]'
    _remove_limits_button = 'xpath=.//*[contains(@class, "remove")]//*[contains(@class, "btn-primary")]'

    @property
    def header(self):
        return ComponentBase(selector=self._header, context=self._we)

    @property
    def daily_field(self):
        return CoralDepositLimitsField(selector=self._deposit_limit_daily, context=self._we)

    @property
    def weekly_field(self):
        return CoralDepositLimitsField(selector=self._deposit_limit_weekly, context=self._we)

    @property
    def monthly_field(self):
        return CoralDepositLimitsField(selector=self._deposit_limit_monthly, context=self._we)

    @property
    def save_button(self):
        return ButtonBase(selector=self._save_button, context=self._we)

    @property
    def message_popup(self):
        return CoralSetDepositLimitsPopUp(selector=self._message_popup, context=self._we)

    @property
    def success_popup(self):
        return CoralSetDepositLimitsSuccessPopup(selector=self._success_popup, context=self._we)

    @property
    def remove_limits(self):
        return ButtonBase(selector=self._remove_limits_button, context=self._we)
