from faker import Faker
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from voltron.pages.coral.dialogs.dialog_contents.my_inbox import CoralMyInbox
from voltron.pages.coral.mobile_site import MobileSite
from voltron.pages.ladbrokes.components.byb_betslip import LadbrokesBYBBetslip
from voltron.pages.ladbrokes.components.header import GlobalHeaderLadbrokes
from voltron.pages.ladbrokes.components.one_two_free import OneTwoFree
from voltron.pages.ladbrokes.components.preferences_overlay import PreferencesOverlayLadbrokes
from voltron.pages.ladbrokes.components.quick_bet import QuickBetLadbrokes
from voltron.pages.ladbrokes.components.the_grid import TheGrid, InShopCoupons, SavedBetCodes, GenerateGridCard
from voltron.pages.ladbrokes.contents.lobby import Lobby
from voltron.pages.ladbrokes.contents.basketball import LadbrokesMobileBasketball
from voltron.pages.ladbrokes.contents.bet_filter.horseracing_bet_filter import LadbrokesHorseRacingBetFilterPage
from voltron.pages.ladbrokes.contents.bet_filter_page import LadbrokesFootballBetFilterPage
from voltron.pages.ladbrokes.contents.bet_receipt.bet_receipt import LadbrokesBetReceipt
from voltron.pages.ladbrokes.contents.betslip.betslip import BetSlipLadbrokes, LottoBetSlipLadbrokes
from voltron.pages.ladbrokes.contents.coupons_page import CouponPageLadbrokes
from voltron.pages.ladbrokes.contents.edp.greyhound_event_details import GreyHoundEventDetailsLadbrokes
from voltron.pages.ladbrokes.contents.edp.racing_event_details import RacingEventDetailsLadbrokes
from voltron.pages.ladbrokes.contents.edp.sport_event_details import EventDetailsLadbrokes
from voltron.pages.ladbrokes.contents.football import LadbrokesMobileFootball
from voltron.pages.ladbrokes.contents.freebets import LadbrokesFreebets
from voltron.pages.ladbrokes.contents.gaming_overlay import LadbrokesGamingOverlay
from voltron.pages.ladbrokes.contents.homepage import LadbrokesHomePage
from voltron.pages.ladbrokes.contents.inplay import LadbrokesInPlay
from voltron.pages.ladbrokes.contents.my_bets.bet_history.bet_history import LadbrokesBetHistory
from voltron.pages.ladbrokes.contents.racing import GreyhoundRacingLadbrokes
from voltron.pages.ladbrokes.contents.racing import LadbrokesHorseracing
from voltron.pages.ladbrokes.contents.settings import SettingsLadbrokes
from voltron.pages.ladbrokes.contents.tennis import LadbrokesMobileTennis
from voltron.pages.ladbrokes.contents.virtuals.virtual_sports import LadbrokesVirtualSports
from voltron.pages.ladbrokes.dialogs.dialog_contents.login import LadbrokesLogInDialog
from voltron.pages.ladbrokes.dialogs.dialog_manager import DialogManagerLadbrokes
from voltron.pages.ladbrokes.menus.other_menus import LadbrokesMenus
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.luckydip import LuckyDipGotItPanel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.quick_bet_betslip_panel import QuickDeposit
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetails
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result
from time import sleep
from voltron.pages.ladbrokes.components.free_ride_overlay import FreeRideOverlay
from voltron.pages.ladbrokes.contents.showusyourcolours import ShowUsYourColours
from voltron.pages.ladbrokes.contents.fanzone import FanZone


class LadbrokesMobileSite(MobileSite):
    _preferences_overlay = 'xpath=.//*[@class="contact-preferences-splash__wrapper"]'
    _banking = 'xpath=.//*[@data-crlat="racingEventPage.subheader"]'
    _my_account_page_content = 'xpath=.//*[@data-crlat="myAccountPageContent"]'
    _header_type = GlobalHeaderLadbrokes
    _greyhound_type = GreyhoundRacingLadbrokes
    _close_button = 'xpath=.//*[@data-tracking-event="header-close"]'
    _quick_deposit_panel = 'xpath=.//*[@data-crlat="quickDepositPanel"]'
    _wait_login_dialog_closed = 25
    _one_two_free = 'xpath=.//*[@id="one-two-free"]'
    _in_shop_coupons = 'xpath=.//*[@id="digital-coupon-root"]'
    # Gaming page
    _gaming_overlay = 'xpath=.//gaming-overlay[@class="isActive"]'
    _my_inbox = 'xpath=.//lh-inbox'
    _free_ride_overlay = 'xpath=.//*[@id="freeRideOverlay"]'
    _lucky_dip_got_it_panel = 'xpath=.//*[@class="modal-body got-it-btn"] | .//*[@class="modal-body"]'

    def __init__(self, *args, **kwargs):
        super(LadbrokesMobileSite, self).__init__()
        if kwargs.get('brand'):
            self._logger.warning(f'Parameter brand "{kwargs.get("brand")}" is ignored for {self.__class__.__name__}')
        self.brand = 'ladbrokes'
        self._content_state_name = ''
        self._driver = get_driver()

    @property
    def dialog_manager(self):
        return DialogManagerLadbrokes()

    def open_sport(self, name, timeout=5, **kwargs):
        ladbrokes_name = name.title()
        self.home.menu_carousel.click_item(ladbrokes_name)
        content_state = kwargs.get('content_state', name)
        self.wait_content_state(content_state, timeout=timeout)
        self.close_qe_or_fanzone_popup(name=name, **kwargs)

    @property
    def inplay(self):
        return LadbrokesInPlay(selector=self._page_content)

    @property
    def betslip(self):
        return BetSlipLadbrokes(selector=self._betslip_slide_menu)

    @property
    def lotto_betslip(self):
        return LottoBetSlipLadbrokes(selector=self._betslip_slide_menu)

    @property
    def free_ride_overlay(self):
        return FreeRideOverlay(selector=self._free_ride_overlay, timeout=5)

    @property
    def home(self):
        return LadbrokesHomePage(selector=self._contents)

    @property
    def racing_event_details(self):
        return RacingEventDetailsLadbrokes(selector=self._page_content)

    @property
    def greyhound_event_details(self):
        return GreyHoundEventDetailsLadbrokes(selector=self._page_content)

    @property
    def promotion_details(self):
        return PromotionDetails(selector=self._page_content)

    @property
    def back_button(self):
        return self.header.back_button

    @property
    def has_back_button(self):
        return self.header.has_back_button

    @property
    def close(self):
        return ButtonBase(selector=self._close_button)

    @property
    def settings(self):
        return SettingsLadbrokes(selector=self._page_content)

    @property
    def sport_event_details(self):
        return EventDetailsLadbrokes(selector=self._page_content)

    @property
    def preferences_overlay(self):
        preferences_overlay = find_element(selector=self._preferences_overlay, timeout=2)
        return PreferencesOverlayLadbrokes(web_element=preferences_overlay) if preferences_overlay else None

    def wait_logged_out(self, timeout=10):
        return wait_for_result(lambda: self.header.sign_in_join_button.is_displayed(timeout=0),
                               name='Login Button should be visible',
                               expected_result=True,
                               timeout=timeout,
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException))

    @property
    def byb_betslip_panel(self):
        return LadbrokesBYBBetslip(selector=self._quick_bet_panel, context=self._driver, timeout=2)

    @property
    def horse_racing(self):
        return LadbrokesHorseracing(selector=self._page_content)

    @property
    def bet_history(self):
        return LadbrokesBetHistory(selector=self._page_content)

    @property
    def settled_bets(self):
        return LadbrokesBetHistory(selector=self._page_content)

    @property
    def coupon(self):
        return CouponPageLadbrokes(selector=self._page_content)

    @property
    def one_two_free(self):
        return OneTwoFree(selector=self._one_two_free)

    @property
    def horseracing_bet_filter(self):
        return LadbrokesHorseRacingBetFilterPage(selector=self._page_content)

    def open_my_bets_open_bets(self):
        self.open_my_bets()

    def open_my_bets(self):
        menu_items = self.navigation_menu.items_as_ordered_dict
        my_bets = menu_items.get(vec.sb.MY_BETS_FOOTER_ITEM)
        if my_bets:
            my_bets.click()
        else:
            self.header.right_menu_button.click()
            history_title = self.window_client_config.history_title
            right_menu = self.right_menu
            right_menu.click_item(item_name=history_title)
            wait_for_result(lambda: right_menu.header.title == history_title,
                            name='Wait for header to change')
            self.menus.click_item(item_name=self.window_client_config.betting_history_title)
            self.wait_content_state(state_name='BetHistory')
            self.bet_history.tabs_menu.open_tab(vec.bet_history.OPEN_BETS_TAB_NAME)
        self.wait_content_state(state_name='OpenBets')

    def open_my_bets_settled_bets(self):
        self.open_my_bets()
        self.open_bets.tabs_menu.open_tab(vec.bet_history.SETTLED_BETS_TAB_NAME)

    @property
    def bet_receipt(self):
        return LadbrokesBetReceipt(selector=self._betslip_slide_menu)

    def navigate_to_my_account(self, name='Personal Details'):
        self.navigate_to_right_menu_item(name)

    def navigate_to_my_account_page(self, name, timeout=0):
        self.navigate_to_my_account(name)

    @property
    def login_dialog(self):
        return LadbrokesLogInDialog(selector=self._login_dialog, timeout=3)

    @property
    def menus(self):
        return LadbrokesMenus(selector=self._other_menus, context=self._driver, timeout=3)

    @property
    def quick_deposit_panel(self):
        return QuickDeposit(selector=self._quick_deposit_panel, context=self._driver, timeout=2)

    def wait_for_quick_deposit_panel(self, expected_result=True, timeout=15):
        return wait_for_result(
            lambda: find_element(selector=self._quick_deposit_panel, timeout=0) is not None,
            expected_result=expected_result,
            name='Quick Bet panel to be displayed',
            timeout=timeout)

    @property
    def quick_bet_panel(self):
        return QuickBetLadbrokes(selector=self._quick_bet_panel_inner, context=self._driver, timeout=5)

    @property
    def lucky_dip_got_it_panel(self):
        return LuckyDipGotItPanel(selector=self._lucky_dip_got_it_panel, context=self._driver, timeout=5)

    def go_to_home_page(self):
        home_on_footer = find_element(selector='xpath=//*[@data-crlat="menuItem" and @href="/"]')
        if home_on_footer:
            home_on_footer.click()
            self.wait_content_state('HomePage')

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
        self.header.sign_in.click()
        self.login_dialog.create_an_account.click()
        username = username if username else f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15]
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
        self.close_all_dialogs(async_close=False, timeout=4) if kwargs.get('close_dialogs', True) else self._logger.info('*** Bypassing close all dialogs')
        self.close_all_banners(async_close=False) if kwargs.get('close_banners', True) else self._logger.info('*** Bypassing close all banners')

    @property
    def football(self):
        return LadbrokesMobileFootball(selector=self._page_content)

    @property
    def basketball(self):
        return LadbrokesMobileBasketball(selector=self._page_content)

    @property
    def tennis(self):
        return LadbrokesMobileTennis(selector=self._page_content)

    @property
    def virtual_sports(self):
        return LadbrokesVirtualSports(selector=self._page_content)

    @property
    def football_bet_filter(self):
        return LadbrokesFootballBetFilterPage(selector=self._page_content)

    @property
    def gaming_overlay(self):
        return LadbrokesGamingOverlay(selector=self._gaming_page, context=self._driver, timeout=20)

    @property
    def freebets(self):
        return LadbrokesFreebets(selector=self._page_content)

    @property
    def my_inbox(self):
        return CoralMyInbox(selector=self._my_inbox, timeout=3)

    @property
    def grid(self):
        return TheGrid(selector=self._page_content)

    @property
    def in_shop_coupons(self):
        return InShopCoupons(selector=self._in_shop_coupons)

    @property
    def saved_bet_codes(self):
        return SavedBetCodes(selector=self._page_content)

    @property
    def generate_grid_card(self):
        return GenerateGridCard(selector=self._page_content)

    @property
    def lobby(self):
        return Lobby(selector=self._page_content)

    @property
    def show_your_colors(self):
        return ShowUsYourColours(selector=self._page_content)

    @property
    def fanzone(self):
        return FanZone(selector=self._page_content)
