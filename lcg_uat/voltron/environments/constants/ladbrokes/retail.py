from collections import namedtuple
from voltron.environments.constants.base.retail import Retail


class LadbrokesRetail(Retail):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/retail.lang.ts
    """
    TITLE = 'THE GRID'
    USE_THE_GRID_ONLINE_BUTTON = 'USE THE GRID ONLINE'
    ACTIVATE_CARD_BUTTON = 'ACTIVATE CARD'
    GENERATE_BUTTON = 'GENERATE'
    GENERATE_GRID_CARD = 'Generate Grid Card'
    MY_GRID_CARD = 'MY GRID CARD'
    FB_BET_FILTER_NAME = Retail.FB_BET_FILTER_NAME.title()
    IN_SHOP_COUPONS = Retail.IN_SHOP_COUPONS
    _bet_filter_your_betting = namedtuple('bet_filter_your_betting', ['bet_in_shop', 'bet_online'])
    _grid_items = namedtuple('grid_items', ['shop_bet_tracker', 'grid_exclusive_promos', 'football_bet_filter', 'in_shop_coupons', 'saved_bet_codes', 'shop_locator'])
    _bet_filter_tabs = namedtuple('_bet_filter_tab', ['create_coupon', 'your_teams', 'the_opposition', 'saved_filters'])

    EXPECTED_YOUR_BETTING = _bet_filter_your_betting(bet_in_shop='Bet In-Shop',
                                                     bet_online='Bet Online')
    EXPECTED_GRID_ITEMS = _grid_items(shop_bet_tracker='Shop Bet Tracker',
                                      grid_exclusive_promos='Grid Exclusive Promos',
                                      football_bet_filter='Football Bet Filter',
                                      in_shop_coupons='In-Shop Coupons',
                                      saved_bet_codes='Saved Bet Codes',
                                      shop_locator='Shop Locator')
    BET_FILTER_TABS = _bet_filter_tabs(create_coupon='CREATE COUPON',
                                       your_teams='YOUR TEAMS',
                                       the_opposition='THE OPPOSITION',
                                       saved_filters='SAVED FILTERS')
    SAVED_BET_CODES = 'Saved Bet Codes'
    FOOTER_TEXT_DIGITAL_COUPONS_PAGE = 'To place bet scan your code in-store, then track your bets using the bet tracker. Odds may change at time of bet placement'
    OPEN_IN_SHOP_NO_BETS_TEXT = 'You currently have no open in-shop bets.'
    SETTLED_IN_SHOP_NO_BETS_TEXT = 'You currently have no settled in-shop bets.'
    BET_IN_SHOP_TEXT = 'Build your coupon now and place your bet later in your Ladbrokes shop.'
    BET_ONLINE_TEXT = 'Build your coupon, add your selections to your betslip, place and track your bets, all online.'
