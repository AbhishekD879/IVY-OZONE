# flake8: noqa
import tests
from voltron.environments.constants.base.account import Account
from voltron.environments.constants.base.app import App
from voltron.environments.constants.base.bet_history import BetHistory
from voltron.environments.constants.base.bet_finder import BetFinder
from voltron.environments.constants.base.betslip import Betslip
from voltron.environments.constants.base.big_competitions import BigCompetitions
from voltron.environments.constants.base.bma import BMA
from voltron.environments.constants.base.bpp import BPP
from voltron.environments.constants.base.colors import Colors
from voltron.environments.constants.base.coupons import Coupons
from voltron.environments.constants.base.dialogs import Dialogs
from voltron.environments.constants.base.ema import EMA
from voltron.environments.constants.base.favourites import Favourites
from voltron.environments.constants.base.five_a_side import FiveASide
from voltron.environments.constants.base.football import Football
from voltron.environments.constants.base.gvc import GVC
from voltron.environments.constants.base.inplay import Inplay
from voltron.environments.constants.base.live_stream import LiveStream
from voltron.environments.constants.base.lotto import Lotto
from voltron.environments.constants.base.odds_boost import OddsBoost
from voltron.environments.constants.base.olympics import Olympics
from voltron.environments.constants.base.promotions import Promotions
from voltron.environments.constants.base.question_engine import QuestionEngine
from voltron.environments.constants.base.quickbet import Quickbet
from voltron.environments.constants.base.quickdeposit import Quickdeposit
from voltron.environments.constants.base.racing import Racing
from voltron.environments.constants.base.retail import Retail
from voltron.environments.constants.base.siteserve import SiteServe
from voltron.environments.constants.base.sportsbook import SB
from voltron.environments.constants.base.sportsbook_desktop import SBDesktop
from voltron.environments.constants.base.stats import Stats
from voltron.environments.constants.base.tote import Tote
from voltron.environments.constants.base.uk_tote import UKTote
from voltron.environments.constants.base.virtuals import Virtuals
from voltron.environments.constants.base.yourcall import Yourcall
from voltron.environments.constants.ladbrokes.fanzone import FANZONE

if tests.settings.brand == 'bma':
    from voltron.environments.constants.bma.ema import CoralEMA as EMA
    from voltron.environments.constants.bma.sportsbook import CoralSB as SB
    from voltron.environments.constants.bma.betslip import CoralBetslip as Betslip
    from voltron.environments.constants.bma.racing import CoralRacing as Racing
    from voltron.environments.constants.bma.bet_history import CoralBetHistory as BetHistory
    from voltron.environments.constants.bma.bma import CoralBMA as BMA
    from voltron.environments.constants.bma.tote import CoralTote as Tote
    from voltron.environments.constants.bma.quickbet import CoralQuickbet as Quickbet
    from voltron.environments.constants.bma.yourcall import CoralYourcall as Yourcall
    from voltron.environments.constants.bma.five_a_side import CoralFiveASide as FiveASide
    from voltron.environments.constants.bma.promotions import CoralPromotions as Promotions
    from voltron.environments.constants.base.regex import Regex as RX
    from voltron.environments.constants.bma.bet_finder import CoralBetFinder as BetFinder

if tests.settings.brand == 'ladbrokes':

    from voltron.environments.constants.ladbrokes.bet_history import LadbrokesBetHistory as BetHistory
    from voltron.environments.constants.ladbrokes.bma import LadbrokesBMA as BMA
    from voltron.environments.constants.ladbrokes.ema import LadbrokesEMA as EMA
    from voltron.environments.constants.ladbrokes.gvc import LadbrokesGVC as GVC
    from voltron.environments.constants.ladbrokes.bet_finder import LadbrokesBetFinder as BetFinder
    from voltron.environments.constants.ladbrokes.betslip import LadbrokesBetslip as Betslip
    from voltron.environments.constants.ladbrokes.promotions import LadbrokesPromotions as Promotions
    from voltron.environments.constants.ladbrokes.quickbet import LadbrokesQuickbet as Quickbet
    from voltron.environments.constants.ladbrokes.racing import LadbrokesRacing as Racing
    from voltron.environments.constants.ladbrokes.retail import LadbrokesRetail as Retail
    from voltron.environments.constants.ladbrokes.sportsbook import LadbrokesSB as SB
    from voltron.environments.constants.ladbrokes.tote import LadbrokesTote as Tote
    from voltron.environments.constants.ladbrokes.uk_tote import LadbrokesUKTote as UKTote
    from voltron.environments.constants.ladbrokes.siteserve import LadbrokesSiteServe as SiteServe
    from voltron.environments.constants.ladbrokes.colors import LadbrokesColors as Colors
    from voltron.environments.constants.ladbrokes.coupons import LadbrokesCoupons as Coupons
    from voltron.environments.constants.ladbrokes.virtuals import LadbrokesVirtuals as Virtuals
    from voltron.environments.constants.ladbrokes.dialogs import LadbrokesDialogs as Dialogs
    from voltron.environments.constants.ladbrokes.inplay import LadbrokesInplay as Inplay
    from voltron.environments.constants.ladbrokes.yourcall import LadbrokesYourcall as Yourcall
    from voltron.environments.constants.ladbrokes.bet_finder import LadbrokesBetFinder as BetFinder
    from voltron.environments.constants.ladbrokes.regex import LadbrokesRegex as RX
    from voltron.environments.constants.ladbrokes.free_ride import FREERIDE
    from voltron.environments.constants.ladbrokes.one_two_free import OneTwoFree

if tests.settings.brand == 'ladbrokes':
    free_ride = FREERIDE
    fanzone = FANZONE
    onetwofree = OneTwoFree

account = Account
app = App
bet_finder = BetFinder
bet_history = BetHistory
betslip = Betslip
big_competitions = BigCompetitions
bma = BMA
bpp = BPP
coupons = Coupons
ema = EMA
favourites = Favourites
five_a_side = FiveASide
football = Football
inplay = Inplay
live_stream = LiveStream
lotto = Lotto
odds_boost = OddsBoost
olympics = Olympics
promotions = Promotions
question_engine = QuestionEngine
quickbet = Quickbet
quick_deposit = Quickdeposit
racing = Racing
retail = Retail
sb = SB
sb_desktop = SBDesktop
stats = Stats
tote = Tote
uk_tote = UKTote
virtuals = Virtuals
yourcall = Yourcall

siteserve = SiteServe
gvc = GVC
colors = Colors
regex = RX
dialogs = Dialogs
