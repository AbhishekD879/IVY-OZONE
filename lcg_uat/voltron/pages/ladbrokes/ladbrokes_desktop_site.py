from voltron.pages.coral.desktop_site import DesktopSite
from voltron.pages.ladbrokes.components.byb_betslip import LadbrokesBYBBetslip
from voltron.pages.ladbrokes.components.header_desktop import GlobalHeaderDesktopLadbrokes
from voltron.pages.ladbrokes.components.preferences_overlay import PreferencesOverlayLadbrokes
from voltron.pages.ladbrokes.components.right_column_widgets.right_column import LadbrokesRightColumn
from voltron.pages.ladbrokes.contents.base_contents.competitions_league_desktop_page import CompetitionLeagueDesktopPageLadbrokes
from voltron.pages.ladbrokes.contents.basketball import LadbrokesDesktopBasketball
from voltron.pages.ladbrokes.contents.bet_filter.horseracing_bet_filter import LadbrokesHorseRacingBetFilterPage
from voltron.pages.ladbrokes.contents.bet_filter_page import LadbrokesFootballBetFilterPage
from voltron.pages.ladbrokes.contents.betslip.betslip_desktop import BetSlipDesktopLadbrokes, LottoBetSlipDesktopLadbrokes
from voltron.pages.ladbrokes.contents.coupons_page import CouponPageDesktopLadbrokes
from voltron.pages.ladbrokes.contents.edp.greyhound_event_details import GreyHoundEventDetailsLadbrokesDesktop
from voltron.pages.ladbrokes.contents.edp.racing_event_details import RacingEventDetailsLadbrokesDesktop
from voltron.pages.ladbrokes.contents.edp.sport_event_details import DesktopEventDetailsLadbrokes
from voltron.pages.ladbrokes.contents.football import LadbrokesDesktopFootball
from voltron.pages.ladbrokes.contents.freebets import LadbrokesFreebets
from voltron.pages.ladbrokes.contents.homepage import LadbrokesHomePageDesktop
from voltron.pages.ladbrokes.contents.inplay_desktop import LadbrokesInPlayDesktop
from voltron.pages.ladbrokes.contents.live_stream_desktop import DesktopLadbrokesLiveStream
from voltron.pages.ladbrokes.contents.lobby import Lobby
from voltron.pages.ladbrokes.contents.my_bets.bet_history.bet_history import LadbrokesBetHistory
from voltron.pages.ladbrokes.contents.my_bets.bet_history.bet_history import LadbrokesBetHistoryDesktop
from voltron.pages.ladbrokes.contents.racing import GreyhoundRacingLadbrokes
from voltron.pages.ladbrokes.contents.racing import LadbrokesHorseracing
from voltron.pages.ladbrokes.contents.tennis import LadbrokesDesktopTennis
from voltron.pages.ladbrokes.contents.virtuals.virtual_sports import LadbrokesVirtualSportsDesktop
from voltron.pages.ladbrokes.dialogs.dialog_contents.login import LadbrokesLogInDialog
from voltron.pages.ladbrokes.dialogs.dialog_manager import DialogManagerLadbrokes
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetails
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.pages.ladbrokes.components.one_two_free import OneTwoFree
from voltron.pages.ladbrokes.components.the_grid import TheGrid, InShopCoupons, SavedBetCodes, GenerateGridCard
from voltron.pages.ladbrokes.components.free_ride_overlay import FreeRideOverlay
from voltron.pages.ladbrokes.contents.showusyourcolours import ShowUsYourColours
from voltron.pages.ladbrokes.contents.fanzone import FanZone


class LadbrokesDesktopSite(DesktopSite):
    _preferences_overlay = 'xpath=.//*[contains(@class, "fn-contact-preferences-splash__accept")]'
    _header_type = GlobalHeaderDesktopLadbrokes
    _greyhound_type = GreyhoundRacingLadbrokes
    _betslip = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"]'
    _cash_out = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.cashOut" or @data-crlat="slideContent.2"]]'
    _open_bets = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.openBets" or @data-crlat="slideContent.1"]]'
    _bet_history = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="slideContent.betHistory" or @data-crlat="slideContent.3"]]'
    _bet_receipt = 'xpath=.//*[@data-crlat="widgetAccordion.betslip"][.//*[@data-crlat="betslipReceipt"]]'
    _one_two_free = 'xpath=.//*[@id="one-two-free"]'
    _in_shop_coupons = 'xpath=.//*[@id="digital-coupon-root"]'
    _free_ride_overlay = 'xpath=.//*[@id="freeRideOverlay"]'
    _wait_login_dialog_closed = 20

    @property
    def right_column(self):
        return LadbrokesRightColumn(selector=self._right_column, timeout=5)

    @property
    def dialog_manager(self):
        return DialogManagerLadbrokes()

    @property
    def sport_event_details(self):
        return DesktopEventDetailsLadbrokes(selector=self._page_content)

    @property
    def betslip(self):
        return BetSlipDesktopLadbrokes(selector=self._betslip)

    @property
    def lotto_betslip(self):
        return LottoBetSlipDesktopLadbrokes(selector=self._betslip)

    @property
    def horse_racing(self):
        return LadbrokesHorseracing(selector=self._page_content)

    @property
    def free_ride_overlay(self):
        return FreeRideOverlay(selector=self._free_ride_overlay, timeout=5)

    @property
    def home(self):
        return LadbrokesHomePageDesktop(selector=self._contents)

    @property
    def login_dialog(self):
        return LadbrokesLogInDialog(selector=self._login_dialog, timeout=3)

    @property
    def inplay(self):
        return LadbrokesInPlayDesktop(selector=self._page_content)

    @property
    def virtual_sports(self):
        return LadbrokesVirtualSportsDesktop(selector=self._page_content)

    @property
    def bet_history(self):
        bet_history_shown_on_widget = find_element(selector=self._bet_history, timeout=5)
        if bet_history_shown_on_widget:
            return LadbrokesBetHistoryDesktop(selector=self._bet_history, timeout=1)
        try:
            return LadbrokesBetHistory(selector=self._page_content)
        except Exception as e:
            raise VoltronException(
                f'Bet History is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def settled_bets(self):
        bet_history_shown_on_widget = find_element(selector=self._bet_history, timeout=5)
        if bet_history_shown_on_widget:
            return LadbrokesBetHistoryDesktop(selector=self._bet_history, timeout=1)
        try:
            return LadbrokesBetHistory(selector=self._page_content)
        except Exception as e:
            raise VoltronException(
                f'Bet History is not shown on Right Menu widget and on page tab content. Exception: {e}')

    @property
    def preferences_overlay(self):
        preferences_overlay = find_element(selector=self._preferences_overlay, timeout=2)
        return PreferencesOverlayLadbrokes(web_element=preferences_overlay) if preferences_overlay else None

    @property
    def racing_event_details(self):
        return RacingEventDetailsLadbrokesDesktop(selector=self._page_content)

    @property
    def football(self):
        return LadbrokesDesktopFootball(selector=self._page_content)

    @property
    def basketball(self):
        return LadbrokesDesktopBasketball(selector=self._page_content)

    @property
    def tennis(self):
        return LadbrokesDesktopTennis(selector=self._page_content)

    @property
    def promotion_details(self):
        return PromotionDetails(selector=self._page_content)

    @property
    def byb_betslip_panel(self):
        return LadbrokesBYBBetslip(selector=self._quick_bet_panel, context=self._driver, timeout=2)

    @property
    def greyhound_event_details(self):
        return GreyHoundEventDetailsLadbrokesDesktop(selector=self._page_content)

    @property
    def live_stream(self):
        return DesktopLadbrokesLiveStream(selector=self._page_content)

    @property
    def coupon(self):
        return CouponPageDesktopLadbrokes(selector=self._page_content)

    @property
    def competition_league(self):
        return CompetitionLeagueDesktopPageLadbrokes(selector=self._page_content)

    @property
    def football_bet_filter(self):
        return LadbrokesFootballBetFilterPage(selector=self._page_content)

    @property
    def horseracing_bet_filter(self):
        return LadbrokesHorseRacingBetFilterPage(selector=self._page_content)

    @property
    def freebets(self):
        return LadbrokesFreebets(selector=self._page_content)

    @property
    def one_two_free(self):
        return OneTwoFree(selector=self._one_two_free)

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
