# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class LimitOption(ComponentBase):
    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class OtherLimitInput(InputBase):

    @property
    def value(self):
        value = self.get_attribute('value')
        if not value:
            return self.get_attribute('placeholder')
        return value

    @value.setter
    def value(self, value):
        self.scroll_to_we()
        self._we.clear()
        self._we.send_keys(value)
        self._we.send_keys(Keys.SHIFT + Keys.TAB)


class DepositLimitRow(SelectBase):
    _other_deposit_limit = 'xpath=.//*[@data-crlat="custom.userLimitsData"]'
    _error_message = 'xpath=.//*[@data-crlat="errorBlock.depositLimit"]'
    _pending_deposit_limit = 'xpath=.//*[@data-crlat="pending.userLimitsData"]'

    def has_other_limit(self, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(
            selector=self._other_deposit_limit, timeout=0) is not None,
            name='Other limit shown status is %s' % expected_result,
            timeout=2,
            expected_result=expected_result)

    @property
    def other_limit(self):
        return OtherLimitInput(selector=self._other_deposit_limit, context=self._we)

    @property
    def pending_limit_message(self):
        return self._get_webelement_text(selector=self._pending_deposit_limit)

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._error_message, timeout=3)


class DepositLimit(SelectBase):
    _item = 'xpath=.//option'
    _list_item_type = LimitOption
    # todo: change after merge
    _deposit_row = 'xpath=.//ancestor::div[@data-crlat="row.middle"]'

    @property
    def deposit_row(self):
        return DepositLimitRow(selector=self._deposit_row, context=self._we)


class DepositLimits(Accordion):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _current_deposit_limit = 'xpath=.//*[@data-crlat="current.userLimitsData"]'
    _select_deposit_limit = 'xpath=.//*[@data-crlat="userLimitsData"]'
    _update_deposit_limits_button = 'xpath=.//*[@data-crlat="updateDepositLimits"]'
    _note = 'xpath=.//*[@data-crlat="label.increasingLimits"]'
    _info_panel = 'xpath=.//*[@data-crlat="infPan.msg"]'

    @property
    def title(self):
        return self.section_header.text

    @property
    def _select_deposit_limits_we(self):
        return self._find_elements_by_selector(selector=self._select_deposit_limit)

    @property
    def limit_options_number(self):
        return len(self._select_deposit_limits_we)

    @property
    def daily_limit(self):
        return DepositLimit(web_element=self._select_deposit_limits_we[0], context=self._we)

    @property
    def weekly_limit(self):
        return DepositLimit(web_element=self._select_deposit_limits_we[1], context=self._we)

    @property
    def monthly_limit(self):
        return DepositLimit(web_element=self._select_deposit_limits_we[2], context=self._we)

    @property
    def update_deposit_limits_button(self):
        return ButtonBase(selector=self._update_deposit_limits_button, context=self._we)

    @property
    def note_text(self):
        return self._find_element_by_selector(selector=self._note).text

    def wait_info_panels(self):
        return wait_for_result(lambda: self._find_element_by_selector(
            selector=self._info_panel, timeout=0).is_displayed(),
            name='Info panel shown',
            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, AttributeError),
            timeout=15)

    @property
    def info_panels_text(self):
        self.wait_info_panels()
        info_texts = InfoPanel(selector=self._info_panel, context=self._we, timeout=30).texts
        return info_texts


class SessionLimits(Accordion):
    _session_limit_msg = 'xpath=.//*[@data-crlat="sessionLimitHint"]'
    _new_session_limit_saved_msg = 'xpath=.//*[contains(@data-crlat, "panelSessionMessage")]'
    _update_session_limits = 'xpath=.//*[@data-crlat="submit"]'
    _limit_options = 'xpath=.//*[@data-crlat="sessionLimitsValues"]'
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'

    @property
    def session_limit_message(self):
        return TextBase(selector=self._session_limit_msg, context=self._we)

    @property
    def new_session_limit_saved_msg(self):
        message = self._find_element_by_selector(selector=self._new_session_limit_saved_msg, timeout=0)
        result = wait_for_result(lambda: message.is_displayed() and message.text != '',
                                 name='Waiting for "Limits Saved" message appears',
                                 timeout=5)
        if not result:
            raise VoltronException('"Limits Saved" message is not shown')
        return TextBase(web_element=message)

    @property
    def update_session_limits(self):
        return ButtonBase(selector=self._update_session_limits, context=self._we)

    @property
    def limit_options(self):
        return SelectBase(selector=self._limit_options)

    @property
    def title(self):
        return self.section_header.text


class GamePlayReminder(DepositLimits):
    _select_game_play_reminder = 'xpath=.//*[@data-crlat="gameplayValues"]'
    _confirm_button = 'xpath=.//*[@data-crlat="submit"]'
    _description = 'xpath=.//*[@data-crlat="gameplayText"]'
    _title = 'xpath=.//*[@data-crlat="containerHeader"]'
    _label = 'xpath=.//*[@data-crlat="gamePlayLabel"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def label(self):
        return self._get_webelement_text(selector=self._label)

    @property
    def confirm_button(self):
        return ButtonBase(selector=self._confirm_button)

    @property
    def select_game_play_reminder(self):
        return SelectBase(selector=self._select_game_play_reminder)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description)


class Limits(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/limits'
    _deposit_limits = 'xpath=.//*[contains(@data-crlat, "section.depositLimits")]/*[@data-crlat="accordion"]'
    _session_limits = 'xpath=.//*[contains(@data-crlat, "section.sessionLimits")]/*[@data-crlat="accordion"]'
    _game_play_reminder = 'xpath=.//*[contains(@data-crlat, "section.gamePlayLimits")]/*[@data-crlat="accordion"]'

    def _wait_active(self, timeout=0):
        self._find_element_by_selector(selector=self._session_limits, context=get_driver())

    @property
    def deposit_limits(self):
        return DepositLimits(selector=self._deposit_limits)

    @property
    def session_limits(self):
        return SessionLimits(selector=self._session_limits)

    @property
    def game_play_reminder(self):
        return GamePlayReminder(selector=self._game_play_reminder)
