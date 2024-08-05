from collections import OrderedDict
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.connect import Connect
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class CouponsMenu(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="tab"]'
    _active_tab = 'xpath=.//*[contains(@class, "active") and //*[@data-crlat="tab"]]'

    @property
    def current(self):
        button = self._find_element_by_selector(selector=self._active_tab, context=self._we, timeout=3)
        if button:
            return button.text
        else:
            raise VoltronException("No coupon tab is selected")

    @property
    def tab_styles(self):
        return ComponentBase(selector=self._item, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            items_ordered_dict.update({item_we.text: item_we})
        return items_ordered_dict


class InShopCouponsEventAccordion(Accordion):
    _name = 'xpath=.//*[@class="cb-results-item-left"]'
    _selections = 'xpath=.//*[@class="btn cb-odds "]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def selections(self):
        return self._find_elements_by_selector(self._selections, context=self._we)


class InShopCouponsEventGroup(ComponentBase):
    _item = 'xpath=.//*[@class="cb-results-item"]'
    _list_item_type = InShopCouponsEventAccordion
    _name = 'xpath=.//*[@class="cb-group-header"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class InShopCouponsAccordionsList(ComponentBase):
    _item = 'xpath=.//*[@class="cb-group-wrap"]'
    _list_item_type = InShopCouponsEventGroup


class GenerateBetFrame(ComponentBase):
    _generate_bet_code = 'xpath=.//*[contains(@class, "button btn btn-primary")]'
    _stake_field = 'xpath=.//*[@class="cb-accumulator-input"]'
    _bet_type = 'xpath=.//*[contains(@class, "cb-accumulator-item")]'
    _cumulative_price = 'xpath=.//*[contains(text(),"Accumulator")]//following-sibling::*[not(contains(@class, "cb-input-wrap"))]'
    _total_stake = 'xpath=.//*[text()="Total Stake"]//parent::*[contains(@class,"cb-accumulator-flex")]//child::*[contains(@class, "right")]'
    _potential_retuns_value = 'xpath=.//*[contains(@class, "potStake")]/child::div[contains(@class, "right")] | //*[text()="Potential Returns"]//parent::*[contains(@class,"cb-accumulator-flex")]/div/span'

    @property
    def generate_bet_code(self):
        return self._find_element_by_selector(selector=self._generate_bet_code)

    @property
    def is_generate_bet_code_active(self):
        attribute = self.generate_bet_code.get_attribute('class')
        active = False if 'disabled' in attribute else True
        return active

    @property
    def stake_field(self):
        return self._find_element_by_selector(selector=self._stake_field)

    @property
    def get_stake_value(self):
        return self.stake_field.get_attribute('placeholder')

    @property
    def bet_type(self):
        return TextBase(self._bet_type, context=self._we)

    @property
    def potential_returns(self):
        return TextBase(self._potential_retuns_value, context=self._we)

    @property
    def total_stake(self):
        return TextBase(self._total_stake, context=self._we)

    @property
    def cumulative_price(self):
        return TextBase(self._cumulative_price, context=self._we)


class InShopCouponsTabContent(TabContent):
    _team_name = 'xpath=.//*[@class="cb-digital-teams__home"]'
    _accordions_list = 'xpath=.//*[@class="cb-group-wrap"]'
    _accordions_list_type = InShopCouponsAccordionsList
    _generate_bet_frame = 'xpath=.//*[@class="cb-accumulator-wrap cb-accumulator-grid"]'

    @property
    def team_styles(self):
        return ComponentBase(selector=self._team_name, context=self._we)

    @property
    def generate_bet_frame(self):
        return GenerateBetFrame(selector=self._generate_bet_frame, context=self._we)


class InShopCoupons(ComponentBase):
    _back_icon = 'xpath=//*[@data-crlat="btnBack"]'
    _coupons_header_title = 'xpath=.//*[@data-crlat="titleText"]'
    _coupons_tabs_menu = 'xpath=.//*[@data-crlat="tab.tpTabs"]'
    _saved_bet_codes = 'xpath=.//*[@class="header-mybets"]'
    _tab_content = 'xpath=.//*[@id="cb-static-container"]'
    _tab_content_type = InShopCouponsTabContent
    _footer_text_on_digital_coupons_page = 'xpath=.//*[contains(@class, "cb-footer-message-text")]'

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)

    @property
    def back_icon(self):
        return ButtonBase(selector=self._back_icon, context=self._we)

    @property
    def title(self):
        return self._find_element_by_selector(self._coupons_header_title, context=self._we)

    @property
    def title_styles(self):
        return ComponentBase(selector=self._coupons_header_title, context=self._we)

    @property
    def coupons_tabs_menu(self):
        return CouponsMenu(selector=self._coupons_tabs_menu, context=self._we)

    @property
    def saved_bet_codes(self):
        return ButtonBase(selector=self._saved_bet_codes, context=self._we)

    @property
    def footer_text(self):
        return TextBase(self._footer_text_on_digital_coupons_page, context=self._we)


class SavedBetCodes(ComponentBase):
    _title_text = 'xpath=.//*[@data-crlat="titleText"]'
    _btn_back = 'xpath=.//*[@data-crlat="btnBack"]'

    @property
    def title(self):
        return self._find_element_by_selector(selector=self._title_text, context=self._we)


class TheGrid(Connect):
    _upgrade_account = 'xpath=.//*[@class="build-card-button"] | .//*[@data-crlat="upgradeButton"]'

    @property
    def upgrade_account(self):
        return self._find_element_by_selector(selector=self._upgrade_account, context=self._we)


class SetPinCode(ComponentBase):
    _enter_pin = 'xpath=.//*[@name="virtucalcardpin"]'
    _confirm_pin = 'xpath=.//*[@name="confirmVirtualCardPin"]'
    _submit = 'xpath=.//*[contains(@class,"btn btn-primary")]'

    @property
    def enter_pin(self):
        return InputBase(selector=self._enter_pin, context=self._we)

    @property
    def confirm_pin(self):
        return InputBase(selector=self._confirm_pin, context=self._we)

    @property
    def submit_button(self):
        return ButtonBase(selector=self._submit, context=self._we)


class MyGridCard(ComponentBase):
    _header = 'xpath=.//*[@class="header-ctrl-txt"]'
    _grid_virtual_card = 'xpath=.//*[@class="flip-card"]'
    _finish_button = 'xpath=.//*[contains(@class,"btn btn-primary")]'

    @property
    def header(self):
        return self._get_webelement_text(selector=self._header)

    @property
    def has_grid_virtual_card(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._grid_virtual_card, timeout=0) is not None,
            name=f'Grid virtual card status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def finish_button(self):
        return self._find_element_by_selector(selector=self._finish_button, timeout=1)


class GenerateGridCard(ComponentBase):
    _generate_grid_card_title = 'xpath=.//*[@class="connect-card-heading"]'
    _no_thanks_button = 'xpath=.//*[contains(@class, "btn btn-secondary")]'
    _generate_button = 'xpath=.//*[contains(@class, "btn btn-primary")]'
    _grid_card_page_content = 'xpath=.//*[@class="dlg-responsive-content"]'

    @property
    def generate_grid_card_title(self):
        return self._get_webelement_text(selector=self._generate_grid_card_title)

    @property
    def no_thanks_button(self):
        return self._find_element_by_selector(selector=self._no_thanks_button, context=self._we)

    @property
    def generate_button(self):
        return self._find_element_by_selector(selector=self._generate_button, context=self._we)

    @property
    def setpincode(self):
        return SetPinCode(selector=self._grid_card_page_content)

    @property
    def my_grid_card(self):
        return MyGridCard(selector=self._grid_card_page_content)

