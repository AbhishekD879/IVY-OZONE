from collections import namedtuple


class Yourcall(object):
    """
    src/app/lazy-modules/locale/translations/en-US/yourCall.lang.ts
    """
    YOURCALL = 'YourCall'
    GO_TO_EVENT = 'Go to Event'

    YOURCALL_HASH = '#YourCall'
    YOURCALL_NO_MARKETS = 'is currently not available for this match'
    YOURCALL_STATIC_TEXT = 'There are currently no #yourcall selections available for this event. Please check here again soon.'

    _markets = namedtuple('markets', ['market_result', 'player_to_be_carded', 'anytime_goal_scorer', 'player_bets',
                                      'both_teams_to_score', 'over_under_goals', 'over_under_corners',
                                      'over_under_booking_points'])
    _markets_market_result = 'Match Result'
    _markets_player_to_be_carded = 'Player to be carded'
    _markets_anytime_goal_scorer = 'Anytime Goalscorer'
    _markets_player_bets = 'Player Bets'
    _markets_both_teams_to_score = 'Both Teams to Score'
    _markets_over_under_goals = 'Over/Under Goals'
    _markets_over_under_corners = 'Over/Under Corners'
    _markets_over_under_booking_points = 'Over/Under Booking Points'

    MARKETS = _markets(market_result=_markets_market_result,
                       player_to_be_carded=_markets_player_to_be_carded,
                       anytime_goal_scorer=_markets_anytime_goal_scorer,
                       player_bets=_markets_player_bets,
                       both_teams_to_score=_markets_both_teams_to_score,
                       over_under_goals=_markets_over_under_goals,
                       over_under_corners=_markets_over_under_corners,
                       over_under_booking_points=_markets_over_under_booking_points)

    SELECT_PLAYER = 'Select a Player'
    SELECT_PLAYER_PLACEHOLDER = 'Select Player'
    SELECT_STATISTIC = 'Select a Statistic'
    SELECT_STATISTIC_PLACEHOLDER = 'Select Stat'
    CHANGE_PLAYER = 'Change Player'
    CHANGE_STATISTIC = 'Change Statistic'
    DONE = 'Done'
    ADD_TO_BET = 'ADD TO BET'

    YES = 'Yes'
    NO = 'No'
    DRAW = 'Draw'
    UNDER = 'Under'
    OVER = 'Over'
    GOALS = 'Goals'
    CORNERS = 'Corners'
    BOOKING_PTS = 'Booking Pts'

    DASHBOARD_ALERT = 'Please add another selection to place a bet'
    DASHBOARD_TITLE = 'Build your bet'
    PLACE_BET = 'PLACE BET'
    OPEN = 'Open'
    CLOSE = 'Close'
    EDIT_SELECTION = 'Edit Selection'

    SELECTION_INVALID_ERROR = 'Please be aware that one or more of your selections have been suspended.'
    SELECTION_UNAVAILABLE_ERROR = 'Statistic currently unavailable for {playerName}.'
    ODDS_INVALID_ERROR = 'There has been a price change.'
    DASH = '-'

    VALIDATION_ERROR = 'There are selections that cannot be combined in the dashboard'
    YOUR_CALL_BETSLIP_TITLE = 'Betslip'
    FIVE_A_SIDE_BETSLIP_TITLE = '5-A-Side Betslip'
    FIVE_A_SIDE_BETRECEIPT_TITLE = '5-A-Side Bet Receipt'
    BACK = 'back'

    TO_HAVE = 'to have'
    TIMEOUT_ERROR = 'We have experienced some difficulties during bet placement, please check your <a class="deposit-external-link" href="/open-bets">open bets</a> to see if your bet was placed.'
    GENERAL_PLACE_BET_ERROR = 'There was a problem processing your bet, please try again soon'
    STAKE_VALUE_EXCEEDED = 'Sorry unable to place bet. The maximum stake for this bet is {currency}{stake}'
    STAKE_EXCEEDED = 'Sorry unable to place bet, maximum stake exceeded'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'
    PRICE_CHANGE_WARNING = 'Please beware that your selection had a price change.'
    FREE_BETS_AVAILABLE = 'Free Bets Available'
    PRICE_NOT_AVAILABLE = 'The price for this bet is not available, please try another combination'
    EVENT_STARTED_ERROR = 'Event has started, please see Main Markets tab for all available bets'

    WHOLE_MATCH = '90 mins'
    FIRST_HALF = '1st Half'
    SECOND_HALF = '2nd Half'

    TODAY = 'today'.upper()
    UPCOMING = 'upcoming'.upper()
    BUILD_YOUR_BET = 'Build Your Bet'
    PATH_BUILD_YOUR_BET = 'build-your-bet'
    LEAGUE_NO_EVENTS = 'There are currently no events available for this league'
    YOURCALL_TAB_DIALOG_DESC = 'By switching tabs you will be creating a new bet that is available for Cashout'
    OK = 'ok'
    YOURCALL_TAB_DIALOG_TITLE = 'New Build Your Bet with Cashout'
    NO_LEAGUES = 'Sorry no Build Your Bet events are available at this time'
    MARKET_NO_SELECTIONS = 'Sorry, This Market Has no Selection Available'
    FIVE_A_SIDE_TITLE = '5-A-SIDE'
    FIVE_A_SIDE_DEFAULT_ERROR = 'There are selections that cannot be combined in your team, ' \
                                'please edit your selections to proceed'
    FIVE_A_SIDE_DRAWER_TITLE = 'Ladbrokes 5-A-Side'
    SELECT_FORMATION = 'Select a formation and build your team'
