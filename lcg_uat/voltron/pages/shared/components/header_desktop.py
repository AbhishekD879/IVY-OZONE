from voltron.pages.coral.components.header import CoralMobileHeader
from voltron.pages.coral.components.header import CoralUserPanelContent
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.header import BetSlipCounter
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.waiters import wait_for_result


class BetSlipCounterDesktop(BetSlipCounter):
    _betslip_widget = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"]'
    _your_selection_subheader = 'xpath=.//*[@data-crlat="bsHead"]'

    @property
    def counter_value(self):
        from voltron.pages.shared.contents.betslip.betslip_desktop import BetSlipDesktop
        betslip = BetSlipDesktop(selector=self._betslip_widget)
        has_header = self._find_element_by_selector(selector=self._your_selection_subheader, context=betslip._we, timeout=0.8) is not None
        return betslip.your_selection_header.count if has_header else '0'

    def click(self):
        self._logger.debug(f'Bypassing {__name__} for {self.__class__.__name__}')


class DesktopHeaderTopMenu(ComponentBase):
    _item = 'xpath=.//a[contains(@class, "tab-nav-link")]'
    _list_item_type = LinkBase


class SportMenuItem(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class SportsMenu(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="subNavigationTab"]'
    _list_item_type = SportMenuItem


class DesktopUserPanel(CoralUserPanelContent):
    _deposit_button = 'xpath=.//vn-h-deposit-button'
    _my_inbox_button = 'xpath=.//lh-inbox-icon'

    @property
    def deposit_button(self):
        return ButtonBase(selector=self._deposit_button, context=self._we, timeout=2)

    @property
    def my_inbox_button(self):
        return ButtonBase(selector=self._my_inbox_button, context=self._we, timeout=2)


class DesktopHeader(CoralMobileHeader):
    _header_top_menu = 'xpath=.//vn-h-product-navigation'
    _header_top_menu_type = DesktopHeaderTopMenu
    _sport_menu = 'xpath=.//*[@data-crlat="header.bottomMenu"]'
    _user_panel_type = DesktopUserPanel

    @property
    def bet_slip_counter(self):
        return BetSlipCounterDesktop(selector='xpath=//body', context=get_driver())

    @property
    def top_menu(self):
        return self._header_top_menu_type(selector=self._header_top_menu, context=self._we)

    @property
    def sport_menu(self):
        return SportsMenu(selector=self._sport_menu)

    @staticmethod
    def wait_for_tab_color_change(tab, initial_color):
        return wait_for_result(
            lambda: tab.text_color_value == initial_color,
            name='Tab color to change',
            expected_result=False)
