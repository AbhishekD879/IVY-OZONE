from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.coral.components.byb_betslip import CoralBYBBetslip
from voltron.pages.coral.components.right_column_widgets.right_column import CoralRightColumn
from voltron.pages.coral.contents.coral_marketing_preferences import CoralMarketingPreferencesDesktop
from voltron.pages.coral.contents.edp.promotion_details import CoralPromotionDetails
from voltron.pages.coral.contents.my_bets.bet_history.bet_history import CoralBetHistory
from voltron.pages.coral.contents.my_bets.bet_history.bet_history import CoralBetHistoryDesktop
from voltron.pages.coral.dialogs.dialog_contents.my_inbox import CoralMyInbox
from voltron.pages.coral.menus.other_menus_desktop import CoralMenusDesktop
from voltron.pages.coral.menus.right_menu_desktop import CoralRightMenuDesktop
from voltron.pages.coral.mobile_site import MobileSite
from voltron.pages.shared import get_cms_config
from voltron.pages.shared.components.back_to_top_button import BackToTopButton
from voltron.pages.shared.components.header_desktop import DesktopHeader
from voltron.pages.shared.components.right_column_widgets.favourites_widget_section import FavoritesWidgetSection
from voltron.pages.shared.contents.base_contents.competitions_league_desktop_page import CompetitionLeagueDesktopPage
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceiptDesktop, LottoBetReceiptDesktop
from voltron.pages.shared.contents.betslip.betslip_desktop import BetSlipDesktop, LottoBetSlipDesktop
from voltron.pages.shared.contents.build_your_race_card import BuildYourRaceCard, BuildYourOwnRaceCard
from voltron.pages.shared.contents.coupons_page import CouponPageDesktop
from voltron.pages.shared.contents.edp.greyhound_event_details import GreyHoundEventDetails
from voltron.pages.shared.contents.edp.racing_event_details_desktop import RacingEventDetailsDesktop
from voltron.pages.shared.contents.edp.sport_event_details import DesktopEventDetails
from voltron.pages.shared.contents.football import FootballDesktop
from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.handball import HandballDesktop
from voltron.pages.shared.contents.homepage import HomePageDesktop
from voltron.pages.shared.contents.inplay_desktop import InPlayDesktop
from voltron.pages.shared.contents.live_stream import DesktopLiveStream
from voltron.pages.shared.contents.lotto_desktop import LottoDesktop
from voltron.pages.shared.contents.messages import MessagesDesktop
from voltron.pages.shared.contents.my_bets.cashout import CashoutDesktop, Cashout
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBetsDesktop, OpenBets
from voltron.pages.shared.contents.virtuals.virtual_sports_desktop import VirtualSportsDesktop
from voltron.pages.shared.menus.desktop_left_sport_menu import DesktopLeftSportMenu
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.waiters import wait_for_result, wait_for_haul


class DesktopSite(MobileSite):
    _header_desktop = 'xpath=.//*[@data-crlat="header"]'
    _header_type = DesktopHeader
    _cash_out = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.cashOut" or @data-crlat="slideContent.2"]]'
    _open_bets = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.openBets" or @data-crlat="slideContent.1"]]'
    _bet_history = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.betHistory" or @data-crlat="slideContent.3"]]'
    _bet_receipt = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="betslipReceipt"]]'
    _marketing_preferences = 'xpath=.//*[@class="portal-center-wrapper"]'

    _right_menu = 'xpath=.//vn-account-menu'
    _deposit_pop_up = 'xpath=.//lh-quick-deposit-responsive[*]'
    _my_inbox = 'xpath=.//lh-inbox'

    @property
    def right_column(self):
        return CoralRightColumn(selector=self._right_column, timeout=5)

    @property
    def sport_menu(self):
        return DesktopLeftSportMenu(selector=self._left_pane, timeout=10)

    @property
    def inplay(self):
        return InPlayDesktop(selector=self._page_content)

    @property
    def football(self):
        return FootballDesktop(selector=self._page_content)

    @property
    def handball(self):
        return HandballDesktop(selector=self._page_content)

    @property
    def virtual_sports(self):
        return VirtualSportsDesktop(selector=self._page_content)

    @property
    def right_menu(self):
        return CoralRightMenuDesktop(selector=self._right_menu, context=self._driver, timeout=3)

    @property
    def marketing_preferences(self):
        return CoralMarketingPreferencesDesktop(selector=self._marketing_preferences, context=self._driver, timeout=3)

    @property
    def betslip(self):
        return BetSlipDesktop(selector=self._betslip)

    @property
    def settled_bets(self):
        bet_history_shown_on_widget = find_element(selector=self._bet_history, timeout=5)
        if bet_history_shown_on_widget:
            return CoralBetHistoryDesktop(selector=self._bet_history, timeout=1)
        try:
            return CoralBetHistory(selector=self._page_content)
        except Exception as e:
            raise VoltronException(
                f'Bet History is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def lotto_betslip(self):
        return LottoBetSlipDesktop(selector=self._betslip)

    def has_betslip_opened(self, expected_result: bool = True, timeout: (int, float) = 1.5) -> bool:
        """
        Waits for betslip to be opened/closed. In case of Desktop - betslip is always visible, sp expected result=False is not expected
        :param expected_result: expected result can be only True for Desktop
        :param timeout: timeout
        :return: True or False
        """
        right_column = self.right_column
        return wait_for_result(lambda: 'BETSLIP' in right_column.items_as_ordered_dict,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'{self.__class__.__name__} Betslip opened state to be {expected_result}')

    @property
    def bet_receipt(self):
        return BetReceiptDesktop(selector=self._bet_receipt, timeout=10)

    @property
    def lotto_bet_receipt(self):
        return LottoBetReceiptDesktop(selector=self._bet_receipt, timeout=10)

    def is_bet_receipt_displayed(self, expected_result=True, timeout=5):
        """
        Verifies if bet receipt is shown or not.
        :param expected_result: Specifies the result the function waits for.
        :param timeout: Specifies waiting time.
        :return: True if bet receipt is displayed, False otherwise
        """
        bet_receipt_shown = wait_for_result(
            lambda: find_element(selector=self._bet_receipt, timeout=0) is not None,
            name='BetReceipt shown on Right Menu widget',
            expected_result=expected_result,
            timeout=timeout,
            bypass_exceptions=(VoltronException,
                               NoSuchElementException,
                               StaleElementReferenceException)
        )
        return bet_receipt_shown

    @property
    def racing_event_details(self):
        return RacingEventDetailsDesktop(selector=self._page_content)

    @property
    def greyhound_event_details(self):
        return GreyHoundEventDetails(selector=self._page_content)

    def open_my_bets_cashout(self):
        cms = get_cms_config()
        initial_data = cms.get_initial_data(device_type='desktop', cached=True)
        cashout_cms = initial_data.get('CashOut', {})
        if not cashout_cms:
            system_config = initial_data.get('systemConfiguration', {})
            cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = cms.get_system_configuration_item('CashOut')
        is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if is_cashout_tab_enabled:
            self.open_my_bets()
            self.betslip.tabs_menu.click_button('CASH OUT')
            if not find_element(selector=self._cash_out, timeout=10):
                raise VoltronException('"Cashout" is not shown on Right Menu widget')
        else:
            self.open_my_bets_open_bets()

    def open_my_bets_open_bets(self):
        self.open_my_bets()
        self.betslip.tabs_menu.click_button('OPEN')
        if not find_element(selector=self._open_bets, timeout=5):
            raise VoltronException('"Open Bets" is not shown on Right Menu widget')

    def open_my_bets_settled_bets(self):
        self.open_my_bets()
        self.betslip.tabs_menu.click_button('SETTLED')
        if not find_element(selector=self._bet_history, timeout=10):
            raise VoltronException('"Settled Bets" is not shown on Right Menu widget')

    def open_my_bets(self):
        self.betslip.betslip_tabs.items_as_ordered_dict.get('MY BETS').click()

    @property
    def cashout(self):
        cms = get_cms_config()
        initial_data = cms.get_initial_data(device_type='desktop', cached=True)
        cashout_cms = initial_data.get('CashOut', {})
        if not cashout_cms:
            system_config = initial_data.get('systemConfiguration', {})
            cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = cms.get_system_configuration_item('CashOut')
        is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if not is_cashout_tab_enabled:
            return OpenBetsDesktop(selector=self._open_bets, timeout=5)
        else:
            cashout_shown_on_widget = find_element(selector=self._cash_out, timeout=5)
            if cashout_shown_on_widget:
                return CashoutDesktop(selector=self._cash_out, timeout=1)
            try:
                return Cashout(selector=self._page_content)
            except Exception as e:
                raise VoltronException(f'Cashout is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def open_bets(self):
        open_bet_shown_on_widget = find_element(selector=self._open_bets, timeout=5)
        if open_bet_shown_on_widget:
            return OpenBetsDesktop(selector=self._open_bets, timeout=5)
        try:
            return OpenBets(selector=self._page_content)
        except Exception as e:
            raise VoltronException(f'Open bets is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def bet_history(self):
        bet_history_shown_on_widget = find_element(selector=self._bet_history, timeout=5)
        if bet_history_shown_on_widget:
            return CoralBetHistoryDesktop(selector=self._bet_history, timeout=1)
        try:
            return CoralBetHistory(selector=self._page_content)
        except Exception as e:
            raise VoltronException(f'Bet History is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def favourites(self):
        favourites = find_element(selector=self._favourites, timeout=10)
        if not favourites:
            raise VoltronException('"Favourites" is not shown on Right Menu widget')
        return FavoritesWidgetSection(selector=self._favourites, timeout=5)

    @property
    def sports_page(self):
        return SportPageDesktop(selector=self._page_content)

    @property
    def home(self):
        return HomePageDesktop(selector=self._contents)

    @property
    def sport_event_details(self):
        return DesktopEventDetails(selector=self._page_content)

    def navigate_to_right_menu_item(self, name, timeout=3):
        self.header.right_menu_button.click()
        self.right_menu.click_item(name)
        wait_for_result(lambda: self.right_menu.header.title == name,
                        name='Wait for header title to change',
                        timeout=timeout)

    def navigate_to_my_account(self):
        raise NotImplementedError('There is no "My Account" page on Coral')

    def navigate_to_my_account_page(self, name, timeout=3):
        self.navigate_to_right_menu_item(name='Settings')

    def wait_logged_in(self, login_criteria=None, timeout=5):
        return wait_for_result(lambda: self.header.has_right_menu() and self.header.right_menu_button.is_displayed(timeout=1),
                               timeout=timeout,
                               name='User to be logged in',
                               bypass_exceptions=VoltronException)

    def wait_for_deposit_pop_up_closed(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: find_element(selector=self._deposit_pop_up, timeout=0) is None,
                               expected_result=expected_result,
                               name='"Deposit" window to be closed',
                               timeout=timeout)

    def open_sport(self, name, timeout=5, **kwargs):
        sport_name = name.title()
        sports = self.sport_menu.items_as_ordered_dict
        if not sports:
            raise VoltronException('Cannot found Sports list')
        if sport_name not in sports:
            raise VoltronException(f'No "{sport_name}" found in sports list "{list(sports.keys())}"')
        sport = sports[sport_name]
        sport.scroll_to()
        sport.perform_click()
        content_state = kwargs.get('content_state', name)
        self.wait_content_state(content_state, timeout=timeout)
        self.close_qe_or_fanzone_popup(name=name, **kwargs)

    def enter_value_to_input_field(self, value, on_betslip=None):
        raise NotImplementedError('Cannot use UI keyboard for setting value. Modify test to use send_keys() instead')

    def toggle_quick_bet(self):
        self._logger.warning('Bypassing disabling quick bet because quick bet is not present on Desktop')

    def open_betslip(self):
        self._logger.warning('Bypassing opening betslip because betslip is always present as widget on Desktop')

    def close_betslip(self):
        self._logger.warning('Bypassing closing betslip because betslip is always present as widget on Desktop')

    def close_betreceipt(self):
        self._logger.warning('Bypassing closing bet receipt because betslip is always present as widget on Desktop')

    @property
    def tutorial_overlay(self):
        raise NotImplementedError('Tutorial overlay is not present on Desktop')

    def wait_for_tutorial_overlay(self, expected_result=True, timeout=5):
        raise NotImplementedError('Tutorial overlay is not present on Desktop')

    @property
    def connect_overlay(self):
        raise NotImplementedError('Connect overlay is not present on Desktop')

    def wait_for_connect_overlay(self, expected_result=True, timeout=5):
        raise NotImplementedError('Connect overlay is not present on Desktop')

    @property
    def build_your_card(self):
        return BuildYourRaceCard(selector=self._contents)

    @property
    def build_your_own_race_card(self):
        return BuildYourOwnRaceCard(selector=self._contents)

    @property
    def byb_betslip_panel(self):
        return CoralBYBBetslip(selector=self._quick_bet_panel, context=self._driver, timeout=2)

    @property
    def back_to_top_button(self):
        return BackToTopButton(selector=self._back_to_top_button, timeout=5)

    @property
    def competition_league(self):
        return CompetitionLeagueDesktopPage(selector=self._page_content)

    @property
    def coupon(self):
        return CouponPageDesktop(selector=self._page_content)

    @property
    def promotion_details(self):
        return CoralPromotionDetails(selector=self._page_content)

    @property
    def my_inbox(self):
        return CoralMyInbox(selector=self._my_inbox, timeout=3)

    @property
    def menus(self):
        return CoralMenusDesktop(selector=self._other_menus, context=self._driver, timeout=3)

    @property
    def live_stream(self):
        return DesktopLiveStream(selector=self._page_content)

    @property
    def lotto(self):
        return LottoDesktop(selector=self._page_content)

    @property
    def messages(self):
        return MessagesDesktop(selector=self._page_content)
