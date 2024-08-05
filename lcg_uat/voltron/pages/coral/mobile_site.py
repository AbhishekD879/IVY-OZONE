import datetime

from faker import Faker
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from voltron.pages.coral.components.byb_betslip import CoralBYBBetslip
from voltron.pages.coral.components.cookies_banner import BMACookieBanner
from voltron.pages.coral.components.header import CoralMobileHeader
from voltron.pages.coral.contents.coral_marketing_preferences import CoralMarketingPreferences
from voltron.pages.coral.contents.edp.promotion_details import CoralPromotionDetails
from voltron.pages.coral.contents.my_bets.bet_history.bet_history import CoralBetHistory
from voltron.pages.coral.contents.registration.three_steps.three_steps import CoralThreeSteps
from voltron.pages.coral.contents.service_closure import CoralServiceClosure
from voltron.pages.coral.contents.set_deposit_limits import CoralCancelLimitChangeRequest
from voltron.pages.coral.contents.set_deposit_limits import CoralSetDepositLimits
from voltron.pages.coral.contents.set_your_deposit_limits import CoralSetYourDepositLimits
from voltron.pages.coral.dialogs.dialog_contents.reward_money import CoralRewardMoney
from voltron.pages.coral.dialogs.dialog_contents.upgrade_your_account import CoralUpgradeYourAccount
from voltron.pages.coral.menus.other_menus import CoralMenus
from voltron.pages.coral.menus.right_menu import CoralRightMenu
from voltron.pages.shared import actions
from voltron.pages.shared import get_cms_config
from voltron.pages.shared.bma_base_site import BMABaseSite
from voltron.pages.shared.components.acca_notification import AccaNotification
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.connect_overlay import ConnectOverlay
from voltron.pages.shared.components.footer_navigation_menu import FooterNavigationMenu
from voltron.pages.shared.components.header import BetSlipCounter
from voltron.pages.shared.components.portal.account_setting import AccountSettingPage
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.quick_bet import QuickBet
from voltron.pages.shared.components.quick_bet import QuickBetOverlay
from voltron.pages.shared.components.recently_played_games_widget import RecentlyPlayedGamesWidget
from voltron.pages.shared.components.tutorial_overlay import TutorialOverlay
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceipt, LottoBetReceipt
from voltron.pages.shared.contents.betslip.betslip import BetSlip, LottoBetSlip
from voltron.pages.shared.contents.coupons_page import CouponPage
from voltron.pages.shared.contents.deposit.deposit import CoralDepositMenu
from voltron.pages.shared.contents.deposit.deposit import GVCDeposit
from voltron.pages.shared.contents.deposit.deposit_limit_warning import GVCDepositLimitWarning
from voltron.pages.shared.contents.deposit.deposit_transaction_details import GVCDepositTransactionDetailsDialog
from voltron.pages.shared.contents.deposit.deposit_transaction_details import GVCDepositTransactionSummary
from voltron.pages.shared.contents.deposit.select_deposit_method import GVCSelectTypeCard
from voltron.pages.shared.contents.edp.greyhound_event_details import GreyHoundEventDetails
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.pages.shared.contents.gambling_controls import GamblingControls
from voltron.pages.shared.contents.homepage import HomePage
from voltron.pages.shared.contents.inplay import InPlay
from voltron.pages.shared.contents.messages import MessagesMobile
from voltron.pages.shared.contents.my_bets.cashout import Cashout
from voltron.pages.shared.contents.registration.three_steps.three_steps import ThreeSteps
from voltron.pages.shared.dialogs.dialog_contents.login import LogIn
from voltron.utils.dialog_action import ActionItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.helpers import get_active_selector
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result
from voltron.utils.window_client_config.client_config import WindowClientConfig
from voltron.pages.shared.contents.time_management import TimeManagement
from voltron.pages.shared.contents.overlay_container import TimeManagementOverlayContainer
from voltron.pages.shared.contents.account_history.payment_history import PaymentHistory
from time import sleep
from voltron.pages.shared.components.stream_and_bet_overlay import StreamAndBetOverlay
from voltron.pages.shared.components.my_stable_onboarding_overlay import MyStableOnboardingOverlay


class MobileSite(BMABaseSite):
    _acca_notification = 'xpath=.//*[@data-crlat="accaNotification"]'
    _quick_bet_overlay = 'xpath=.//*[@data-crlat="loadingOverlay"]'
    _page_content = 'xpath=.//*[@data-uat="pageContent"]'
    _overlay_container = 'xpath=.//*[@class="overlay-container"]'
    _betslip_slide_menu = 'xpath=.//*[@data-crlat="betslipSidebar"]//*[@data-uat="leftColumn"]'
    _right_menu_opened = 'xpath=.//*[@data-crlat="rightMenu.sidebar"]/*[@data-uat="leftColumn"]'
    _animation_in_landscape_mode = 'xpath=.//*[@data-crlat="landscapeOverlay"]'
    _footer_navigation = 'xpath=.//*[@data-uat="footer"]'
    _footer_navigation_type = FooterNavigationMenu
    _betslip_notification = 'xpath=.//*[contains(@class,"betslip-notification")]'
    _header = 'xpath=.//vn-responsive-header | .//vn-header'
    _header_type = CoralMobileHeader
    _login_dialog = 'xpath=.//lh-login'
    _upgrade_your_account = 'xpath=.//lh-cross-product-layout'
    _right_menu = 'xpath=.//vn-account-menu-view'
    _three_steps_registration = 'xpath=.//pt-registration'
    _set_your_deposit_limits = 'xpath=.//pt-lcg-funds-regulation'
    _select_deposit_method = 'xpath=.//*[@class="main"]/*[contains(text(), "Select a deposit method")]/ancestor::body ' \
                             '| .//*[@class="v6-theme channel-MW"] | .//*[@class="v6-theme channel-WC"]' \
                             '| .//*[@class="cashier-wrapper"]'
    _deposit = 'xpath=.//*[@id="applePayError"]/ancestor::body | .//*[@class="deposit-payments-container"] |.//*[@class="cashier-wrapper"]'
    _deposit_pop_up = 'xpath=.//lh-quick-deposit-responsive[.//iframe]'
    _deposit_transaction_details = 'xpath=.//*[contains(@class, "card-success")]'
    _recently_played_games = 'xpath=.//div[contains(@class,"rpg-module-container")]'
    _low_balance = 'xpath=.//*[@aria-label="Low Balance"]'
    _cookie_banner = 'xpath=.//*[contains(@class, "cookie-consent-message")] | .//*[@id="onetrust-button-group"]'
    _marketing_preferences = 'xpath=.//pt-communication'
    _deposit_limit_warning = 'xpath=.//*[contains(@class, "theme channel")][.//form[@id="depLimitsForm"]]'
    _other_menus = 'xpath=.//body'
    _cancel_limit_change_request = 'xpath=.//vn-dialog-content'
    _reward_money = 'xpath=.//div[@id="rtmsNotify"]'
    _main_content = 'xpath=.//div[@id="main-content"]'
    _service_closure = 'xpath=.//vn-app[.//pt-service-closure]'
    _stream_and_bet_overlay = 'xpath=.//*[@class="tint-overlay"]'
    _my_stable_onboarding_overlay = 'xpath=.//*[@data-crlat="myStableOnboardingOverlay"]'

    # RightMenu Account Settings
    _account_settings = 'xpath= //vn-main'

    @property
    def tutorial_overlay(self):
        tutorial_overlay = find_element(selector=self._tutorial_overlay, timeout=5)
        return TutorialOverlay(web_element=tutorial_overlay) if tutorial_overlay else None

    def wait_for_tutorial_overlay(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: find_element(selector=self._tutorial_overlay, timeout=0) is not None,
                               name=f'Tutorial Overlay presence status to be {expected_result}',
                               timeout=timeout,
                               expected_result=expected_result)

    @property
    def stream_and_bet_overlay(self):
        stream_and_bet_overlay = find_element(selector=self._stream_and_bet_overlay, timeout=1)
        return StreamAndBetOverlay(web_element=stream_and_bet_overlay) if stream_and_bet_overlay else None

    def wait_for_stream_and_bet_overlay(self, expected_result=True, timeout=2, bypass_exceptions=Exception):
        return wait_for_result(lambda: find_element(selector=self._stream_and_bet_overlay, timeout=1) is not None,
                               name=f'Tutorial Overlay presence status to be {expected_result}',
                               timeout=timeout,
                               expected_result=expected_result,
                               bypass_exceptions=bypass_exceptions)

    @property
    def my_stable_onboarding_overlay(self):
        my_stable_onboarding_overlay = find_element(selector=self._my_stable_onboarding_overlay, timeout=1)
        return MyStableOnboardingOverlay(web_element=my_stable_onboarding_overlay) if my_stable_onboarding_overlay else None

    def wait_for_my_stable_onboarding_overlay(self, expected_result=True, timeout=2, bypass_exceptions=Exception):
        return wait_for_result(lambda: find_element(selector=self._my_stable_onboarding_overlay, timeout=1) is not None,
                               name=f'My stable onboarding overlay presence status to be {expected_result}',
                               timeout=timeout,
                               expected_result=expected_result,
                               bypass_exceptions=bypass_exceptions)

    @property
    def connect_overlay(self):
        connect_overlay = find_element(selector=self._connect_overlay, timeout=1)
        return ConnectOverlay(web_element=connect_overlay) if connect_overlay else None

    def wait_for_connect_overlay(self, expected_result=True, timeout=5):
        self.wait_splash_to_hide()
        return wait_for_result(lambda: find_element(selector=self._connect_overlay, timeout=0) is not None,
                               name=f'Connect Overlay presence status to be {expected_result}',
                               timeout=timeout,
                               expected_result=expected_result)

    def is_right_menu_opened(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: find_element(selector=self._right_menu, timeout=0) is not None,
            name=f'Right menu presence status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout
        )

    @property
    def navigation_menu(self):
        return self._footer_navigation_type(selector=self._footer_navigation, context=self._driver)

    @property
    def betslip_notification(self):
        return AccaNotification(selector=self._betslip_notification, context=self._driver)

    def has_betslip_notification(self, expected_result: bool = True, timeout: (int, float) = 1.5) -> bool:
        betslip_notification_shown = wait_for_result(
            lambda: BetSlipCounter(selector=self._betslip_notification, context=self._driver, timeout=timeout).is_displayed(timeout=timeout),
            name='betslip_notification is displayed',
            expected_result=expected_result,
            timeout=timeout,
            bypass_exceptions=(VoltronException,
                               NoSuchElementException,
                               StaleElementReferenceException)
        )
        return betslip_notification_shown

    @property
    def right_menu(self):
        return CoralRightMenu(selector=self._right_menu, context=self._driver, timeout=3)

    @property
    def promotion_details(self):
        return CoralPromotionDetails(selector=self._page_content)

    @property
    def acca_notification(self):
        return AccaNotification(selector=self._betslip_notification, timeout=3)

    def wait_for_acca_notification_present(self, expected_result=True):
        return wait_for_result(lambda: find_element(selector=self._betslip_notification, timeout=0) is not None,
                               name='Waiting for Acca notification to be displayed',
                               expected_result=expected_result,
                               timeout=3)

    @property
    def quick_bet_overlay(self):
        return QuickBetOverlay(selector=self._quick_bet_overlay, context=self._driver)

    @property
    def quick_bet_panel(self):
        return QuickBet(selector=self._quick_bet_panel_inner, context=self._driver, timeout=5)

    @property
    def byb_betslip_panel(self):
        return CoralBYBBetslip(selector=self._quick_bet_panel, context=self._driver, timeout=2)

    @property
    def recently_played_games(self):
        return RecentlyPlayedGamesWidget(selector=self._recently_played_games, context=self._driver, timeout=10)

    def open_my_bets_cashout(self):
        self.open_my_bets()
        cms = get_cms_config()
        initial_data = cms.get_initial_data(cached=True)
        cashout_cms = initial_data.get('CashOut', {})
        if not cashout_cms:
            system_config = initial_data.get('systemConfiguration', {})
            cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = cms.get_system_configuration_item('CashOut')
        is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if is_cashout_tab_enabled:
            self.open_bets.tabs_menu.open_tab(vec.bet_history.CASHOUT)
            self.wait_content_state(state_name='Cashout', timeout=10)

    def open_my_bets_open_bets(self):
        self.header.my_bets.click()
        self.wait_content_state(state_name='OpenBets')

    def open_my_bets_settled_bets(self):
        self.open_my_bets_open_bets()
        self.open_bets.tabs_menu.open_tab(vec.bet_history.SETTLED_BETS_TAB_NAME)
        self.wait_content_state(state_name='BetHistory', timeout=10)

    def open_my_bets(self):
        self.open_my_bets_open_bets()

    @property
    def cashout(self):
        return Cashout(selector=self._page_content)

    @property
    def bet_history(self):
        return CoralBetHistory(selector=self._page_content)

    @property
    def settled_bets(self):
        return CoralBetHistory(selector=self._page_content)

    @property
    def inplay(self):
        return InPlay(selector=self._page_content)

    def wait_for_quick_bet_panel(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: find_element(selector=self._quick_bet_panel, timeout=0) is not None,
                               expected_result=expected_result,
                               name='Quick Bet panel to be displayed',
                               timeout=timeout)

    def wait_quick_bet_overlay_to_hide(self, timeout=25):
        quick_bet_overlay = find_element(selector=self._quick_bet_overlay, timeout=1)
        if quick_bet_overlay:
            self.quick_bet_overlay.wait_to_hide(timeout=timeout)

    def add_first_selection_from_quick_bet_to_betslip(self, timeout=2):
        if self.wait_for_quick_bet_panel(timeout=timeout):
            self.quick_bet_panel.add_to_betslip_button.click()
            self.wait_for_quick_bet_panel(expected_result=False)
            self.wait_quick_bet_overlay_to_hide(timeout=6)

    def wait_for_deposit_pop_up_closed(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: find_element(selector=self._deposit_pop_up, timeout=0) is None,
                               expected_result=expected_result,
                               name='"Deposit" window to be closed',
                               timeout=timeout)

    @property
    def marketing_preferences(self):
        return CoralMarketingPreferences(selector=self._marketing_preferences, context=self._driver, timeout=3)

    @property
    def animation_in_landscape(self):
        return ComponentBase(selector=self._animation_in_landscape_mode, context=self._driver, timeout=1)

    @property
    def login_dialog(self):
        return LogIn(selector=self._login_dialog, timeout=3)

    @property
    def home(self):
        return HomePage(selector=self._contents)

    @property
    def upgrade_your_account(self):
        return CoralUpgradeYourAccount(selector=self._upgrade_your_account, timeout=30)

    def _wait_for_login_dialog(self, timeout):
        if wait_for_result(lambda: find_element(selector=self._login_dialog, timeout=0),
                           timeout=timeout,
                           name=f'{self.__class__.__name__} Login dialog to be shown'):
            dialog = self.login_dialog
            actual_dialog_name = dialog.name
            dialog_name = vec.dialogs.DIALOG_MANAGER_LOG_IN
            if actual_dialog_name not in ['LOG IN', 'LOGIN', 'Login']:
                raise VoltronException(f'Actual Dialog name "{actual_dialog_name}" != Expected "{dialog_name}"')
            return dialog
        else:
            return None

    def wait_for_dialog(self, dialog_name: str, verify_name: bool = True, timeout: (int, float) = 10):
        """
        Method used for checking dialog presence on UI
        :param dialog_name: actual dialog name as on UI
        :param verify_name: parameter for comparing expected dialog title with actual
        :param timeout: timeout for waiting
        :return: dialog object in case of success, None if required dialog is not found
        """
        # Note: handling for login dialog here is temporary.
        # in case if ANY new coral dialog will be found – it should be handled through Coral Dialog Manager
        if dialog_name == vec.dialogs.DIALOG_MANAGER_LOG_IN:
            return self._wait_for_login_dialog(timeout=timeout)
        else:
            return self.dialog_manager.wait_for_dialog(dialog_name=dialog_name, timeout=timeout,
                                                       verify_name=verify_name)

    def wait_logged_in(self, login_criteria=None, timeout=5):
        if login_criteria == 'betslip_balance':
            return wait_for_result(lambda: self.betslip.header.has_user_balance,
                                   name='User balance is displayed on Betslip',
                                   timeout=timeout)
        if login_criteria == 'betreceipt_balance':
            return wait_for_result(lambda: self.bet_receipt.user_header.has_user_balance,
                                   name='User balance is displayed on Betreceipt',
                                   timeout=timeout)
        return wait_for_result(
            lambda: self.header.has_right_menu() and self.header.right_menu_button.is_displayed(timeout=1),
            timeout=timeout,
            name='Right Menu button to be displayed',
            bypass_exceptions=VoltronException)

    def logout(self, timeout=10):
        self.header.right_menu_button.click()
        self.right_menu.logout()
        logged_out = self.wait_logged_out(timeout=timeout)
        if not logged_out:
            raise VoltronException('User is not logged out')
        if self._driver.current_url.startswith('http:'):
            # todo: reason is the same as VANO-768
            self._driver.get(f'https://{tests.HOSTNAME}')

    @property
    def select_deposit_method(self):
        return GVCSelectTypeCard(selector=self._select_deposit_method, timeout=10)

    @property
    def deposit(self):
        selectors = [self._deposit, self._deposit_pop_up]
        selector = get_active_selector(selectors=selectors)

        if selector == self._deposit:
            return GVCDeposit(selector=selector, timeout=5)
        elif selector == self._deposit_pop_up:
            return CoralDepositMenu(selector=selector, timeout=5)

        raise VoltronException(f'Can not recognize deposit type. All selectors from "{selectors}" are not available')

    @property
    def deposit_transaction_details(self):
        selectors = [self._deposit_transaction_details, self._deposit_pop_up]
        selector = get_active_selector(selectors=selectors)

        if selector == self._deposit_transaction_details:
            return GVCDepositTransactionSummary(selector=self._deposit_transaction_details, timeout=5)
        elif selector == self._deposit_pop_up:
            return GVCDepositTransactionDetailsDialog(selector=selector, timeout=5)

        raise VoltronException(f'Can not recognize deposit type. All selectors from "{selectors}" are not available')

    def register_new_user(
            self,
            social_title='Mr.',
            first_name=Faker().first_name_female(),
            last_name=Faker().last_name_female(),
            birth_date='01-Jun-1977',
            country='United Kingdom',
            post_code='PO16 7GZ',
            address_one='1 Owen Close',
            city='Fareham',
            mobile='+447537152317',
            email=None,
            username=None,
            password=tests.settings.default_password,
            currency='GBP',
            deposit_limit=None,
            terms_and_conditions=True,
            **kwargs
    ):
        expected_content_state = kwargs.get('expected_content_state', 'Homepage')
        self.header.join_us.click()
        username = username if username else f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[
                                             :15]
        email = email if email else f'test+{username}@internalgvc.com'
        self.three_steps_registration.complete_all_registration_steps(social_title=social_title,
                                                                      first_name=first_name,
                                                                      last_name=last_name,
                                                                      birth_date=birth_date,
                                                                      country=country,
                                                                      post_code=post_code,
                                                                      address_one=address_one,
                                                                      city=city,
                                                                      mobile=mobile,
                                                                      email=email,
                                                                      username=username,
                                                                      password=password,
                                                                      currency=currency)
        if country == 'United Kingdom':
            self.set_your_deposit_limits.set_limits(deposit_limit=deposit_limit)
        wait_for_result(lambda: self.select_deposit_method.close_button.is_displayed(), timeout=15)
        sleep(2)
        self.select_deposit_method.close_button.click()
        self.wait_content_state(expected_content_state)
        self.close_all_dialogs(async_close=False, timeout=4) if kwargs.get('close_dialogs',
                                                                           True) else self._logger.info(
            '*** Bypassing close all dialogs')
        self.close_all_banners(async_close=False) if kwargs.get('close_banners', True) else self._logger.info(
            '*** Bypassing close all banners')

    @property
    def set_your_deposit_limits(self):
        return CoralSetYourDepositLimits(selector=self._set_your_deposit_limits)

    @property
    def betslip(self):
        return BetSlip(selector=self._betslip_slide_menu)

    @property
    def lotto_betslip(self):
        return LottoBetSlip(selector=self._betslip_slide_menu)

    def has_betslip_opened(self, expected_result: bool = True, timeout: (int, float) = 1.5) -> bool:
        """
        Waits for betslip to be opened/closed
        :param expected_result: True or False
        :param timeout: timeout
        :return: True or False
        """
        return wait_for_result(
            lambda: 'is-visible' in find_element(selector=self._betslip_slide_menu).get_attribute('class'),
            name=f'{self.__class__.__name__} Betslip opened state to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout
        )

    @property
    def bet_receipt(self):
        return BetReceipt(selector=self._betslip_slide_menu)

    @property
    def lotto_bet_receipt(self):
        return LottoBetReceipt(selector=self._betslip_slide_menu)

    def is_bet_receipt_displayed(self, expected_result=True, timeout=5):
        """
        Verifies if bet receipt is shown or not.
        :param expected_result: Specifies the result the function waits for.
        :param timeout: Specifies waiting time.
        :return: True if bet receipt is displayed, False otherwise
        """
        bet_receipt_shown = wait_for_result(
            lambda: BetReceipt(selector=self._betslip_slide_menu, timeout=1).is_displayed(timeout=1),
            name='BetReceipt is displayed',
            expected_result=expected_result,
            timeout=timeout,
            bypass_exceptions=(VoltronException,
                               NoSuchElementException,
                               StaleElementReferenceException)
        )
        return bet_receipt_shown

    @property
    def racing_event_details(self):
        return RacingEventDetails(selector=self._page_content)

    @property
    def greyhound_event_details(self):
        return GreyHoundEventDetails(selector=self._page_content)

    @property
    def coupon(self):
        return CouponPage(selector=self._page_content)

    @property
    def three_steps_registration(self):
        if tests.settings.brand == 'bma' and tests.settings.backend_env == 'tst2':
            # TODO: remove when username registration feature will be released
            return CoralThreeSteps(selector=self._three_steps_registration, timeout=30)
        else:
            return ThreeSteps(selector=self._three_steps_registration, timeout=30)

    def open_sport(self, name, timeout=5, **kwargs):
        self.home.menu_carousel.click_item(name.upper())
        content_state = kwargs.get('content_state', name)
        self.wait_content_state(content_state, timeout=timeout)
        self.close_qe_or_fanzone_popup(name=name, **kwargs)

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

    def change_odds_format(self, odds_format):
        # TODO revert once VANO-768 will be resolved
        # self.navigate_to_my_account_page(name=self.window_client_config.settings_menu_title)
        # self.right_menu.click_item(self.window_client_config.betting_settings_menu_title)
        # self.wait_content_state('Settings', timeout=5)
        self._driver.get(f'https://{tests.HOSTNAME}/settings' + '?automationtest=true')
        self.wait_splash_to_hide()
        self.wait_content_state('Settings', timeout=5)
        if odds_format == vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC:
            button = self.settings.fractional_btn
        elif odds_format == vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC:
            button = self.settings.decimal_btn
        else:
            raise VoltronException(f'Odds format "{odds_format}" is not available')
        button.click()
        return button.is_selected(name=f'Odds format "{odds_format}" to be selected')

    def enter_value_to_input_field(self, value, on_betslip=True):
        keyboard = self.betslip.betnow_section.keyboard if on_betslip else self.quick_bet_panel.selection.keyboard
        if not keyboard.is_displayed(name='Numeric keyboard shown', timeout=3):
            raise VoltronException('Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=value)

    def toggle_quick_bet(self):
        # TODO revert once VANO-768 will be resolved
        # self.navigate_to_my_account_page(name='Settings')
        # self.right_menu.click_item('Betting Settings')
        self._driver.get(f'https://{tests.HOSTNAME}/settings' + '?automationtest=true')
        self.wait_splash_to_hide()
        self.settings.allow_quick_bet.click()
        # TODO revert once VANO-1008 be resolved
        # self.navigate_to_page(name='/')
        self._driver.get(f'https://{tests.HOSTNAME}')
        self.wait_splash_to_hide()
        self.wait_content_state('HomePage')

    def open_betslip(self):
        try:
            self.header.bet_slip_counter.click()
        except VoltronException:
            self.betslip_notification.click()
        self.betslip.wait_for_betslip_widget_displayed()

    def close_betslip(self):
        self.betslip.close_button.click()

    def close_betreceipt(self):
        self.bet_receipt.close_button.click()

    def add_card_to_user(self, deposit_value=20, card_number=None, cvv_2=None, card_expiry_date=None):
        """
        Method makes first initial deposit for user, also in result of this execution

        :param deposit_value: Amount to deposit, 20 by default (Limit is 22 per transaction for coral beta env)
        :param card_number: Card number to enter, if not specified, default will be used
        :param cvv_2: Card's cvv2 to enter, if not specified, default will be used
        :param card_expiry_date: Card's expiry date to enter, if not specified, current date will be shifted
        """
        card_number = tests.settings.master_card if not card_number else card_number
        cvv_2 = tests.settings.master_card_cvv if not cvv_2 else cvv_2
        if not card_expiry_date:
            now = datetime.datetime.now()
            shifted_year = str(now.year + 5)
            card_expiry_date = f'{now.month:02d}/{shifted_year[:-2]}'

        self.header.right_menu_button.click()
        self.right_menu.click_item(item_name=self.window_client_config.cashier_menu_title)
        self.right_menu.click_item(item_name=self.window_client_config.deposit_menu_title)
        self.select_deposit_method.master_card_button.click()
        self.deposit.add_new_card_and_deposit(amount=deposit_value,
                                              card_number=card_number,
                                              cvv_2=cvv_2,
                                              expiry_date=card_expiry_date)

        self.deposit_transaction_details.ok_button.click()
        self.wait_content_state('HomePage', timeout=5)

    def deposit_via_master_card(self, deposit_value=20, cvv_2=None):
        """
        Method allows to deposit using master card

        :param deposit_value: Amount to deposit, 20 by default (Limit is 22 per transaction for coral beta env)
        :param cvv_2: Card's cvv2 to enter, if not specified, default will be used
        """
        cvv_2 = tests.settings.master_card_cvv if not cvv_2 else cvv_2

        self.header.right_menu_button.click()
        self.right_menu.click_item(item_name=self.window_client_config.cashier_menu_title)
        self.right_menu.click_item(item_name=self.window_client_config.deposit_menu_title)
        self.select_deposit_method.master_card_button.click()
        self.deposit.add_new_card_and_deposit(amount=deposit_value,
                                              cvv_2=cvv_2)

        self.deposit_transaction_details.ok_button.click()
        self.wait_content_state('HomePage', timeout=5)

    @property
    def window_client_config(self):
        return WindowClientConfig(config=self.get_window_client_config, brand=self.brand)

    def has_low_balance(self, expected_result=True, timeout=5):
        result = wait_for_result(lambda: find_element(selector=self._low_balance, timeout=0) is not None,
                                 expected_result=expected_result,
                                 name='Low balance tooltip to appear',
                                 timeout=timeout)
        return result

    @property
    def cookie_banner(self):
        cookie_banner = find_element(selector=self._cookie_banner, timeout=1)
        return BMACookieBanner(web_element=cookie_banner) if cookie_banner else None

    def is_cookie_banner_shown(self, expected_result=True):
        banner = self.cookie_banner
        if expected_result:
            return banner.is_displayed() if banner else False
        return not banner.wait_for_element_disappear() if banner else False

    @property
    def service_closure(self):
        return CoralServiceClosure(selector=self._service_closure)

    @property
    def menus(self):
        return CoralMenus(selector=self._other_menus, context=self._driver, timeout=3)

    @property
    def set_deposit_limits(self):
        return CoralSetDepositLimits(selector=self._main_content)

    @property
    def cancel_limit_change_request(self):
        return CoralCancelLimitChangeRequest(selector=self._cancel_limit_change_request)

    @property
    def deposit_limit_warning(self):
        return GVCDepositLimitWarning(selector=self._deposit_limit_warning, timeout=5)

    @property
    def reward_money(self):
        reward_money = find_element(selector=self._reward_money, timeout=0.5)
        return CoralRewardMoney(web_element=reward_money) if reward_money else None

    def close_all_dialogs(self, async_close=True, timeout=6, ignored_dialogs=()):
        ignored_dialogs = ignored_dialogs if ignored_dialogs else (vec.dialogs.DIALOG_MANAGER_YOU_ARE_LOGGED_OUT,)
        close_dialogs = ActionItem(
            name='Close all dialogs',
            action_func=lambda: self.dialog_manager.perform_dialog_default_action(ignored_dialogs=ignored_dialogs),
            expected_result=True,
            timeout=timeout
        )
        close_bonus = ActionItem(
            name='Close reward money',
            action_func=lambda: self.reward_money and self.reward_money.close_button.click(),
            expected_result=True,
            timeout=timeout
        )
        if async_close:
            actions.push(close_dialogs)
            actions.push(close_bonus)
        else:
            wait_for_result(
                close_dialogs.action,
                name=f'{close_dialogs.name}',
                timeout=timeout
            )
            wait_for_result(
                close_bonus.action,
                name=f'{close_bonus.name}',
                timeout=1
            )

    @property
    def gambling_controls_page(self):
        return GamblingControls(selector=self._page_content)

    @property
    def messages(self):
        return MessagesMobile(selector=self._page_content)

    def has_recently_played_games(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: find_element(selector=self._recently_played_games, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'RecentlyPlayedGamesWidget status to be "{expected_result}"')

    @property
    def time_management_page(self):
        return TimeManagement(selector=self._page_content)

    @property
    def time_management_overlay(self):
        return TimeManagementOverlayContainer(selector=self._overlay_container)

    @property
    def payment_history(self):
        return PaymentHistory(selector=self._other_menus)

    @property
    def account_settings(self):
        return AccountSettingPage(selector=self._account_settings, timeout=2)