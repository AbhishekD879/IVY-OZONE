import re
from urllib import parse

from voltron.pages.ladbrokes.components.one_two_free import OneTwoFreeWelcomeScreen
from voltron.pages.ladbrokes.components.the_grid import InShopCoupons
from voltron.pages.ladbrokes.contents.fanzone import FanZoneEvents
from voltron.pages.shared import get_driver
from voltron.pages.shared.contents.account_history.account_history import AccountHistory
from voltron.pages.shared.contents.account_history.gaming_history import GamingHistory
from voltron.pages.shared.contents.account_history.transaction_history import TransactionHistory
from voltron.pages.shared.contents.all_sports import AllSports
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.bet_filter.football_bet_filter import FootballBetFilterPage
from voltron.pages.shared.contents.bet_filter.football_bet_filter import FootballBetFilterResultsPage
from voltron.pages.shared.contents.bet_filter.horseracing_bet_filter import HorseRacingBetFilterPage
from voltron.pages.shared.contents.bet_receipt.bet_receipt import BetReceipt
from voltron.pages.shared.contents.bet_receipt.football_jackpot_receipt import FootballJackpotReceipt
# from voltron.pages.shared.contents.bet_receipt.lotto_bet_receipt import LottoBetReceipt
from voltron.pages.shared.contents.betslip.betslip import BetSlip
from voltron.pages.shared.contents.change_password import ChangePassword
from voltron.pages.shared.contents.competitions_league_page import CompetitionLeaguePage
from voltron.pages.shared.contents.connect import Connect, BetTracker, ShopLocator
from voltron.pages.shared.contents.coupons_page import CouponPage
from voltron.pages.shared.contents.edp.freebet_details import FreeBetDetails
from voltron.pages.shared.contents.edp.greyhound_event_details import GreyHoundEventDetails
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetails
from voltron.pages.shared.contents.edp.racing_event_details import RacingEventDetails
from voltron.pages.shared.contents.edp.sport_event_details import EventDetails
from voltron.pages.shared.contents.edp.tote_event_details import ToteEventDetails
from voltron.pages.shared.contents.favourite_matches import Favourites
from voltron.pages.shared.contents.football import Football
from voltron.pages.shared.contents.freebets import Freebets
from voltron.pages.shared.contents.gambling_controls import GamblingControls
from voltron.pages.shared.contents.handball import Handball
from voltron.pages.shared.contents.homepage import HomePage
from voltron.pages.shared.contents.inplay import InPlay
from voltron.pages.shared.contents.league_page import LeaguePage
from voltron.pages.shared.contents.leagues_search import LeagueSearch
from voltron.pages.shared.contents.limits import Limits
from voltron.pages.shared.contents.live_stream import LiveStream
from voltron.pages.shared.contents.lotto import Lotto
from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistory
from voltron.pages.shared.contents.my_bets.cashout import Cashout
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBets
from voltron.pages.shared.contents.my_stable.my_stable_page import MyStable
from voltron.pages.shared.contents.odds_boost import OddsBoost
from voltron.pages.shared.contents.other_sports import Cricket, TableTennis
from voltron.pages.shared.contents.other_sports import Cycling
from voltron.pages.shared.contents.other_sports import Darts
from voltron.pages.shared.contents.other_sports import Diving
from voltron.pages.shared.contents.other_sports import Formula1
from voltron.pages.shared.contents.other_sports import MotorBikes
from voltron.pages.shared.contents.other_sports import Snooker
from voltron.pages.shared.contents.other_sports import Triathlon
from voltron.pages.shared.contents.other_sports import IceHockey
from voltron.pages.shared.contents.other_sports import Volleyball
from voltron.pages.shared.contents.other_sports import Badminton
from voltron.pages.shared.contents.other_sports import Golf
from voltron.pages.shared.contents.other_sports import Esports
from voltron.pages.shared.contents.private_markets import PrivateMarketsTermsAndConditionsPage
from voltron.pages.shared.contents.promotions import Promotions
from voltron.pages.shared.contents.racing import GreyhoundRacing
from voltron.pages.shared.contents.racing import Horseracing
from voltron.pages.shared.contents.registration.three_steps.three_steps import ThreeSteps
from voltron.pages.shared.contents.responsible_gambling import ResponsibleGambling
from voltron.pages.shared.contents.responsible_gambling_info import ResponsibleGamblingInfo
from voltron.pages.shared.contents.settings import Settings
from voltron.pages.shared.contents.tennis import Tennis
from voltron.pages.shared.contents.time_out import TimeOut
from voltron.pages.shared.contents.time_out_confirm import TimeOutPasswordConfirm
from voltron.pages.shared.contents.tote import Tote
from voltron.pages.shared.contents.under_maintenance import UnderMaintenance
from voltron.pages.shared.contents.us_sports import AmericanFootball
from voltron.pages.shared.contents.us_sports import Baseball
from voltron.pages.shared.contents.us_sports import Basketball
from voltron.pages.shared.contents.virtuals.virtual_sports import VirtualSports
from voltron.pages.shared.contents.voucher_code import VoucherCode
from voltron.pages.shared.contents.your_call import YourCall
from voltron.utils import mixins
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.pages.shared.contents.gaelic_football import GaelicFootball
from voltron.pages.shared.contents.rugby_union import RugbyUnion
from voltron.pages.shared.contents.rugby_league import RugbyLeague
from voltron.pages.shared.contents.hockey import Hockey


class BMAContentManager(mixins.LoggingMixin):

    pages = {
        'signup': {
            'default_page': ThreeSteps,
        },
        'home': {
            'default_page': HomePage,
        },
        'football': {
            'default_page': Football,
            'event': EventDetails
        },
        'coupons': {
            'default_page': CouponPage
        },
        'american-football': {
            'default_page': AmericanFootball,
            'event': EventDetails
        },
        'baseball': {
            'default_page': Baseball,
            'event': EventDetails
        },
        'basketball': {
            'default_page': Basketball,
            'event': EventDetails
        },
        'handball': {
            'default_page': Handball,
            'event': EventDetails
        },
        'favourites': {
            'default_page': Favourites,
        },
        'leagues': {
            'default_page': LeaguePage,
        },
        'search-leagues': {
            'default_page': LeagueSearch,
        },
        'competitions': {
            'default_page': CompetitionLeaguePage,
        },
        'horse-racing': {
            'default_page': Horseracing,
            'event': RacingEventDetails
        },
        'bet-finder': {
            'default_page': HorseRacingBetFilterPage
        },
        'bet-filter': {
            'default_page': FootballBetFilterPage,
            'results': FootballBetFilterResultsPage
        },
        'greyhound-racing': {
            'default_page': GreyhoundRacing,
            'event': GreyHoundEventDetails
        },
        'transaction-history': {
            'default_page': TransactionHistory,
        },
        '1-2-free': {
            'default_page': OneTwoFreeWelcomeScreen,
        },
        'settings': {
            'default_page': Settings,
        },
        'bet-history': {
            'default_page': BetHistory,
        },
        'gaming-history': {
            'default_page': GamingHistory,
        },
        'voucher-code': {
            'default_page': VoucherCode,
        },
        'freebets': {
            'default_page': Freebets,
            'event': FreeBetDetails
        },
        'limits': {
            'default_page': Limits,
        },
        'change-password': {
            'default_page': ChangePassword,
        },
        'responsible-gambling': {
            'default_page': ResponsibleGambling,
        },
        'betslip': {
            'default_page': BetSlip,
            'receipt': BetReceipt
        },
        'cashout': {
            'default_page': Cashout
        },
        'football-jackpot-receipt': {
            'default_page': FootballJackpotReceipt
        },
        'promotions': {
            'default_page': Promotions,
            'details': PromotionDetails,
        },
        'az-sports': {
            'default_page': AllSports,
        },
        'open-bets': {
            'default_page': OpenBets,
        },
        'in-play': {
            'default_page': InPlay,
        },
        'ice-hockey': {
            'default_page': IceHockey,
            'event': EventDetails
        },
        'tennis': {
            'default_page': Tennis,
            'event': EventDetails
        },
        'cricket': {
            'default_page': Cricket,
            'event': EventDetails
        },
        'virtual-sports': {
            'default_page': VirtualSports
        },
        'lotto': {
            'default_page': Lotto,
            # 'lottery-receipt': LottoBetReceipt,
            'lotto-49s': Lotto,
            'german-lotto': Lotto,
            'irish-lotto': Lotto,
            'daily-million': Lotto,
            'canadian-lotto': Lotto,
            'ny-lotto': Lotto,
            'singapore-lotto': Lotto,
            'hong-kong-lotto': Lotto,
            'spanish-lotto': Lotto,
            'australian-ozlotto-lottery': Lotto,
            'australian-tattslotto-lottery': Lotto
        },
        'tote': {
            'default_page': Tote,
            'event': ToteEventDetails
        },
        'darts': {
            'default_page': Darts,
            'event': EventDetails
        },
        'snooker': {
            'default_page': Snooker,
            'event': EventDetails
        },
        'cycling': {
            'default_page': Cycling,
        },
        'motor-bikes': {
            'default_page': MotorBikes,
        },
        'formula-1': {
            'default_page': Formula1,
        },
        'diving': {
            'default_page': Diving,
        },
        'retail': {
            'default_page': Connect
        },
        'yourcall': {
            'default_page': YourCall
        },
        'live-stream': {
            'default_page': LiveStream
        },
        'account-history': {
            'default_page': AccountHistory
        },
        'under-maintenance': {
            'default_page': UnderMaintenance
        },
        'triathlon': {
            'default_page': Triathlon
        },
        'private-markets': {
            'default_page': PrivateMarketsTermsAndConditionsPage
        },
        'oddsboost': {
            'default_page': OddsBoost
        },
        'gambling-controls': {
            'default_page': GamblingControls
        },
        'responsible-gambling-info': {
            'default_page': ResponsibleGamblingInfo
        },
        'time-out': {
            'default_page': TimeOut,
            'password-confirm': TimeOutPasswordConfirm
        },
        'gaelic-football': {
            'default_page': GaelicFootball,
            'event': EventDetails
        },
        'rugby-union': {
            'default_page': RugbyUnion,
            'event': EventDetails
        },
        'rugby-league': {
            'default_page': RugbyLeague,
            'event': EventDetails
        },
        'volleyball': {
            'default_page': Volleyball,
            'event': EventDetails
        },
        'hockey': {
            'default_page': Hockey,
            'event': EventDetails
        },
        'badminton': {
            'default_page': Badminton,
            'event': EventDetails
        },
        'golf': {
            'default_page': Golf,
            'event': EventDetails
        },
        'esports': {
            'default_page': Esports,
            'event': EventDetails
        },
        'table-tennis': {
            'default_page': TableTennis,
            'event': EventDetails
        },
        'bet-tracker': {
            'default_page': BetTracker
        },
        'digital-coupons': {
            'default_page': InShopCoupons
        },
        'shop-locator': {
            'default_page': ShopLocator
        },
        'my-stable': {
            'default_page': MyStable
        }
    }

    def __init__(self):
        super(BMAContentManager, self).__init__()
        self._driver = get_driver()

    def _parse_url(self):
        # url = parse.unquote(self._driver.current_url)
        # Changed to Remove encoded url special character 
        url = parse.unquote(parse.quote(self._driver.current_url))
        if 'limits' in url:
            url = url.split(';')[0]
        if url is not None:
            pattern = r'^(http[s]?):\/\/([A-Za-z0-9\-\.]+)\/([\w\-\.,\/\s%]*)(\?.+)?$'
            match = re.match(pattern=pattern, string=url)
            if not match:
                raise GeneralException(
                    f'Current URL "{url}" doesn\'t match pattern "{pattern}"')
            protocol = match.group(1)
            host = match.group(2)
            path = '/'
            query = None
            if match.lastindex >= 3:
                path = match.group(3)
            if match.lastindex >= 4:
                query = match.group(4)
            self._logger.debug('*** Parsed url protocol: "{0}", host: {1}, path: {2}, query {3}'.format(
                protocol,
                host,
                path,
                query if query is not None else '- No query')
            )
            return {
                'protocol': protocol,
                'host': host,
                'path': path,
                'query': query
            }

    def get_content_state(self):
        path = self._parse_url()['path']
        path_array = path.strip('/').split('/')
        if path in ('/', ''):
            self._logger.debug('*** Home Page identified by URL path: "/"')
            return HomePage

        path_array.pop(0) if path_array[0] in ('sport', 'event') else ''
        if 'betslip' in path_array:
            self._logger.debug(f'*** "Betslip" identified by URL path: "{path}"')
            return BetSlip
        if 'freebets' in path_array and path_array[-1].isdigit():
            return FreeBetDetails
        if 'fanzone' in path_array:
            return FanZoneEvents
        if 'superbooster' in path_array:
            return OddsBoost

        value = r'[\d]{6,}'
        if path_array[0] in self.pages.keys():
            if len(path_array) > 1 and any((re.match(value, path_array[-2]),  # for races pages: horse-racing/horse-racing-live/steepledowns/17-04-steepledowns/8814347/win-or-each-way
                                            (re.match(value, path_array[-3]) if len(path_array) >= 3 else False),  # for races pages: horse-racing/horse-racing-live/lingfield/15-00-lingfield/8813366/totepool/exacta
                                            re.match(value, path_array[-2]))):  # for sport pages
                page_class = self.pages[path_array[0]]['event']
                self._logger.debug(f'*** "{page_class.__name__}" page identified by URL path:"{path}"')
                return page_class
            elif len(path_array) > 1 and path_array[1] in self.pages[path_array[0]].keys():
                page_class = self.pages[path_array[0]][path_array[1]]
                self._logger.debug(f'*** "{page_class.__name__}" page identified by URL path: "{path}"')
                return page_class
            elif len(path_array) > 2 and path_array[2] in self.pages[path_array[0]].keys():
                page_class = self.pages[path_array[0]][path_array[2]]
                self._logger.debug(f'*** "{page_class.__name__}" page identified by URL path: "{path}"')
                return page_class
            page_class = self.pages[path_array[0]]['default_page']
            self._logger.debug(f'*** "{page_class.__name__}" page identified by URL path: "{path}"')
            return page_class

        self._logger.warning(f'*** URL path "{path}" is unknown, BaseContent will be returned')
        return BaseContent
