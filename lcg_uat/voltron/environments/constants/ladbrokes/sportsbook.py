from voltron.environments.constants.base.sportsbook import SB


class LadbrokesSB(SB):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/sb.lang.ts
    """
    FANZONE = 'Fanzone'
    TABS_NAME_COUPONS = 'ACCAS'
    TABS_NAME_FEATURED = 'Meetings'
    CHANGE_MARKET = 'Change Market'
    AZ_SPORTS = 'A-Z Betting'

    TABS_NAME_TODAY = SB.TABS_NAME_TODAY.upper()
    TABS_NAME_TOMORROW = SB.TABS_NAME_TOMORROW.upper()
    TABS_NAME_FUTURE = SB.TABS_NAME_FUTURE.upper()

    CHANGE_COMPETITION = SB.CHANGE_COMPETITION.upper()
    INSURANCE_MARKETS = SB.INSURANCE_MARKETS.upper()
    HOME = SB.HOME.upper()
    DRAW = SB.DRAW.upper()
    AWAY = SB.AWAY.upper()
    NO_GOAL = SB.NO_GOAL.upper()
    FIRST_GOALSCORER_SCORECAST = SB.FIRST_GOALSCORER_SCORECAST.upper()
    LAST_GOALSCORER_SCORECAST = SB.LAST_GOALSCORER_SCORECAST.upper()
    FAVOURITE_MATCHES = SB.FAVOURITE_MATCHES.upper()

    SPORT_DAY_TABS = SB._sport_tabs_keys(today='Today', tomorrow='Tomorrow', future='Future')

    EXPECTED_POPULAR_GOALSCORER_COLUMNS = ['PLAYERS', '1ST', 'ANYTIME', '2 OR MORE']
    EXPECTED_OTHER_GOALSCORER_COLUMNS = ['PLAYERS', 'LAST', 'HAT TRICK']
    EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS = ['TOTAL GOALS', 'OVER', 'UNDER']
    EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS_DESKTOP = ['Total Goals', 'OVER', 'UNDER']
    EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS = ["90 MINS", "1ST HALF", "2ND HALF"]
    ODDS_A_PLACES = 'Each Way: {num}/{den} odds - places {arr}'

    # Footer menu items
    HOME_FOOTER_ITEM = 'Home'
    MENU_FOOTER_ITEM = 'Menu'
    IN_PLAY_FOOTER_ITEM = 'In-Play'
    GAMING_FOOTER_ITEM = 'Gaming'
    CASINO_FOOTER_ITEM = 'Casino'
    MY_BETS_FOOTER_ITEM = 'My Bets'
    WATCH_LIVE_LABEL = 'Watch Live'

    MOBILE_FEATURED_MODULE_NAME = 'HIGHLIGHTS'
