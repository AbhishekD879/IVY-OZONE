from collections import namedtuple


class Tote(object):
    """
    src/app/lazy-modules/locale/translations/en-US/tt.lang.ts
    """
    TOTE_TITLE = 'International Tote'
    TOTE_INFO_TITLE = 'International Tote Information'
    TOTEPOOL = 'Totepool'
    RESULTS = 'Results'
    BY_TIME = 'By Time'
    BY_MEETING = 'By Meeting'
    EVENTS = 'Events'
    TOTE_EVENTS = 'Tote Events'
    BOLD = 'Bold'
    PRICED = 'Priced'
    TOMORROW = 'Tomorrow'
    TODAY = 'Today'
    MORE = 'More'
    CANCEL = 'Cancel'
    ACCEPT = 'Accept'
    DISTANCE = 'Distance:'
    WIN_OR_EACH_WAY = 'Win or E/W'
    BETTING_WITHOUT = 'Betting W/O'
    OTHER_MARKETS = 'More Markets'
    VIEW_ALL_RACING = 'View all racing'
    WATCH_LIVE = 'Watch Live'
    RACE_SUMMARY = 'Race Summary'
    SHOW_MORE = 'Show More'
    POOL_GUIDE_LEGEND = '(Pool guide displayed could change before the race starts &amp; should be used as a guide only)'
    PRICE_POOL = 'Prize pool'
    GUIDE = 'Guide'
    CONVERTED_VALUE = 'Est.'

    TABS_NAME_HORSE_RACING = 'Horse Racing'
    TABS_NAME_RESULTS = 'Results'
    BY_LATEST_RESULTS = 'By Latest Results'
    BY_MEETINGS = 'By meetings'

    EX = 'Exacta'
    P6 = 'Jackpot'
    PL = 'Place'
    TR = 'Trifecta'
    DB = 'Double'
    P3 = 'Pick 3'
    P4 = 'Pick 4'
    P5 = 'Pick 5'
    P9 = 'Pick 9'
    P1_0 = 'Pick 10'
    SU = 'Superfecta'
    QU = 'Quinella'
    WN = 'Win'
    SH = 'Show'
    OM = 'Swinger'

    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'

    ERROR = 'Error'
    ERROR_TITLE_503 = '503 Error - Services Unavailable'
    ERROR_MESSAGE_503 = 'Please contact your support team for assistance'

    BET_NOW = 'Bet Now'
    TOTAL_STAKE = 'Total Stake:'
    CLEAR_BET_SLIP = 'Clear Betslip'

    STAKE_TITLE = 'Stake'
    TOTAL_STAKE_TITLE = 'Total Stake'
    LEG_TITLE = 'Leg:'
    BET_ID_TITLE = 'Bet ID:'
    BET_RECEIPT_TITLE = 'Bet Receipt'
    SUCCESS_BET_RECEIPT_MSG = 'Your bet has been placed'
    SUCCESS_BETS_RECEIPT_MSG = 'All your bets have been placed'
    UNSUCCESSFUL_BET_RECEIPT_MSG = '%1 out of %2 bets have been placed'
    UNSUCCESSFUL_BET_RECEIPT_ADV = 'Please review racecard for details'

    BETTING_RULES_MSG = 'All bets are accepted with the <a href="https://coral-eng.custhelp.com/app/answers/detail/a_id/2141">Coral Betting Rules</a> as published on this site.'
    CONTINUE = 'CONTINUE'

    VIDEO_STREAM = 'VIDEO STREAM'
    ONLY_LOGIN_REQUIRED = 'In order to watch this stream, you must be logged in.'
    DENIED_BY_WATCH_RULES = 'In order to view this event you need to place a bet greater than or equal to £1'
    STREAM_IS_NOT_AVAILABLE = 'The Stream for this event is currently not available.'
    EVENT_NOT_STARTED = 'This stream has not yet started. Please try again soon.'
    EVENT_FINISHED = 'This event is over.'
    UNAVAILABLE_POOLS = 'Pools for this event are currently unavailable'
    TOTE_SUSPENSION_ERROR = 'Please beware some of your selections have been suspended'

    MIN_STAKE_PER_LINE = 'Stake must be greater than {value}'
    MAX_STAKE_PER_LINE = 'Stake must be lower than {value}'
    MIN_TOTAL_STAKE = 'Total stake must be greater than {value}'
    MAX_TOTAL_STAKE = 'Total stake must be lower than {value}'
    STAKE_INCREMENT_FACTOR = 'Stake must be in increments of {value}'

    _tote_tabs = namedtuple('tote_tabs', ('win', 'place', 'exacta', 'trifecta', 'quadpot', 'placepot', 'jackpot'))
    TOTE_TABS = _tote_tabs(win='WIN', place='PLACE', exacta='EXACTA', trifecta='TRIFECTA', quadpot='QUADPOT',
                           placepot='PLACEPOT', jackpot='JACKPOT')
