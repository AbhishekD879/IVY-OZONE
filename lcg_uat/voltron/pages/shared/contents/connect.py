from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.menu_carousel import MenuCarousel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import mouse_event_click as safari_click


class ConnectOptionItem(ComponentBase):
    _item_name = 'xpath=.//*[@data-crlat="title"]'
    _item_icon = 'xpath=.//*[@data-crlat="icon"]'

    @property
    def name(self):
        return self.item_name

    @property
    def item_name(self):
        self.scroll_to_we()
        return self._get_webelement_text(selector=self._item_name, context=self._we, timeout=1).split('\n')[0]

    @property
    def item_icon(self):
        self.scroll_to_we()
        return ButtonBase(selector=self._item_icon, context=self._we)


class Connect(BaseContent):
    menu_carousel_items = ['HOME', 'BENEFITS', 'SIGN UP', 'FAQ']
    _url_pattern = r'^https?:\/\/.+\/retail'
    _menu_items_container = 'xpath=.//*[@data-crlat="pageContainer"]'
    _item = 'xpath=.//*[@data-crlat="menu.listItem"]'
    _fade_out_overlay = True
    _verify_spinner = True

    def _wait_active(self, timeout=0):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._item, context=self._context, timeout=3),
            name='Connect - ConnectOptionItem Items to load',
            timeout=3)

    @property
    def menu_carousel(self):
        return MenuCarousel(context=self._we)

    @property
    def menu_items(self):
        return MenuItems(selector=self._menu_items_container, context=self._we)


class MenuItems(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="menu.listItem"]'
    _list_item_type = ConnectOptionItem

    def _wait_active(self, timeout=0):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._item, context=self._context, timeout=3),
            name='MenuItems(Connect) - ConnectOptionItem Items to load',
            timeout=3)


class BetTabs(ComponentBase):
    _open_in_shop_bet_tab = 'xpath=.//*[@id="open_bet_tab"]'
    _settle_in_shop_bet_tab = 'xpath=.//*[@id="closed_bet_tab"]'
    _open_in_shop_bet_tab_active = 'xpath=.//*[@class="bet-tab bet-tab--active" and //*[@id="open_bet_tab"]]'
    _settle_in_shop_bet_tab_active = 'xpath=.//*[@class="bet-tab bet-tab--active" and //*[@id="closed_bet_tab"]]'

    @property
    def open_in_shop_bet_tab(self):
        return self._find_element_by_selector(selector=self._open_in_shop_bet_tab, context=self._we)

    @property
    def shop_bet_tab_styles(self):
        return ComponentBase(selector=self._open_in_shop_bet_tab, context=self._we)

    @property
    def settle_bet_tab_styles(self):
        return ComponentBase(selector=self._settle_in_shop_bet_tab, context=self._we)

    @property
    def settle_in_shop_bet_tab(self):
        return self._find_element_by_selector(selector=self._settle_in_shop_bet_tab, context=self._we, timeout=10)

    @property
    def open_in_shop_bet_tab_active(self):
        return self._find_element_by_selector(selector=self._open_in_shop_bet_tab_active, context=self._we)

    @property
    def settle_in_shop_bet_tab_active(self):
        return self._find_element_by_selector(selector=self._settle_in_shop_bet_tab_active, context=self._we)


class ReceiptNumberInfo(ComponentBase):
    _bet_station_receipt = 'xpath=.//*[@class="betSlipTitle"][contains(text(),"Bet Station receipt")]'
    _over_the_counter_receipt = 'xpath=.//*[@class="betSlipTitle"][contains(text(),"Over-the-counter receipt")]'

    @property
    def bet_station_receipt(self):
        return self._find_element_by_selector(selector=self._bet_station_receipt, context=self._we)

    @property
    def over_the_counter_receipt(self):
        return self._find_element_by_selector(selector=self._over_the_counter_receipt, context=self._we)


class BetTracker(ComponentBase):
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _page_title = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _coupon_input = 'xpath=.//*[@name="coupon-input"]'
    _track_button = 'xpath=.//*[@class="rc-btn"]'
    _coupon_error_msg = 'xpath=.//*[contains(@class,"coupon-input--error")]'
    _cash_out_block = 'xpath=.//*[@class= "cash-out-block"]'
    _bet_tracker_info_icon = 'xpath=.//*[@class="info-icon"]'
    _receipt_number_info = 'xpath=.//*[@class ="modal-info"]'
    _no_event_text = 'xpath=.//*[contains(@class, "cash-out-block__tab") and not(@hidden)]//*[@id="no-event__text"]'

    @property
    def cash_out_block(self):
        return BetTabs(selector=self._cash_out_block)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def page_title(self):
        return TextBase(selector=self._page_title)

    @property
    def title_styles(self):
        return ComponentBase(selector=self._page_title, context=self._we)

    @property
    def coupon_input_styles(self):
        return ComponentBase(selector=self._coupon_input, context=self._we)

    @property
    def coupon_input(self):
        return self._find_element_by_selector(selector=self._coupon_input, context=self._we)

    @coupon_input.setter
    def coupon_input(self, value):
        we = self._find_element_by_selector(selector=self._coupon_input, context=self._we)
        if self.is_safari:
            safari_click(we)
        else:
            we.click()
        we.send_keys(value)

    @property
    def track_button(self):
        return ButtonBase(selector=self._track_button, context=self._we)

    @property
    def track_button_styles(self):
        return ComponentBase(selector=self._track_button, context=self._we)

    @property
    def coupon_error_msg(self):
        return self._find_element_by_selector(selector=self._coupon_error_msg, context=self._we, timeout=10)

    @property
    def bet_tracker_info_icon(self):
        return self._find_element_by_selector(self._bet_tracker_info_icon, context=self._we)

    @property
    def tracker_info_styles(self):
        return ComponentBase(selector=self._bet_tracker_info_icon, context=self._we)

    @property
    def receipt_number_info(self):
        return ReceiptNumberInfo(selector=self._receipt_number_info)

    @property
    def no_event_text(self):
        return self._find_element_by_selector(self._no_event_text, context=self._we)


class ShopLocator(ComponentBase):
    _page_title = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'

    @property
    def page_title(self):
        return TextBase(selector=self._page_title)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)
