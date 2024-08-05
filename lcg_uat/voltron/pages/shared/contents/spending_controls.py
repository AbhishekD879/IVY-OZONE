import random
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from collections import OrderedDict

from voltron.pages.shared.contents.betslip.betslip_each_way import CheckBoxInput


class SpendingControlsTabContent(ComponentBase):
    _info_text = "xapth=.//*[text()='Find out more']/../preceding-sibling::div | .//*[text()='Find out more']/preceding-sibling::div"
    _find_out_more = "xpath=.//*[text()='Find out more']"

    @property
    def info_text(self):
        return self._get_webelement_text(selector=self._info_text, timeout=1)

    @property
    def find_out_more(self):
        return self._find_element_by_selector(selector=self._find_out_more, timeout=1)


class DepositLimitItem(ComponentBase):
    _set_limit_button = 'xpath=.//*[contains(@class,"underline")]//*[text()="Set Limit"] | .//*[contains(@class,"plus-icon-div")]'
    _cancel_button = 'xpath=.//*[contains(@class,"underline")]//*[text()="Cancel"]'
    _card_header = 'xpath=.//*[@id="card-header"]'
    _set_limit_input = 'xpath=.//*[@class="form-control-container"]/input'
    _edit = 'xpath=.//*[contains(@class,"underline")]//*[text()="Edit"] | .//*[contains(@class,"edit-icon")]'
    _remove = 'xpath=.//*[contains(@class,"delete-icon")] | .//*[contains(@class,"underline")]//*[text()="Remove"]'
    _limit_msg = 'xpath=.//*[@id="depositlimit-card-bottom"]//ul'

    @property
    def set_limit_button(self):
        return ButtonBase(selector=self._set_limit_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def card_header(self):
        return self._get_webelement_text(selector=self._card_header,context=self._we)

    @property
    def name(self):
        return self.card_header

    @property
    def set_limit_input(self):
        return InputBase(selector=self._set_limit_input,context=self._we)

    @property
    def edit(self):
        return ButtonBase(selector=self._edit,context=self._we)

    @property
    def remove(self):
        return ButtonBase(selector=self._remove, context=self._we)

    @property
    def limit_msg(self):
        return self._get_webelement_text(selector=self._limit_msg,context=self._we)


class SCDepositLimitTabContent(SpendingControlsTabContent):
    _item = 'xpath=.//*[contains(@class,"card--clickable card card-bg bonus-card")]'
    _list_item_type = DepositLimitItem


class SlotForMaxStakeLimit(DepositLimitItem):
    _limit_msg = 'xpath=.//*[@id="max-card-bottom"]//ul'
    _save = 'xpath=.//*[contains(@class,"btn") and contains(text(),"Save")]'
    _current_limit = 'xpath=.//*[contains(@id, "current-limit")]'

    @property
    def set_limit_button(self):
        return ButtonBase(selector=self._set_limit_button)

    @property
    def max_limit_input(self):
        return self.set_limit_input

    @property
    def save(self):
        return ButtonBase(selector=self._save)

    @property
    def current_limit(self):
        return self._get_webelement_text(selector=self._current_limit)


class SpendingControlsOverlay(SlotForMaxStakeLimit):
    _cancel_button = 'xpath=.//*[@class="underline cancel-btn cursorPointer"]'
    _save = 'xpath=.//*[contains(@class,"btn submit") and contains(text(),"Save")]'
    _deposit_curfew_pop_up = 'xpath=.//*[contains(@class,"deposit-curfew-popup-title")]'
    _close = 'xpath=.//*[contains(@class, "ui-close")]'
    _enable = 'xpath=.//*[text()="ENABLE"]'
    _curfew_confirm_button = 'xpath=.//*[text()="CONFIRM"]'
    _delete_curfew_button = 'xpath=.//*[text()="DELETE CURFEW"]'

    @property
    def curfew_confirm_button(self):
        return ButtonBase(self._curfew_confirm_button)

    @property
    def delete_curfew_button(self):
        return ButtonBase(self._delete_curfew_button)

    @property
    def curfew_enable_button(self):
        return ButtonBase(self._enable)

    @property
    def save(self):
        return ButtonBase(selector=self._save)

    @property
    def is_deposit_curfew_pop_up_displayed(self):
        return self._find_element_by_selector(selector=self._deposit_curfew_pop_up) is not None

    @property
    def close(self):
        return ButtonBase(selector=self._close, context=self._we)


class SCMaxStakeLimitTabContent(SpendingControlsTabContent):
    _item = 'xpath=.//*[contains(@class,"card--clickable card card-bg bonus-card")]'
    _list_item_type = SlotForMaxStakeLimit

    @property
    def slots_box(self):
        return self._list_item_type(selector=self._item)


class PillsList(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"sports-pill")]'
    _list_item_type = ButtonBase


class CurfewItem(ComponentBase):
    _name = 'xpath=.//*[@class="font-weight-bold bolder-dcr"]'
    _toggle = 'xpath=.//*[contains(@class,"custom-control custom-checkbox custom-control-switcher")]'
    _edit_icon = 'xpath=.//*[contains(@class,"edit-icon-div")]'
    _bin_icon = 'xpath=.//*[contains(@class,"ui-icon theme-bin")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def toggle(self):
        return ButtonBase(selector=self._toggle, context=self._we)

    @property
    def edit_icon(self):
        return ButtonBase(selector=self._edit_icon, context=self._we)

    @property
    def has_edit_icon(self):
        return self._find_element_by_selector(selector=self._edit_icon, context=self._we) is not None

    @property
    def delete_curfew(self):
        return ButtonBase(selector=self._bin_icon)


class CurfewsList(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"card card--clickable card-bg bonus-card portal-ch-task-card simple-top-margin")]'
    _list_item_type = CurfewItem

class NewCurfewDaysContainer(ComponentBase):
    _check_box = 'xpath=.//input[@formcontrolname="selected"]'
    _label = 'xpath=.//label'

    @property
    def check_box(self):
        return CheckBoxInput(selector=self._check_box, context=self._we)

    @property
    def label(self):
        return self._get_webelement_text(selector=self._label, context=self._we)


class SCDepositCurfewTabContent(SpendingControlsTabContent):
    _pills_list = 'xpath=.//*[contains(@class,"sports-pill")]/../..'
    _pills_list_type = PillsList
    _edit_curfews = 'xpath=.//*[contains(@class,"pc-text underline txt-link")]//*[text()="Edit curfews"]'
    _cancel_button = 'xpath=.//*[contains(@class,"underline")]//*[text()="Cancel"]'
    _time_zone = 'xpath=.//*[contains(text(), "zone")]'
    _add_new_curfew = 'xpath=.//*[contains(@class,"btn submit")]'
    _new_curfew_name = 'xpath=.//*[@formcontrolname="curfewNameInput"]'
    _curfew_list = 'xpath=(.//*[contains(@class,"card card--clickable card-bg bonus-card portal-ch-task-card simple-top-margin")]/..)[1]'
    _curfew_list_type = CurfewsList
    _upcoming_curfews = 'xpath=(.//*[contains(@class,"card card--clickable card-bg bonus-card portal-ch-task-card simple-top-margin")]/..)[2]'
    _upcoming_curfews_list_type = CurfewsList
    _days_container = 'xpath=.//*[@class="form-element day-margin-right"]'
    _days_container_type = NewCurfewDaysContainer
    
    @property
    def has_upcoming_curfews(self):
        return self._find_element_by_selector(selector=self._upcoming_curfews) is not None

    @property
    def upcoming_curfews_list(self):
        return self._upcoming_curfews_list_type(selector=self._upcoming_curfews)

    @property
    def new_curfew_name(self):
        return InputBase(self._new_curfew_name)

    @property
    def curfew_list(self):
        return self._curfew_list_type(selector=self._curfew_list)


    @property
    def pills_list(self):
        return self._pills_list_type(selector=self._pills_list)

    @property
    def edit_curfews(self):
        return ButtonBase(selector=self._edit_curfews)

    @property
    def time_zone(self):
        return self._get_webelement_text(selector=self._time_zone).split(':')[1].strip().strip('\n')

    @property
    def cancel(self):
        return ButtonBase(selector=self._cancel_button)

    @property
    def add_new_curfew(self):
        return ButtonBase(selector=self._add_new_curfew)

    @property
    def days(self):
        days_list = self._find_elements_by_selector(selector=self._days_container)
        res = OrderedDict()
        for item in days_list:
            container_type_item = self._days_container_type(web_element=item)
            res.update({container_type_item.label: container_type_item.check_box})
        return res

    @property
    def save_curfew(self):
        return ButtonBase(selector=self._add_new_curfew)


class SpendingControlsTabMenu(TabsMenu):
    _item = 'xpath=.//*[contains(@class,"nav-item")]'
    _list_item_type = ButtonBase


class SpendingControlsPage(ComponentBase):
    _tab_content_types = {
        'DEPOSIT LIMITS': SCDepositLimitTabContent,
        'MAX STAKE LIMIT': SCMaxStakeLimitTabContent,
        'DEPOSIT CURFEW': SCDepositCurfewTabContent
    }
    _tabs_menu = 'xpath=.//*[contains(@class,"nav nav-tabs active-primary") or contains(@class, "navigation-layout-nav-items")]'
    _tabs_menu_type = SpendingControlsTabMenu
    _tab_content = 'xpath=.//*[@id="navigation-layout-page-content"] | .//*[contains(@class,"nav nav-tabs active-primary") or contains(@class, "navigation-layout-nav-items")]/following-sibling::*[2]'
    _save = 'xpath=.//*[contains(@class,"btn") and contains(text(),"Save")]'

    @property
    def tabs_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu)

    @property
    def tab_content(self):
        tab_menu_type = self._tab_content_types.get(self.tabs_menu.current.upper())
        return tab_menu_type(selector=self._tab_content)

    @property
    def save(self):
        return ButtonBase(selector=self._save)