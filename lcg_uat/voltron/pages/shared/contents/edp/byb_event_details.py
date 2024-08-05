from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.byb_dashboard import BYBDashboardSection
from voltron.pages.shared.components.edp.sport_event_details import MarketsSectionsList
from voltron.pages.shared.components.markets.build_your_bet.byb_correct_score_market import BYBCorrectScoreMarket
from voltron.pages.shared.components.markets.build_your_bet.byb_default_market import BYBDefaultMarket
from voltron.pages.shared.components.markets.build_your_bet.byb_double_chance_market import BYBDoubleChanceMarket
from voltron.pages.shared.components.markets.build_your_bet.byb_match_result_market import BYBMatchResultMarket, BYBTotalGoalsMarket
from voltron.pages.shared.components.markets.build_your_bet.byb_match_result_market import BYBMatchResultMarketSwitcher
from voltron.pages.shared.components.markets.build_your_bet.byb_player_bets_market import BYBPlayerBetsMarket
from voltron.pages.shared.components.markets.build_your_bet.byb_player_market import BYBPlayerMarket
from voltron.pages.shared.components.your_call_static_block import YourCallStaticBlock
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class BYBMarketsSectionsList(MarketsSectionsList):
    _default_market_sections_list_type = BYBDefaultMarket
    _accordions_list_type = {
        'PLAYER BETS': BYBPlayerBetsMarket,
        'PLAYER TOTAL PASSES': BYBPlayerBetsMarket,
        'PLAYER TOTAL GOALS': BYBPlayerBetsMarket,
        'PLAYER TO BE CARDED': BYBMatchResultMarketSwitcher,
        'ANYTIME GOALSCORER': BYBMatchResultMarketSwitcher,
        'CORRECT SCORE': BYBCorrectScoreMarket,
        'MATCH BETTING': BYBMatchResultMarket,
        'DOUBLE CHANCE': BYBDoubleChanceMarket,
        'PLAYER TO SCORE 2+ GOALS': BYBPlayerMarket,
        'BOTH TEAMS TO SCORE': BYBMatchResultMarket,
        'TOTAL GOALS': BYBTotalGoalsMarket
    }


class TabMenu(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"tab")]'

    @property
    def name(self):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._item),
                                 name="Tab to have visible name",
                                 timeout=5)
        return result if result else ''


class BYBEventDetailsTabMenu(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"tab-wrapper")]'
    _list_item_type = TabMenu
    _selected_item = 'xpath=.//*[contains(@class, "active")]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._item, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,), timeout=3)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')

    @property
    def menu_item_names(self):
        return list(self.items_as_ordered_dict.keys())

    @property
    def current(self):
        try:
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name
        except (StaleElementReferenceException, VoltronException):
            self._logger.debug(f'*** Overriding Exception in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=2)
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name

    def click(self):
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def open_tab(self, tab_name, timeout=5):
        scroll_to_center_of_element(self._we)
        result = wait_for_result(lambda: tab_name in self.items_as_ordered_dict,
                                 name=f'Tab "{tab_name}" to appear in {self.__class__.__name__} - {self._list_item_type.__name__}',
                                 timeout=timeout)
        if not result:
            raise VoltronException('Tab name "%s" is not found in list of tabs ["%s"]'
                                   % (tab_name, '", "'.join(filter(None, self.items_as_ordered_dict.keys()))))
        if tab_name == self.current:
            self._logger.warning(f'*** Bypassing click on tab "{tab_name}" as it is already active')
            return True
        opened_tab = self.items_as_ordered_dict[tab_name]
        scroll_to_center_of_element(opened_tab._we)
        opened_tab.click()
        return wait_for_result(lambda: self.current == tab_name,
                               name=f'"{tab_name}" to be active',
                               bypass_exceptions=(NoSuchElementException,
                                                  StaleElementReferenceException,
                                                  VoltronException),
                               timeout=timeout)


class BYBEventDetailsTabContent(TabContent):
    _accordions_list = 'xpath=.//yourcall-tab-content//*[@class="parent"]'
    _accordions_list_type = BYBMarketsSectionsList

    _static_block = 'xpath=.//*[@data-crlat="yourcallStaticBlock"]'
    _static_block_type = YourCallStaticBlock

    _yourcall_dashboard_panel = 'xpath=.//*[@data-crlat="yourcall.dashboardSection"]'

    _verify_spinner = True
    _fade_out_overlay = True

    @property
    def static_block(self):
        return YourCallStaticBlock(selector=self._static_block, context=self._we)

    @property
    def dashboard_panel(self):
        return BYBDashboardSection(selector=self._yourcall_dashboard_panel, context=self._we, timeout=1)

    def wait_for_dashboard_panel(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._yourcall_dashboard_panel,
                                                                      context=self._we, timeout=0) is not None,
                               name=f'Build Your Bet Dashboard display status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_dashboard_panel(self, expected_result=True, timeout=1):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._yourcall_dashboard_panel, context=self._we, timeout=0),
            name=f'change match section to be expected "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result
