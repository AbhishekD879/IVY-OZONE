import json
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.common.exceptions import WebDriverException

import tests
import voltron.environments.constants as vec
from voltron.pages.ladbrokes.components.five_a_side_leaderborad import FiveASideLeaderboard, FiveASideRulesButtonInfo, \
    FiveASideLobbyOverlay, FiveASideRulesEntryInformation
from voltron.pages.ladbrokes.components.fanzone_coming_back import FanzoneComingBack
from voltron.pages.shared import actions
from voltron.pages.shared import get_device_properties
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.byb_betslip import BYBBetReceipt
from voltron.pages.shared.components.byb_betslip import BYBBetslip
from voltron.pages.shared.components.cookie_banner import CookieBanner
from voltron.pages.shared.components.football_overlay import FootballOverlay
from voltron.pages.shared.components.footer import Footer, FooterHelp
from voltron.pages.shared.components.markets.build_your_bet.byb_player_bets_market import PlayerStatsDialog
from voltron.pages.shared.components.policy_banner import PolicyBanner
from voltron.pages.shared.components.portal.manage_my_cards import ManageMyCards
from voltron.pages.shared.components.portal.payment_history import PaymentHistory
from voltron.pages.shared.components.portal.withdraw_page import CashierWithdraw
from voltron.pages.shared.components.preferences_overlay import PreferencesOverlay
from voltron.pages.shared.components.promotion_overlay import PromotionOverlay
from voltron.pages.shared.components.question_engine import QuestionEngine, QuizHomePage, QuizResultsPage, QuizPagePopup
from voltron.pages.shared.components.quick_deposit_button import QuickDepositDesktop
from voltron.pages.shared.components.root_app import RootApp
from voltron.pages.shared.components.timeline import Timeline
from voltron.pages.shared.contents.account_closure import AccountClosure, AccountClosureOverlay
from voltron.pages.shared.contents.account_history.account_history import AccountHistory
from voltron.pages.shared.contents.account_history.gaming_history import GamingHistory
from voltron.pages.shared.contents.account_history.transaction_history import TransactionHistory
from voltron.pages.shared.contents.all_sports import AllSports
from voltron.pages.shared.contents.base_contents.big_competition import BigCompetitionPageBase
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_results import \
    HorseRacingResultedEventsPage, HorseRacingTriForecast, RacingHeaders
from voltron.pages.shared.contents.bet_filter.football_bet_filter import FootballBetFilterPage
from voltron.pages.shared.contents.bet_filter.football_bet_filter import FootballBetFilterResultsPage
from voltron.pages.shared.contents.bet_filter.horseracing_bet_filter import HorseRacingBetFilterPage
from voltron.pages.shared.contents.bet_filter.horseracing_bet_filter import HorseRacingBetFilterResultsPage
from voltron.pages.shared.contents.bet_receipt.football_jackpot_receipt import FootballJackpotReceipt
# from voltron.pages.shared.contents.bet_receipt.lotto_bet_receipt import LottoBetReceipt
from voltron.pages.shared.contents.betslip.betslip_unavailable import BetSlipUnavailable
from voltron.pages.shared.contents.build_info_json_page import BuildInfoJSONPage
from voltron.pages.shared.components.tutorial_overlay import TutorialOverlay
from voltron.pages.shared.components.loss_limit_dialog import LossLimitDialog
from voltron.pages.shared.contents.change_password import ChangePassword
from voltron.pages.shared.contents.competitions_league_page import CompetitionLeaguePage
from voltron.pages.shared.contents.connect import Connect, BetTracker, ShopLocator
from voltron.pages.shared.contents.contact_us_outer_page import ContactUsOuterPage
from voltron.pages.shared.contents.edp.freebet_details import FreeBetDetails
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetails
from voltron.pages.shared.contents.edp.sport_event_details import EventDetails
from voltron.pages.shared.contents.edp.tote_event_details import ToteEventDetails
from voltron.pages.shared.contents.favourite_matches import Favourites
from voltron.pages.shared.contents.football import Football
from voltron.pages.shared.contents.football import SportPage
from voltron.pages.shared.contents.freebets import Freebets
from voltron.pages.shared.contents.gambling_controls import GamblingControls, Immediate24HoursBreak
from voltron.pages.shared.contents.gaming import Gaming
from voltron.pages.shared.contents.handball import Handball
from voltron.pages.shared.contents.hockey import Hockey
from voltron.pages.shared.contents.league_page import LeaguePage
from voltron.pages.shared.contents.leagues_search import LeagueSearch
from voltron.pages.shared.contents.limits import Limits
from voltron.pages.shared.contents.live_stream import LiveStream
from voltron.pages.shared.contents.lotto import Lotto
from voltron.pages.shared.contents.marketing_preferences import MarketingPreferences
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistory
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBets, OpenBet
from voltron.pages.shared.contents.my_stable.my_stable_page import MyStable
from voltron.pages.shared.contents.odds_boost import OddsBoost
from voltron.pages.shared.contents.other_sports import Badminton, IceHockey
from voltron.pages.shared.contents.other_sports import Cricket
from voltron.pages.shared.contents.other_sports import Cycling
from voltron.pages.shared.contents.other_sports import Darts
from voltron.pages.shared.contents.other_sports import Formula1
from voltron.pages.shared.contents.other_sports import MotorBikes
from voltron.pages.shared.contents.other_sports import Snooker
from voltron.pages.shared.contents.other_sports import Golf
from voltron.pages.shared.contents.private_markets import PrivateMarketsTermsAndConditionsPage
from voltron.pages.shared.contents.promotions import Promotions
from voltron.pages.shared.contents.racing import GreyhoundRacing
from voltron.pages.shared.contents.racing import Horseracing
from voltron.pages.shared.contents.responsible_gambling import ResponsibleGambling
from voltron.pages.shared.contents.responsible_gaming import ResponsibleGaming
from voltron.pages.shared.contents.self_exclusion import SelfExclusion, SelfExclusionSelection, SelfExclusionDialog, \
    SelfExclusionOptions
from voltron.pages.shared.contents.service_closure import ServiceClosure
from voltron.pages.shared.contents.settings import Settings
from voltron.pages.shared.contents.spending_controls import SpendingControlsPage, SpendingControlsOverlay
from voltron.pages.shared.contents.tennis import Tennis
from voltron.pages.shared.contents.time_out import TimeOut
from voltron.pages.shared.contents.time_out_confirm import TimeOutPasswordConfirm
from voltron.pages.shared.contents.tote import Tote
from voltron.pages.shared.contents.us_sports import AmericanFootball
from voltron.pages.shared.contents.us_sports import Baseball
from voltron.pages.shared.contents.us_sports import Basketball
from voltron.pages.shared.contents.other_sports import Boxing
from voltron.pages.shared.components.direct_chat import HelpContactUs
from voltron.pages.shared.contents.virtuals.virtual_hub_page import VirtualSectionWrapper
from voltron.pages.shared.contents.virtuals.virtual_sports import VirtualSports
from voltron.pages.shared.contents.voucher_code import VoucherCode
from voltron.pages.shared.contents.withdraw import Withdraw
from voltron.pages.shared.contents.your_call import YourCall
from voltron.pages.shared.contents.forgot_username_password import ForgotPassword
from voltron.pages.shared.dialogs.dialog_manager import DialogManager
from voltron.utils import mixins
from voltron.pages.shared.contents.my_balance import MyBalance
from voltron.utils.content_manager import ContentManager
from voltron.utils.dialog_action import ActionItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.js_functions import get_data_layer
from voltron.utils.waiters import wait_for_result


class BMABaseSite(mixins.LoggingMixin, metaclass=ABCMeta):
    _app_ready = 'xpath=.//*[contains(@class, "bma-ready")]'
    _root_app = 'tag=root-app'
    _cookie_banner = 'xpath=.//*[@data-crlat="cookieBanner"] | .//*[@id="onetrust-banner-sdk"]'
    _contents = 'xpath=.//*[@data-crlat="pageContent"]'
    _preferences_overlay = 'xpath=.//contact-prefer-screen'
    _header = 'xpath=.//*[@data-uat="header"]'
    _header_type = None
    _page_content = 'xpath=.//*[@data-uat="pageContent"]'
    _footer = 'xpath=.//vn-responsive-footer/footer | .//vn-footer'
    _footer_type = Footer
    _footer_element_help = FooterHelp
    _footer_help = 'xpath=.//body[@class="cf is-popup"]'
    _greyhound_type = GreyhoundRacing

    _policy_banner = 'xpath=.//*[@data-crlat="policiesBanner"]'
    _change_password = 'xpath=.//pt-change-password'

    _promotion_overlay = 'xpath=.//*[@data-crlat="d.promoOver"]'
    _arrow_panel = 'xpath=.//*[@class="arr-panel"]'
    _tutorial_overlay = 'xpath=.//*[@data-crlat="tutorialOverlay"]'
    _timeline = 'xpath=//timeline'
    _question_engine = 'xpath=.//*[@class="question-engine"]'
    _quiz_page = 'xpath=.//*[@class="qe-container"] | .//*[@id="content"]/question-engine-main'
    _quiz_page_popup = 'xpath=.//div[@class="modal-dialog"]'
    _connect_overlay = 'xpath=.//*[@data-crlat="retailOverlay"]'
    _football_overlay = 'xpath=.//*[@class="arr-panel"]'

    # Player Bets Stats Popup
    _player_bets_stats_popup = 'xpath=.//div[@class="modal-dialog"]'

    # Gaming page
    _gaming_page = 'xpath=.//vn-app[@class="app-root"]'

    # Quick Bet panel
    _quick_bet_panel = 'xpath=.//*[@data-crlat="quickbetPanel" and contains(@class, "slide-up")]'
    _quick_bet_panel_inner = 'xpath=.//*[@data-crlat="quickbetPanel" and contains(@class, "slide-up")][./div[not(contains(@class,"hidden"))]] | //*[@id="quickbet-updated-panel"] | //*[@data-crlat="quickbetPanel"]'
    _quick_bet_receipt = 'xpath=.//*[@data-crlat="quickbetReceipt"]'

    # Five-a-side lobby and leaderboard pages
    _five_A_side_leaderboard = 'xpath=.//fiveaside-leader-board'
    _five_a_side_lobby = 'xpath=.//fiveaside-show-down-lobby'

    # Contact Us page
    _contact_us_page = 'xpath=.//div[.//*[@id="header"]]'

    # wait for login dialog closed timeout
    _wait_login_dialog_closed = 30

    _left_pane = 'xpath=.//*[@data-crlat="leftColumn"]'  # Sport menu on desktop
    _right_column = 'xpath=.//*[@data-crlat="rightColumn"]'
    _right_menu = 'xpath=.//vn-account-menu-view'
    _back_to_top_button = 'xpath=.//*[@data-crlat="backToTop"]'
    _betslip = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"]/*[@data-crlat="accordion"]'
    _bet_receipt = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"]/*[@data-crlat="accordion"][.//*[@data-crlat="betslipReceipt"]]'
    _favourites = 'xpath=.//*[@data-crlat="widgetAccordion.favourites"]/*[@data-crlat="accordion"]'
    _withdrawal = 'xpath=.//div[contains(@class,"channel")]'
    _responsible_gambling = 'xpath=.//*[@class="casino-body"] | .//*[@id="main-content"]'
    _gambling_control = 'xpath=.//*[@id="ptgamblingcontrols"]'
    _immediate_break_page_layout = "xpath=.//*[@id='navigation-layout-page']"

    safari_browser = 'safari'

    # self exclusion dialog
    _dialog = 'xpath=.//pt-self-exclusion-confirm-dialog'

    # timeline overlay tutorial
    _timeline_overlay_tutorial = 'xpath=.//*[@id="timeline-tutorial-overlay"]'

    # fanzone coming back overlay
    _fanzone_cb_overlay = 'xpath=.//fanzone-cb-overlay//div[@class="FCB-Popup"]'

    # loss limit dialog
    _loss_limit_dialog = 'xpath=.//*[@class="dlg-responsive-content"]'

    # quick_deposit_desktop
    _quick_deposit_desktop = 'xpath=.//vn-cashier-iframe'

    # portal selector
    _cashier_withdraw = 'xpath=.//*[@id="mainCashierWrapper"]'
    _cashier_payment_history = 'xpath=.//*[@id="mainCashierWrapper"]'
    _cashier_manage_my_card = 'xpath=.//*[@id="mainCashierWrapper"]'
    _transaction_history = 'xpath=.//*[@id="main-content"]'
    _account_closure = 'xpath=//*[@id="main-content"]'
    _account_closure_overlay = 'xpath=//*[@class="cdk-overlay-container"]'

    # spending controls
    _spending_controls_page = 'xpath=.//pt-spending-controls'
    _spending_controls_overlay_page = 'xpath=.//*[@class="cdk-overlay-container"]'

    # biwin hint
    _bwin_hint = 'xpath=.//vn-hint//span[@class]'

    def __init__(self, *args, **kwargs):
        super(BMABaseSite, self).__init__()
        self.brand = kwargs.get('brand', 'bma')
        self._content_manager = ContentManager()
        self._logger.debug(f'*** Recognized "{self._content_manager.__class__.__name__}" content manager')
        self._content_state_name = ''
        self._driver = get_driver()

    @property
    def dialog_manager(self):
        """Property that returns dialog manager object"""
        return DialogManager()

    @property
    def root_app(self):
        # TODO timeout w/a because slow page refresh/navigation
        return RootApp(selector=self._root_app, timeout=25)

    def launch_application(self):
        self.wait_content_state('Home')

    def wait_for_app_to_be_ready(self, timeout=10):
        result = wait_for_result(lambda: find_element(selector=self._app_ready, timeout=0) is not None,
                                 name='Application to be ready',
                                 timeout=timeout)
        if not result:
            raise VoltronException(f'Timeout waiting for application to load')
        return result

    def wait_splash_to_hide(self, timeout=None):
        timeout = timeout if timeout is not None else tests.settings.page_load_timeout
        self.wait_for_app_to_be_ready(timeout=timeout)
        self.root_app.wait_to_show(timeout=timeout)
        self.close_all_banners(async_close=False)

    @property
    def header(self):
        """Property that should return header object"""
        return self._header_type(selector=self._header, context=self._driver)

    @property
    def back_button(self):
        return self.contents.header_line.back_button

    @property
    def has_back_button(self):
        return self.contents.header_line.has_back_button

    @abstractproperty
    def right_menu(self):
        """Property that should return right menu object"""

    @property
    def direct_chat(self):
        return HelpContactUs(selector=self._page_content, timeout=3)

    @property
    def my_balance(self):
        return MyBalance(selector=self._right_menu, context=self._driver, timeout=3)

    @property
    def contents(self):
        content_state = self._content_manager.get_content_state()
        self._content_state_name = content_state.__name__
        self._logger.debug('*** Content state is "%s"' % self._content_state_name)
        return content_state(selector=self._contents, context=self._driver)

    def wait_content_state_changed(self, timeout=10):
        wait_for_result(
            lambda: self._content_state_name != self._content_manager.get_content_state().__name__,
            name='Content state changed',
            timeout=timeout
        )

    def wait_for_byb_betslip_panel(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: find_element(selector=self._quick_bet_panel, timeout=0) is not None,
                               expected_result=expected_result,
                               name='Build Your Bet Betslip panel to be displayed',
                               timeout=timeout)

    def wait_for_byb_bet_receipt_panel(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: find_element(
                selector=self._quick_bet_panel,
                timeout=0) is not None and self.byb_bet_receipt_panel.header.title == vec.betslip.BET_RECEIPT,
            expected_result=expected_result,
            name='Build Your Bet BetReceipt panel to be displayed: %s' % expected_result,
            timeout=timeout)

    def wait_for_5_a_side_bet_receipt_panel(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: find_element(
                selector=self._quick_bet_panel,
                timeout=0) is not None and self.byb_bet_receipt_panel.header.title == vec.yourcall.FIVE_A_SIDE_BETRECEIPT_TITLE,
            expected_result=expected_result,
            name='Build Your Bet BetReceipt panel to be displayed: %s' % expected_result,
            timeout=timeout)

    def wait_content_state(self, state_name, raise_exceptions=True, timeout=15):
        """
        Verifies page by url
        :param raise_exceptions: throw exception when timeout reached
        :type raise_exceptionss:
        """
        states_dict = {
            'Greyhounds': 'GREYHOUNDRACING',
            'GREYHOUNDS': 'GREYHOUNDRACING',
            'ALL SPORTS': 'ALLSPORTS',
            'All Sports': 'ALLSPORTS',
            'AZ Sports': 'ALLSPORTS',
            'Home': 'HOMEPAGE',
            'INTERNATIONAL TOTE': 'TOTE',
            'GAMING': 'HomePage',
            'Gaming': 'HomePage',
            'Football': 'FOOTBALL',
            'OPENBETS': 'open-bets',
            'ADD NEW PAYMENT TYPE': 'Deposit',
            'MARKETING PREFERENCES': 'BaseContent',
            'MARKET PREFERENCES': 'BaseContent',
            'FREEBET INFORMATION': 'Freebets',
            'VIRTUAL': 'VirtualSports',
            'Personal Details': 'ChangePasswordAddress',
            'HORSES': 'Horseracing',
            'Horses': 'Horseracing',
            'EVENTDETAILS': 'EventDetails',
            'RACINGEVENTDETAILS': 'RacingEventDetails',
            '1-2-free': 'ONETWOFREEWELCOMESCREEN',
            'avtar-menu' : "BaseContent"
        }
        expected_state_name = states_dict.get(state_name, state_name.upper().replace(' ', '').replace('-', ''))
        result = wait_for_result(
            lambda: self._content_manager.get_content_state().__name__.upper() == expected_state_name.upper(),
            name=f'Content state changed to "{state_name}"',
            timeout=timeout
        )
        if raise_exceptions and not result:
            raise VoltronException(f'Timeout waiting for page: "{expected_state_name}"')
        return result

    @property
    def build_info_json_page(self):
        return BuildInfoJSONPage(selector='xpath=.//pre')

    @property
    def content_state(self):
        return self._content_manager.get_content_state().__name__.upper()

    @property
    def tutorial_arrow_panel(self):
        return TutorialOverlay(selector=self._tutorial_overlay, timeout=5)

    @property
    def timeline_tutorial_overlay(self):
        return TutorialOverlay(selector=self._timeline_overlay_tutorial, timeout=5)

    @property
    def fanzone_cb_overlay(self):
        return FanzoneComingBack(selector=self._fanzone_cb_overlay)

    @property
    def loss_limit_dialog(self):
        return LossLimitDialog(selector=self._loss_limit_dialog)

    @property
    def biwin_hint(self):
        return ComponentBase(selector=self._bwin_hint)

    @property
    def football_overlay_panel(self):
        return TutorialOverlay(selector=self._arrow_panel, timeout=5)

    @property
    def footer(self):
        return self._footer_type(selector=self._footer, context=self._driver)

    @abstractproperty
    def betslip(self):
        """Property that should return Betslip object"""

    @abstractmethod
    def open_my_bets_cashout(self):
        """Method that should open My bets/Cashout Page/Widget"""

    @abstractmethod
    def open_my_bets_open_bets(self):
        """Method that should open My bets/Open Bets Page/Widget"""

    @abstractproperty
    def cashout(self):
        """Property that should return Cashout object"""

    @abstractmethod
    def has_betslip_opened(self, expected_result=True, timeout=5):
        """Property that should return True or False depending on betslip closed (visible) or not"""

    @abstractproperty
    def bet_receipt(self):
        """Property that should return betreceipt object"""

    def is_bet_receipt_displayed(self, expected_result=True, timeout=5):
        """
        Verifies if bet receipt is shown or not.
        :param expected_result: Specifies the result the function waits for.
        :return: True if bet receipt is displayed, False otherwise
        """

    @property
    def cookie_banner(self):
        cookie_banner = find_element(selector=self._cookie_banner, timeout=1)
        return CookieBanner(web_element=cookie_banner) if cookie_banner else None

    @property
    def get_data_layer(self):
        return json.loads(get_data_layer())

    @property
    def get_gcdata(self):
        return self._driver.execute_script("return gcData;")

    @property
    def get_iapiconf(self):
        return self._driver.execute_script("return iapiConf;")

    @property
    def get_window_client_config(self):
        return self._driver.execute_script('return window.clientConfig')

    @property
    def initialize_new_relic(self):
        return self._driver.execute_script('return newRelicEvents={};')

    @property
    def get_new_relic(self):
        try:
            return self._driver.execute_script("return newRelicEvents;")
        except WebDriverException as e:
            self._logger.warning(e)
            return None

    @property
    def get_performance_entries(self):
        return json.loads(self._driver.execute_script("return JSON.stringify(performance.getEntries());"))

    @property
    def cashier_withdraw(self):
        return CashierWithdraw(selector=self._cashier_withdraw, timeout=10)

    @property
    def cashier_payment_history(self):
        return PaymentHistory(selector=self._cashier_payment_history, timeout=2)

    @property
    def cashier_manage_my_card(self):
        return ManageMyCards(selector=self._cashier_manage_my_card, timeout=2)

    def wait_for_dialog(self, dialog_name: str, verify_name: bool = True, timeout: (int, float) = 10):
        """
        Method used for checking dialog presence on UI
        :param dialog_name: actual dialog name as on UI
        :param verify_name: parameter for comparing expected dialog title with actual
        :param timeout: timeout for waiting
        :return: dialog object in case of success, None if required dialog is not found
        """
        return self.dialog_manager.wait_for_dialog(dialog_name=dialog_name, verify_name=verify_name, timeout=timeout)

    @abstractmethod
    def wait_logged_in(self, login_criteria=None, timeout=5):
        """Method that should implement check if user is logged in"""

    @abstractmethod
    def navigate_to_my_account(self):
        """Method that should implement navigation to My Account menu"""

    @abstractmethod
    def change_odds_format(self, odds_format):
        """
        Method that should change odds format
        :param odds_format: 'DECIMAL' or 'FRACTIONAL'
        :return: True if format is changed to expected
        """

    @abstractmethod
    def navigate_to_my_account_page(self, name, timeout=3):
        """Method that should implement navigation to My Account menu item page"""

    def wait_logged_out(self, timeout=10):
        return wait_for_result(lambda: self.header.has_log_in_button(timeout=0),
                               name='Login Button should be visible',
                               expected_result=True,
                               timeout=timeout,
                               bypass_exceptions=(StaleElementReferenceException, VoltronException))

    @property
    def preferences_overlay(self):
        timeout = 7 if tests.settings.backend_env == 'prod' else 2.5
        preferences_overlay = find_element(selector=self._preferences_overlay, timeout=timeout)
        return PreferencesOverlay(web_element=preferences_overlay) if preferences_overlay else None

    def close_preferences_overlay(self, timeout=10):
        def _inner():
            overlay = self.preferences_overlay
            if overlay:
                overlay.click_save_preferences_button()
                return overlay.wait_for_element_disappear()

        wait_for_result(
            lambda: find_element(selector=self._preferences_overlay, timeout=0.5) is not None,
            timeout=timeout,
            name=f'Preferences Overlay to be displayed'
        )
        try:
            _inner()
        except StaleElementReferenceException:
            _inner()

    def close_all_dialogs(self, async_close=True, timeout=6, ignored_dialogs=()):
        ignored_dialogs = ignored_dialogs if ignored_dialogs else (vec.dialogs.DIALOG_MANAGER_YOU_ARE_LOGGED_OUT,)
        close_dialogs = ActionItem(
            name='Close all dialogs',
            action_func=lambda: self.dialog_manager.perform_dialog_default_action(ignored_dialogs=ignored_dialogs),
            expected_result=True,
            timeout=timeout
        )
        if async_close:
            actions.push(close_dialogs)
        else:
            wait_for_result(
                close_dialogs.action,
                name=close_dialogs.name,
                timeout=timeout
            )

    def close_all_banners(self, async_close: bool = True, timeout: float = 5):
        close_policy_banner = ActionItem(
            name='Close policy banner',
            action_func=lambda: self.close_policy_banner(),
            expected_result=True,
            timeout=timeout
        )
        close_cookie_banner = ActionItem(
            name='Close cookie banner',
            action_func=lambda: self.close_cookie_banner(),
            expected_result=True,
            timeout=timeout
        )
        if async_close:
            actions.push(close_policy_banner)
            actions.push(close_cookie_banner)
        else:
            wait_for_result(lambda: self.close_policy_banner(),
                            name='Policy banner to close',
                            expected_result=False,
                            timeout=timeout)
            wait_for_result(lambda: self.close_cookie_banner(),
                            name='Cookie banner to close',
                            expected_result=False,
                            timeout=timeout)

    def login(
            self,
            username=None,
            password=None,
            remember_me=False,
            login_criteria=None,
            async_close_dialogs=True,
            async_close_banners=False,
            close_all_banners=True,
            timeout=30,
            timeout_close_dialogs=10,
            timeout_wait_for_dialog=0,
            **kwargs
    ):
        if not self.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=timeout_wait_for_dialog):
            self.header.sign_in.click()
        dialog = self.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        if dialog is None:
            raise VoltronException(f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not present on page')
        username = username if username else tests.settings.betplacement_user
        password = password if password else tests.settings.default_password
        self._logger.info(f'*** Trying to login with user {username}')
        dialog.username = username
        dialog.password = password
        if remember_me:
            dialog.remember_me.click()
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=self._wait_login_dialog_closed)
        if not dialog_closed:
            raise VoltronException('User is not logged in as Login Dialog was not closed')
        im_happy_with_limit = kwargs.get("im_happy_with_limit", False)
        if self.root_app.has_biwin_hint(timeout=0.5, expected_result=True):
            self.biwin_hint.click()
        if self.root_app.has_loss_limit_dialog(timeout=0.5, expected_result=True) and not im_happy_with_limit:
            self.loss_limit_dialog.im_happy_with_limit.click()
        if self.root_app.has_fanzone_cb_overlay(timeout=0.5, expected_result=True):
            self.fanzone_cb_overlay.close_button_click()
        if self.root_app.has_biwin_hint(timeout=0.5, expected_result=True):
            self.biwin_hint.click()
        if close_all_banners:
            self.close_all_banners(async_close=async_close_banners)
        ignored_dialogs_to_close = kwargs.pop('ignored_dialogs',
                                              (vec.dialogs.DIALOG_MANAGER_LOG_IN,
                                               vec.dialogs.DIALOG_MANAGER_YOU_ARE_LOGGED_OUT))
        self.close_all_dialogs(async_close=async_close_dialogs, timeout=timeout_close_dialogs,
                               ignored_dialogs=ignored_dialogs_to_close)
        logged_in = self.wait_logged_in(login_criteria=login_criteria, timeout=timeout)
        if not logged_in:
            raise VoltronException(f'User "{username}" is not logged in after "{timeout}" seconds')
        timeline = kwargs.get("timeline", False)
        if self.root_app.has_timeline_overlay_tutorial(timeout=1, expected_result=True) and not timeline:
            self.timeline_tutorial_overlay.close_icon.click()
        if kwargs.get('close_free_bets_notification', True) and self.contents.has_free_bets_notification(timeout=0.5,
                                                                                                         expected_result=True):
            self.contents.free_bets_notification.close_button.click()

    def grid_connect_login(
            self,
            card_number=None,
            card_pin=None,
            remember_me=False,
            timeout_wait_for_dialog=5,
    ):
        if not self.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=timeout_wait_for_dialog):
            self.header.sign_in.click()
        dialog = self.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        if dialog is None:
            raise VoltronException(f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not present on page')
        dialog.connect_card_toggle.click()
        card_number = card_number if card_number else tests.settings.in_shop_user_card_number
        card_pin = card_pin if card_pin else tests.settings.in_shop_pin
        self._logger.info(f'*** Trying to login with user {card_number}')
        dialog.connect_card_number = card_number
        dialog.connect_card_pin = card_pin
        if remember_me:
            dialog.remember_me.click()
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed(timeout=self._wait_login_dialog_closed)
        if not dialog_closed:
            raise VoltronException('User is not logged in as Login Dialog was not closed')

    @abstractmethod
    def logout(self, timeout=10):
        """Method that should implement logout"""

    @property
    def policy_banner(self):
        policy_banner = find_element(selector=self._policy_banner, timeout=1)
        return PolicyBanner(web_element=policy_banner) if policy_banner else None

    def close_policy_banner(self):
        banner = self.policy_banner
        if banner:
            banner.close_icon.click()
            banner.wait_for_element_disappear()

    def close_cookie_banner(self):
        banner = self.cookie_banner
        if banner and banner.is_displayed():
            banner.ok_button.click()
            return banner.wait_for_element_disappear()

    @abstractproperty
    def tutorial_overlay(self):
        """Property that should return Tutorial Overlay object"""

    @abstractmethod
    def wait_for_tutorial_overlay(self, expected_result=True, timeout=5):
        """Method that should implement check if Tutorial Overlay is shown"""

    @abstractmethod
    def wait_for_connect_overlay(self, expected_result=True, timeout=5):
        """Method that should implement check if Connect Overlay is shown"""

    @property
    def change_password(self):
        return ChangePassword(selector=self._change_password, context=self._driver, timeout=10)

    @abstractmethod
    def register_new_user(self,
                          social_title,
                          first_name,
                          last_name,
                          birth_date,
                          country,
                          post_code,
                          address_one,
                          city,
                          mobile,
                          email,
                          username,
                          password,
                          currency,
                          daily_deposit_limit,
                          weekly_deposit_limit,
                          monthly_deposit_limit,
                          terms_and_conditions,
                          leave_limits_dialog_open):
        """Method that should implement registration"""

    @abstractmethod
    def open_sport(self, name, timeout=5, **kwargs):
        """Method to open sport from menu"""

    @abstractproperty
    def racing_event_details(self):
        """Property that should return Racing EDP object"""

    @property
    def horse_racing(self):
        return Horseracing(selector=self._page_content)

    @abstractproperty
    def greyhound_event_details(self):
        """Property that should return Racing EDP object"""

    @property
    def horseracing_bet_filter(self):
        return HorseRacingBetFilterPage(selector=self._page_content)

    @property
    def racing_bet_filter_results_page(self):
        return HorseRacingBetFilterResultsPage(selector=self._page_content)

    @property
    def football_bet_filter(self):
        return FootballBetFilterPage(selector=self._page_content)

    @property
    def football_bet_filter_results_page(self):
        return FootballBetFilterResultsPage(selector=self._page_content)

    @property
    def sport_event_details(self):
        return EventDetails(selector=self._page_content)

    @property
    def byb_bet_receipt_panel(self):
        return BYBBetReceipt(selector=self._quick_bet_panel, context=self._driver, timeout=1)

    @property
    def five_a_side_leaderboard(self):
        return FiveASideRulesButtonInfo(selector=self._five_A_side_leaderboard, context=self._driver, timeout=1)

    @property
    def five_A_side_leaderboard(self):
        return self.five_a_side_leaderboard

    @property
    def five_a_side_lobby(self):
        return FiveASideLobbyOverlay(selector=self._five_a_side_lobby, context=self._driver, timeout=1)

    @property
    def byb_betslip_panel(self):
        return BYBBetslip(selector=self._quick_bet_panel, context=self._driver, timeout=2)

    @property
    def greyhound(self):
        return self._greyhound_type(selector=self._page_content)

    @property
    def tote(self):
        return Tote(selector=self._page_content)

    @property
    def football(self):
        return Football(selector=self._page_content)

    @property
    def ice_hockey(self):
        return IceHockey(selector=self._page_content)

    @property
    def sports_page(self):
        return SportPage(selector=self._page_content)

    @property
    def big_competitions(self):
        return BigCompetitionPageBase(selector=self._page_content)

    @property
    def your_call(self):
        return YourCall(selector=self._page_content)

    @property
    def tennis(self):
        return Tennis(selector=self._page_content)

    @property
    def golf(self):
        return Golf(selector=self._page_content)

    @property
    def boxing(self):
        return Boxing(selector=self._page_content)

    @property
    def basketball(self):
        return Basketball(selector=self._page_content)

    @property
    def lotto(self):
        return Lotto(selector=self._page_content)

    # @property
    # def lotto_receipt(self):
    #     return LottoBetReceipt(selector=self._page_content)

    @property
    def baseball(self):
        return Baseball(selector=self._page_content)

    @property
    def badminton(self):
        return Badminton(selector=self._page_content)

    @property
    def american_football(self):
        return AmericanFootball(selector=self._page_content)

    @property
    def handball(self):
        return Handball(selector=self._page_content)

    @property
    def tote_event_details(self):
        return ToteEventDetails(selector=self._page_content)

    @abstractproperty
    def inplay(self):
        """Property that should return In Play object"""

    @property
    def competition_league(self):
        return CompetitionLeaguePage(selector=self._page_content)

    @property
    def favourites(self):
        return Favourites(selector=self._page_content)

    @abstractproperty
    def coupon(self):
        """Property should return coupon page object"""

    @property
    def football_jackpot_receipt(self):
        return FootballJackpotReceipt(selector=self._page_content)

    @property
    def league_search(self):
        return LeagueSearch(selector=self._page_content)

    @property
    def league_page(self):
        return LeaguePage(selector=self._page_content)

    @property
    def account_history(self):
        return AccountHistory(selector=self._page_content)

    @property
    def bet_history(self):
        return BetHistory(selector=self._page_content)

    @property
    def open_bets(self):
        return OpenBets(selector=self._page_content)

    @property
    def open_bet(self):
        return OpenBet(selector=self._page_content)

    @property
    def settings(self):
        return Settings(selector=self._page_content)

    @property
    def transaction_history(self):
        return TransactionHistory(selector=self._transaction_history)

    @property
    def responsible_gambling(self):
        return ResponsibleGambling(selector=self._page_content)

    @property
    def gambling_controls(self):
        return GamblingControls(selector=self._gambling_control)

    @property
    def immediate_24_hours_break(self):
        return Immediate24HoursBreak(selector=self._immediate_break_page_layout, timeout=1)

    @property
    def spending_controls(self):
        return SpendingControlsPage(selector=self._spending_controls_page)

    @property
    def spending_controls_overlay(self):
        return SpendingControlsOverlay(selector=self._spending_controls_overlay_page)

    @property
    def time_out(self):
        return TimeOut(selector=self._page_content)

    @property
    def time_out_confirm(self):
        return TimeOutPasswordConfirm(selector=self._page_content)

    @property
    def limits(self):
        return Limits(selector=self._page_content)

    @property
    def gaming_history(self):
        return GamingHistory(selector=self._page_content)

    @property
    def voucher_code(self):
        return VoucherCode(selector=self._page_content)

    @property
    def freebets(self):
        return Freebets(selector=self._page_content)

    @property
    def freebet_details(self):
        return FreeBetDetails(selector=self._page_content)

    @property
    def promotions(self):
        return Promotions(selector=self._page_content)

    @property
    def promotion_details(self):
        return PromotionDetails(selector=self._page_content)

    @property
    def snooker(self):
        return Snooker(selector=self._page_content)

    @property
    def cycling(self):
        return Cycling(selector=self._page_content)

    @property
    def cricket(self):
        return Cricket(selector=self._page_content)

    @property
    def darts(self):
        return Darts(selector=self._page_content)

    @property
    def formula_1(self):
        return Formula1(selector=self._page_content)

    @property
    def all_sports(self):
        return AllSports(selector=self._page_content)

    @property
    def connect(self):
        return Connect(selector=self._page_content)

    @property
    def betslip_unavailable(self):
        return BetSlipUnavailable(selector=self._page_content)

    @property
    def live_stream(self):
        return LiveStream(selector=self._page_content)

    @property
    def hockey(self):
        return Hockey(selector=self._page_content)

    @property
    def contact_us_page(self):
        return ContactUsOuterPage(selector=self._contact_us_page, timeout=25)

    @property
    def gaming_main_page(self):
        return Gaming(selector=self._gaming_page, context=self._driver, timeout=20)

    @property
    def private_markets_terms_and_conditions_page(self):
        return PrivateMarketsTermsAndConditionsPage(selector=self._contents)

    @property
    def promotion_overlay(self):
        promotion_overlay = find_element(selector=self._promotion_overlay, timeout=2)
        return PromotionOverlay(web_element=promotion_overlay) if promotion_overlay else None

    @property
    def football_overlay(self):
        football_overlay = find_element(selector=self._football_overlay, timeout=2)
        return FootballOverlay(web_element=football_overlay) if football_overlay else None

    @property
    def odds_boost_page(self):
        return OddsBoost(selector=self._page_content)

    @property
    def quick_deposit_desktop(self):
        return QuickDepositDesktop(selector=self._quick_deposit_desktop, timeout=10)

    @abstractmethod
    def enter_value_to_input_field(self, value, on_betslip):
        """
        For tests where it is needed to use mobile keyboard on Mobile Emulation test and send_keys on Desktop test
        will raise NotImplementedError for desktop case that should be handled
        :param value: stake amount, cvv code, deposit amount, etc.
        :param on_betslip: True/False var used in enter_value_to_input_field method to detect keyboard location
          either it a keyboard on betslip (True) or keyboard on quick_bet (False) (is used in Mobile Emulation case)
        :return:
        """

    @abstractmethod
    def toggle_quick_bet(self):
        """Method that should enable/disable quickbet for Mobile tests"""

    @abstractmethod
    def open_betslip(self):
        """Method that should open betslip slide-out for Mobile tests"""

    @abstractmethod
    def close_betslip(self):
        """Method that should close betslip slide-out for Mobile tests"""

    @abstractmethod
    def close_betreceipt(self):
        """Method that should close betreceipt slide-out for Mobile tests"""

    @property
    def marketing_preferences(self):
        return MarketingPreferences(selector=self._page_content)

    @property
    def virtual_sports(self):
        return VirtualSports(selector=self._page_content)

    @property
    def virtual_sports_hub(self):
        return VirtualSectionWrapper(selector=self._page_content,timeout=5)

    @property
    def motor_bikes(self):
        return MotorBikes(selector=self._page_content)

    def go_to_home_page(self):
        self._driver.get(f'https://{tests.HOSTNAME}/')
        self.wait_splash_to_hide()
        self.close_all_dialogs(async_close=False, timeout=1)
        self.wait_content_state(state_name='Home')

    def back_button_click(self):
        # this sleep is needed to avoid delay from header with back button, when we click e.g. on EDP there is
        # small delay and back button is still from prev. page or not active, and click on it will give us nothing
        import time
        time.sleep(2)

        wait_for_result(lambda: self.has_back_button,
                        name=f'"Back button" to appear',
                        timeout=2)
        try:
            self.back_button.click()
        except (VoltronException, StaleElementReferenceException):
            self.back_button.click()

    @property
    def is_safari(self):
        return get_device_properties()['browser'].lower() in self.safari_browser

    @property
    def forgot_password(self):
        return ForgotPassword(selector=self._page_content)

    @property
    def footer_help(self):
        return self._footer_element_help(selector=self._footer_help)

    @property
    def withdrawal(self):
        return Withdraw(selector=self._withdrawal)

    @property
    def responsible_gaming(self):
        return ResponsibleGaming(selector=self._responsible_gambling)

    @property
    def racing_resulted_events_page(self):
        return HorseRacingResultedEventsPage(selector=self._page_content)

    @property
    def racing_headers(self):
        return RacingHeaders(selector=self._page_content)

    @property
    def racing_resulted_tricast_forecast(self):
        return HorseRacingTriForecast(selector=self._page_content)

    @property
    def my_stable(self):
        return MyStable(selector=self._page_content)

    @property
    def account_closure(self):
        return AccountClosure(selector=self._account_closure)

    @property
    def account_closure_overlay(self):
        return AccountClosureOverlay(selector=self._account_closure_overlay)

    @property
    def service_closure(self):
        return ServiceClosure(selector=self._page_content)

    @property
    def self_exclusion(self):
        return SelfExclusion(selector=self._page_content)

    @property
    def self_exclusion_selection(self):
        return SelfExclusionSelection(selector=self._page_content)

    @property
    def self_exclusion_options(self):
        return SelfExclusionOptions(selector=self._page_content)

    @property
    def self_exclusion_dialog(self):
        return SelfExclusionDialog(selector=self._dialog)

    def has_timeline(self, expected_result=True, timeout=2, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, WebDriverException)):
        return wait_for_result(
            lambda: find_element(selector=self._timeline, context=None, bypass_exceptions=bypass_exceptions, timeout=timeout) is not None,
            name=f'{self.__class__.__name__} "Timeline" displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def timeline(self):
        return Timeline(selector=self._timeline)

    @property
    def question_engine(self):
        return QuestionEngine(selector=self._question_engine)

    @property
    def quiz_home_page(self):
        return QuizHomePage(selector=self._quiz_page)

    @property
    def quiz_results_page(self):
        return QuizResultsPage(selector=self._quiz_page)

    @property
    def quiz_page_popup(self):
        return QuizPagePopup(selector=self._quiz_page_popup)

    @property
    def bet_tracker(self):
        return BetTracker(selector=self._page_content)

    @property
    def shop_locator(self):
        return ShopLocator(selector=self._page_content)

    @property
    def player_bets_stats_popup(self):
        return PlayerStatsDialog(selector=self._player_bets_stats_popup)

    def close_qe_or_fanzone_popup(self, name='football', **kwargs):
        """
        @param name: Name of the sport
        @param kwargs: qe: if Question engine related TC qe=True else qe=False
        @param kwargs: fanzone: if Fanzone related TC fanzone=True else fanzone=False
        """
        qe = kwargs.get('qe', False)
        fanzone = kwargs.get('fanzone', False)
        if self.wait_logged_in():
            if self.brand != 'bma':
                if not fanzone:
                    if 'football' in name.lower():
                        try:
                            dialog_syc = self.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                              verify_name=False,
                                                              timeout=10)
                            dialog_syc.dont_show_me_button.click()
                        except Exception:
                            self._logger.info(msg='"Show Your Colors" dialog is not displayed')
            if self.brand == 'bma':
                if not qe:
                    try:
                        dialog_qe = self.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ,
                                                         verify_name=False,
                                                         timeout=10)
                        dialog_qe.dont_show_again.click()
                    except Exception:
                        self._logger.info(msg='"Question Engine" dialog is not displayed')
