from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import SwitchersMenu
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem
from voltron.pages.shared.contents.edp.racing_edp_market_section import RacingMarketSection
from voltron.pages.shared.contents.edp.racing_event_details import RacingEDPTabContent
from voltron.pages.shared.contents.virtuals.base_tab_content import BaseVirtualsTabContent


class VirtualTabsMenuItem(TabsMenuItem):
    _fade_out_overlay = False


class VirtualTabsMenu(TabsMenu):
    _list_item_type = VirtualTabsMenuItem


class VirtualEventMarketsList(RacingMarketSection):
    _market_tabs_list = 'xpath=.//*[@data-crlat="switchers"]'
    _market_tabs_list_type = SwitchersMenu
    _add_to_betslip_button = 'xpath=.//*[@data-crlat="addToBetslipButton"]'

    @property
    def market_tabs_list(self):
        return self._market_tabs_list_type(selector=self._market_tabs_list, context=self._we)

    @property
    def add_to_betslip_button(self):
        return ButtonBase(selector=self._add_to_betslip_button, context=self._we)


class VirtualRacingTabContent(BaseVirtualsTabContent, RacingEDPTabContent):
    _tabs_menu_type = VirtualTabsMenu
    _event_markets_list = 'xpath=.//*[@data-crlat="accordionsList"]'
    _event_markets_list_type = VirtualEventMarketsList
