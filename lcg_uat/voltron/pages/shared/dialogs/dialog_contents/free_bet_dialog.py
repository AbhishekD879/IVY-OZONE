import re

from multidict import MultiDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog, DialogHeader
from voltron.utils.exceptions.voltron_exception import VoltronException


class FreebetDialogHeader(DialogHeader):

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=1)


class FreebetStakeContainer(ComponentBase):
    _radio_button = 'xpath=.//*[@data-crlat="freebetStakeCircle"]'
    _name = 'xpath=.//*[@data-crlat="freebetStakeName"]'

    @property
    def radio_button(self):
        return ButtonBase(selector=self._radio_button, context=self._we)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)


class FreebetStakeDialog(Dialog):
    _dialog_header_type = FreebetDialogHeader
    _header_name = 'xpath=.//*[@data-crlat="dTitle"]'
    _add_button = 'xpath= .//*[@data-crlat="remove"]'
    _list_item_type = FreebetStakeContainer
    _item = 'xpath=.//*[@data-crlat="freebetStakeContainer"]'
    _freebet_amount = 'xpath=.//*[@data-crlat="fbAmount"]'

    @property
    def name(self):
        text = self._get_webelement_text(selector=self._header_name)
        return text.split('(x')[0].strip()

    @property
    def add_button(self):
        return ButtonBase(selector=self._add_button)

    @property
    def free_bet_number(self):
        text = self._get_webelement_text(selector=self._header_name)
        if text:
            return text.split('(x')[1][:-1].strip() if '(x' in text else text.split('(')[1][:-1].strip()
        else:
            return '0'

    @property
    def freebet_amount(self):
        return self._wait_for_not_empty_web_element_text(selector=self._freebet_amount, context=self._we, timeout=1)

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = MultiDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.add(list_item.name, list_item)
        return items_ordered_dict

    def select_free_bet(self, free_bet_name, timeout=3):
        if not self.add_button.is_displayed(timeout=timeout):
            raise VoltronException("ADD button on Free Bet Dialog is not displayed. "
                                   "Can not proceed with Free Bet selection")
        for fb_name, fb in self.items_as_ordered_dict.items():
            if free_bet_name in fb_name:
                fb.radio_button.click()
                free_bet_value = re.search(r'\d+.\d+\d+', free_bet_name)
                if not self.add_button.is_enabled(timeout=timeout):
                    raise VoltronException("ADD button on Free Bet Dialog is not enabled")
                self.add_button.click()
                return free_bet_value.group()
        raise VoltronException(f'Can not select free bet "{free_bet_name}" from "{list(self.items_as_ordered_dict.keys())}"')

    def select_first_free_bet(self, timeout=5):
        if not self.add_button.is_displayed(timeout=timeout):
            raise VoltronException("ADD button on Free Bet Dialog is not displayed. "
                                   "Can not proceed with Free Bet selection")
        free_bet_name, free_bet = list(self.items_as_ordered_dict.items())[0]
        free_bet.radio_button.click()
        if not self.add_button.is_enabled(timeout=timeout):
            raise VoltronException("ADD button on Free Bet Dialog is not enabled")
        self.add_button.click()
        return free_bet_name


class ContinueWithFreebetDialog(Dialog):
    _header_name = 'xpath=.//*[@data-crlat="dTitle"]'
    _no_thanks_button = 'xpath=.//*[contains(@data-crlat,"button.No")]'
    _yes_please_button = 'xpath=.//*[contains(@data-crlat,"button.Yes")]'
    _dialog_content = 'xpath=.//*[@data-crlat="popUpText"]'
    _ok_thanks_button = 'xpath=.//*[contains(@data-crlat,"button.Ok")]'

    @property
    def ok_thanks_button(self):
        return ButtonBase(selector=self._ok_thanks_button)

    @property
    def name(self):
        text = self._get_webelement_text(selector=self._header_name)
        return text.split('(x')[0].strip()

    @property
    def no_thanks_button(self):
        return ButtonBase(selector=self._no_thanks_button)

    @property
    def yes_please_button(self):
        return ButtonBase(selector=self._yes_please_button)

    @property
    def title(self):
        text = self._get_webelement_text(selector=self._header_name)
        return text.split('(x')[0].strip()

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we).replace('\n\n', ' ').replace(
            '\n', ' ')


class FreeBetNotEligible(Dialog):
    _header_name = 'xpath=.//*[@data-crlat="dTitle"]'
    _ok_button = 'xpath=.//*[@data-crlat="button.OK"]'
    _dialog_content = 'xpath=.//*[@data-crlat="popUpText"]'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button)

    @property
    def title(self):
        text = self._get_webelement_text(selector=self._header_name)
        return text.split('(x')[0].strip()

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we).replace('\n\n', ' ').replace(
            '\n', ' ')
