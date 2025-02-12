from collections import namedtuple


class SB(object):
    """
    src/app/lazy-modules/locale/translations/en-US/sb.lang.ts
    """
    IN_PLAY = 'In-Play'
    LIVE_STREAM = 'Live Stream'
    AZ_COMPETITIONS = 'A-Z Competitions'
    LIVE_SIM = 'LIVESIM'
    ALL_SPORTS = 'All Sports'
    AZ_SPORTS = 'A-Z Sports'
    AZ_MENU = 'A-Z Menu'
    DELAY = '(Possible delay: 10 seconds)'
    LOGGED = 'You have been logged in:'
    TOP_GAMES = 'Top Games'
    TOP_SPORTS = 'Top Sports'
    PLAYERS = 'Players'
    FIRST = '1st'
    ANYTIME = 'Anytime'
    TWO_OR_MORE = '2 or More'
    LAST = 'Last'
    HATRICK = 'Hatrick'
    AZ = 'A-Z'
    BOLD = 'Bold:'
    PRICED = 'Priced'
    WAS_PRICE = 'Was'
    SHOW_ALL_LIVE_STREAMING_EVENTS = 'Show All Live Streaming Events'
    HIDE_ALL_LIVE_STREAMING_EVENTS = 'Show Less Live Streaming Events'
    GAMBLING = 'Safer Gambling'
    CONTACTS = 'Contact Us'
    LOBBY = 'Sports'
    OK = 'Ok'
    SELECT_YOUR_COUPON = 'Select your Coupon'
    CHANGE_COMPETITION = 'Change Competition'

    TABS_NAME_JACKPOT = 'Jackpot'
    FOOTBALL = 'Football'
    AMERICANFOOTBALL = 'American Football'
    BOXING = 'Boxing'
    GOLF = 'Golf'
    CRICKET = 'Cricket'
    HORSERACING = 'Horse Racing'
    GREYHOUND = 'Greyhounds'
    SNOOKER = 'Snooker'
    POOL = 'Pool'
    MOTORSPORTS = 'Motor Sports'
    MOTORBIKES = 'Motor Bikes'
    SPEEDWAY = 'Speedway'
    HURLING = 'Hurling'
    TENNIS = 'Tennis'
    DARTS = 'Darts'
    RUGBYUNION = 'Rugby Union'
    RUGBYLEAGUE = 'Rugby League'
    AUSSIERULES = 'Aussie Rules'
    BOWLS = 'Bowls'
    HOCKEY = 'Hockey'
    VOLLEYBALL = 'Volleyball'
    BEACHVOLLEYBALL = 'Beach Volleyball'
    BADMINTON = 'Badminton'
    BASKETBALL = 'Basketball'
    ICEHOCKEY = 'Ice Hockey'
    FORMULA_1 = 'Formula 1'
    BASEBALL = 'Baseball'
    TVSPECIALS = 'TV Specials'
    POLITICS = 'Politics'
    HANDBALL = 'Handball'
    UFCMMA = 'UFC/MMA'
    CYCLING = 'Cycling'
    MOVIES = 'Movies'
    GAELICFOOTBALL = 'Gaelic Football'
    ESPORTS = 'E-sports'

    TOMORROW = 'Tomorrow'
    TODAY = 'Today'
    YESTERDAY = 'Yesterday'
    MORE = 'More'
    CANCEL = 'Cancel'
    ACCEPT = 'Accept'
    DISTANCE = 'Distance:'
    WIN_OR_EACH_WAY = 'Win or E/W'
    BETTING_WITHOUT = 'Betting W/O'
    OTHER_MARKETS = 'More Markets'
    TO_FINISH_MARKETS = 'To Finish'
    TOP_FINISH_MARKETS = 'Top Finish'
    INSURANCE_MARKETS = 'Place Insurance'

    EXTRA_PLACE_TITLE = 'Extra Place Offer'

    BY_LEAGUES_COMPETITIONS = 'Leagues & Competitions'
    BY_LEAGUES_CUPS = 'By Leagues & Cups'
    BY_COMPETITIONS = 'By Competitions'
    BY_LATEST_RESULTS = 'By Latest Results'
    BY_MEETING = 'By Meeting'
    BY_MEETINGS = 'By Meetings'
    BY_TIME = 'By Time'
    NO_EVENTS_FOUND = 'No events found'
    NO_COUPONS_FOUND = 'No coupons found'
    NO_LIVE_EVENTS_FOUND = 'There are currently no Live events available'
    NO_UPCOMING_EVENTS_AVAILABLE = 'There are no upcoming events'
    STREAM_IS_NOT_AVAILABLE = 'The Stream for this event is currently not available.'
    NO_UPCOMING_EVENTS_FOUND = 'There are no upcoming events'
    STREAM = 'Stream'
    VIEW_FULL_RACE = 'View Full Race Card'
    PREVIOUS_RACES = 'Previous'
    NEXT_RACES = 'Next'
    PREVIOUS_CARD = 'Previous'
    NEXT_CARD = 'Next'
    VIEW_ALL = 'View All'
    SEE_ALL = 'See All'
    SEE_MORE = 'See More'
    SEE_LESS = 'See Less'
    EVENTS = 'Events'
    SHOW_ALL = 'Show All'
    TERMS = 'Terms'
    LIVE = 'Live'
    BY_LIVE_NOW = 'Live Now'
    BY_UPCOMING = 'Upcoming'
    BY_RACES = 'By Races'
    PLAYER = 'player'
    NUMBER = 'number'
    ODDS = 'odds'

    FORM = 'Form = '
    FORM_HEADER = 'Form'
    CARD = 'Card'
    JOCKEY_TRAINER = 'Jockey/Trainer'
    RP_RATING = 'R.P Rating'
    PREVIOUS_ODDS = 'Previous\nOdds'
    CURRENT_ODDS = 'Current\nOdds'
    DETAILS = 'Details'
    R_DETAILS = 'Runner Details'
    HORSE = 'Horse'
    DOG = 'Dog'
    JOCKEY = 'Jockey'
    TRAINER = 'Trainer'
    FORM_GUIDE = 'Form'
    AGE = 'Age'
    WEIGHT = 'Weight'
    STALL_NO = 'Stall No'
    RATING = 'Rating'
    RUNNER = 'Runner'
    SIRE = 'Sire'

    FLAG_UK = 'UK & IRE'
    FLAG_UK_LONG = 'UK / IRELAND RACES'
    FLAG_US = 'USA'
    FLAG_US_LONG = 'USA Races'
    FLAG_ZA = 'South Africa'
    FLAG_ZA_LONG = 'South Africa Races'
    FLAG_AE = 'UAE'
    FLAG_AE_LONG = 'UAE Races'
    FLAG_CL = 'Chile'
    FLAG_CL_LONG = 'Chile Races'
    FLAG_IN = 'India'
    FLAG_IN_LONG = 'India Races'
    FLAG_AU = 'Australia'
    FLAG_AU_LONG = 'Australia Races'
    FLAG_FR = 'France'
    FLAG_FR_LONG = 'France Races'
    FLAG_INT = 'Other International'
    FLAG_INT_LONG = 'International Races'
    FLAG_VR = 'Virtual'
    FLAG_V_RACES = 'Virtual Races'
    FLAG_ALL = 'All Races'
    FLAG_ENHRCS = 'Offers and Featured Races'

    TABS_NAME_FEATURED = 'Featured'
    TABS_NAME_ANTEPOST = 'Future'
    TABS_NAME_SPECIALS = 'Specials'
    TABS_NAME_YOURCALL = 'Yourcall'

    TABS_NAME_LIVE = 'Live'
    TABS_NAME_IN_PLAY = 'In-Play'
    TABS_NAME_TODAY = 'Today'
    TABS_NAME_TOMORROW = 'Tomorrow'
    TABS_NAME_FUTURE = 'Future'
    TABS_NAME_NEXT = 'Next Races'
    TABS_NAME_RESULTS = 'Results'
    TABS_NAME_COUPONS = 'Coupons'
    TABS_NAME_MATCHES = 'Matches'
    TABS_NAME_EVENTS = 'Events'
    TABS_NAME_FIGHTS = 'Fights'
    TABS_NAME_MATCHES_GOLF = '2/3 Balls'
    TABS_NAME_COMPETITIONS = 'Competitions'
    TABS_NAME_OUTRIGHTS = 'Outrights'
    TABS_NAME_SCORECAST = 'Scorecast'
    TABS_NAME_POPULAR_BETS = 'popularbets'
    TABS_MARKETS = 'Markets'
    TABS_NAME_MAIN_MARKETS = 'Main Markets'
    TABS_NAME_MAIN = 'Main'
    TABS_NAME_GOAL_MARKETS = 'Goal Markets'
    TABS_NAME_SCORE_MARKETS = 'Score Markets'
    TABS_NAME_HALF_MARKETS = 'Half Markets'
    TABS_NAME_HALF = 'Half'
    TABS_NAME_CORNER_MARKETS = 'Corner Markets'
    TABS_NAME_CARD_MARKETS = 'Card Markets'
    TABS_NAME_OTHER_MARKETS = 'Other Markets'
    TABS_NAME_ALL_MARKETS = 'All Markets'
    TABS_NAME_STANDINGS = 'Standings'
    LAST_GOAL_SCORECAST = 'Last Scorer'
    LAST_GOALSCORER_SCORECAST = 'Last Scorer'
    FIRST_GOAL_SCORECAST = 'First Scorer'
    FIRST_GOALSCORER_SCORECAST = 'First Scorer'
    POPULAR_GOALSCORER_MARKETS = 'Popular Goalscorer Markets'
    OTHER_GOALSCORER_MARKETS = 'Other Goalscorer Markets'
    FIRST_SECOND_HALF_RESULT = '1st Half / 2nd Half Result'
    FIRST_HALF_RESULT = '1st Half'
    SECOND_HALF_RESULT = '2nd Half'
    MINS_A = '15 Mins'
    MINS_B = '30 Mins'
    MINS_C = '60 Mins'
    MINS_D = '75 Mins'
    OVER_UNDER_TOTAL_GOALS = 'Over/Under Total Goals'
    HALF_TIME_FULL_TIME = 'Half Time/Full Time'
    DRAW_NO_BET = 'Draw No Bet'
    DOUBLE_CHANCE = 'Double Chance'
    VISUALISATION = 'Match Live'
    MATCHES = 'Matches'
    OUTRIGHTS = 'Outrights'
    RESULTS = 'Results'
    POPULAR_BETS = 'popularbets'

    DAY_SUNDAY = 'Sunday'
    DAY_MONDAY = 'Monday'
    DAY_TUESDAY = 'Tuesday'
    DAY_WEDNESDAY = 'Wednesday'
    DAY_THURSDAY = 'Thursday'
    DAY_FRIDAY = 'Friday'
    DAY_SATURDAY = 'Saturday'

    MONTH_JANUARY = 'January'
    MONTH_FEBRUARY = 'February'
    MONTH_MARCH = 'March'
    MONTH_APRIL = 'April'
    MONTH_MAY = 'May'
    MONTH_JUNE = 'June'
    MONTH_JULY = 'July'
    MONTH_AUGUST = 'August'
    MONTH_SEPTEMBER = 'September'
    MONTH_OCTOBER = 'October'
    MONTH_NOVEMBER = 'November'
    MONTH_DECEMBER = 'December'

    MON_JANUARY = 'Jan'
    MON_FEBRUARY = 'Feb'
    MON_MARCH = 'Mar'
    MON_APRIL = 'Apr'
    MON_MAY = 'May'
    MON_JUNE = 'Jun'
    MON_JULY = 'Jul'
    MON_AUGUST = 'Aug'
    MON_SEPTEMBER = 'Sep'
    MON_OCTOBER = 'Oct'
    MON_NOVEMBER = 'Nov'
    MON_DECEMBER = 'Dec'

    ADD_TO_BETSLIP = 'Add to Betslip'
    MY_BETS = 'My Bets'
    ODDS_A_PLACES = 'E/W {num}/{den} odds - places {arr}'
    NEW_ODDS_A_PLACES = 'E/W {num}/{den} Places {arr}'
    NEW_ODDS_A_PLACES_EXTENDED = 'E/W {num}/{den} odds - places {arr}'
    ODDS_A_PLACES_LABEL = 'odds - places'
    CLASS = 'Class {class}'

    EACH_WAY_TERMS_LABEL = 'Each Way:'
    PLACE_LABEL = 'Place'
    SILK_LABEL = 'Silk'
    TRAP_LABEL = 'Trap'
    RUNNERS_LABEL = 'Runners'
    GREYHOUNDS_LABEL = 'Greyhounds'
    PRICE_S_P_LABEL = 'Price(SP)'
    DIVIDEND_STRAIGHT = 'Straight forecast:'
    DIVIDEND_TRICAST = 'Tricast:'
    CONFIRM_CLEAR_OF_BET_SLIP = 'Confirm clear betslip'

    SS_DOWN = 'There was a problem retrieving the information requested'
    ERROR = 'Error'
    WARNING = 'Warning!'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'

    WATCH = 'Watch'
    WATCH_LIVE = 'Watch Live'
    WATCH_STOP = 'Stop'
    WATCH_FREE = 'WATCH FREE'
    VIDEO_STREAM = 'VIDEO STREAM'
    WATCH_FREE_INFORMATION = 'Find out more about Watch Free here'
    WATCH_FREE_INFORMATION_TITLE = 'EVERY RACE, EVERY ANGLE, EVERY DAY...'
    PRE_RACE = 'Pre-Race Sim'
    LOGIN_REQUIRED = 'In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours.'
    EVENT_IS_NOT_MAPPED = 'This event is not mapped and does not have video stream, contact support team.'
    SERVICES_CRASHED = 'The Stream for this event is currently not available.'
    EVENT_NOT_STARTED = 'This stream has not yet started. Please try again soon.'
    EVENT_FINISHED = 'This event is over.'
    ONLY_LOGIN_REQUIRED = 'In order to watch this stream, you must be logged in.'
    ONLY_FOR_MOBILE = 'This feature available only for mobile devices.'
    UNDER_CONSTRUCTION = 'This page is currently in preparation'
    NO_MARKETS_FOUND = 'No markets found'
    DENIED_BY_WATCH_RULES = 'In order to view this event you need to place a bet greater than or equal to £1'
    GEO_BLOCKED = 'You are blocked by geolocation. This live stream might not be supported in your current location. Please contact support team for further information.'
    USAGE_LIMITS_BREACHED = 'Your limit for streaming has been exceeded. Please try again later.'
    FAIR_USE_BREACH = 'Fair Use Breach.'
    HOW_TO_PLAY = 'Football Jackpot Operation'

    PROCEED_LUCKY_DIP = 'Proceed to replace your selections with Lucky Dip selections?'

    HOME = 'Home'
    DRAW = 'Draw'
    AWAY = 'Away'
    NO_GOAL = 'No Goal'
    TENNIS_SET = 'Set'

    NUM_SUFFIX_TH = 'th'
    NUM_SUFFIX_ST = 'st'
    NUM_SUFFIX_ND = 'nd'
    NUM_SUFFIX_RD = 'rd'

    PROMOTIONS = 'Promotions'
    MORE_INFORMATION = 'More information'
    MORE_INFO = 'More info'
    NO_PROMOTIONS_FOUND = 'No active Promotions at the moment'
    TERMS_AND_CONDITIONS_LABEL = 'Terms and Conditions'
    CASHOUT = 'cash out'
    SMALL_HOME = 'H'
    SMALL_AWAY = 'A'
    SMALL_DRAW = 'D'
    SUMMARY = 'Summary'
    SHOW_FORM = 'Show Summary'
    HIDE_FORM = 'Hide Summary'
    NO_SUMMARY = 'Currently there is no Summary available.'
    NO_DETAILS = 'Currently there are no Details available.'

    HANDICAP_RESULTS = 'Handicap Results'
    MATCH_RESULT = '90 mins'
    FIRST_HALF = '1st Half'
    SECOND_HALF = '2nd Half'
    BOTH_HALVES = 'Both Halves'
    TOTAL_GOALS = 'Total Goals'
    TOTAL = 'Total'
    OVER = 'Over'
    UNDER = 'Under'
    SHOW_LESS = 'Show Less'
    OVER_UNDER_GOALS = 'Over/Under goals'
    YES = 'Yes'
    NO = 'No'
    YOUR_ENHANCE_MARKETS = 'Your Enhanced Markets'
    PRIVATE_MARKETS_TERMS_AND_CONDITIONS = 'Private Markets Terms and Conditions'
    CURRENT_MATCHES = 'Current Matches'
    FAVOURITE_MATCHES = 'Favourite Matches'
    ADD_FAVOURITE_MATCH = 'Add Favourite Match'
    NO_MARKETS_AVAILABLE = 'No markets are currently available for this event'
    NO_CASH_OUT_AVAILABLE = 'Cash Out is not available for this event'
    FAVOURITES = 'Favourites'

    CORAL_INTRODUCES_NEW = 'Coral introduces new'
    FEATURE_ALLOWING_YOU_TO = 'feature allowing you to'
    EASILY_ACCESS_AND_FOLLOW_SEVERAL = 'easily access and follow several'
    MATCHES_OF_YOUR_CHOICE = 'matches of your choice'
    PRESSING_THE_STAR_WILL_ADD_THIS = 'Pressing the star will add this'
    MATCH_TO_YOUR = 'match to your'
    HERE_YOU_CAN_QUICKLY_AND_EASILY = 'Here you can quickly and easily'
    ACCESS_YOUR_FAVOURITED_MATCHES = 'access your favourited matches'
    TRY_IT_NOW = 'Try it now!'
    CLOSE_TUTORIAL = 'Close tutorial'
    SHOW_MORE = 'Show More'
    SEE_MORE_DATES = 'See More Dates'
    SHOW_LESS_SLN = 'SHOW LESS SELECTIONS'
    SHOW_MORE_SLN = 'SHOW ALL SELECTIONS'

    NO_RESULTS_AVAILABLE = 'No Results Available'

    _scorecast = namedtuple('scorecast', ['select_goalscorer', 'select_result'])
    _scorecast_select_goalscorer = 'Select Goalscorer'
    _scorecast_select_result = 'Select Result'
    SCORECAST = _scorecast(select_goalscorer=_scorecast_select_goalscorer,
                           select_result=_scorecast_select_result)

    FOOTBALL_JACKPOT_RECEIPT = 'Football Jackpot Bet Receipt'
    JACKPOT_LINES = 'Lines'
    FOOTBALL_JACKPOT = 'Football Jackpot '
    BET_RECEIPT_NO = 'Bet Receipt No: '
    TOTAL_STAKE = 'Total Stake: '
    BET_LINES = 'Number of Lines: '
    GAME = 'Game'
    JACKPOT_SELECTION = 'Selection'
    DONE = 'Done'
    PRE_PARADE = 'Pre-Parade'

    FREE_BETS_AVAILABLE = 'Free Bets Available'
    BET_REJECTED_ERROR = 'Pool bet has been rejected by system.'
    INSUFFICIENT_FOUNDS_ERROR = 'Bet is not placed due to insufficient funds. Please make a '
    DEPOSIT_SMALL = 'deposit.'
    GO_TO_EVENT = 'Go to event'
    LIVE_COMMENTARY = 'Live Commentary'

    _sport_tabs_keys = namedtuple('SPORT_DAY_TABS', ['today', 'tomorrow', 'future'])
    SPORT_DAY_TABS = _sport_tabs_keys(today='TODAY', tomorrow='TOMORROW', future='FUTURE')

    _handicap_switchers = namedtuple('HANDICAP_SWITCHERS', ('ninety_mins', 'first_half', 'second_half'))
    HANDICAP_SWITCHERS = _handicap_switchers(ninety_mins='90 MINS', first_half='1ST HALF', second_half='2ND HALF')

    EXPECTED_POPULAR_GOALSCORER_COLUMNS = ['Players', '1ST', 'ANYTIME', '2 OR MORE']
    EXPECTED_OTHER_GOALSCORER_COLUMNS = ['Players', 'LAST', 'HAT TRICK']
    EXPECTED_OVER_UNDER_TOTAL_GOALS_COLUMNS = ['Total Goals', 'OVER', 'UNDER']
    EXPECTED_OVER_UNDER_TOTAL_GOALS_BUTTONS = ["90 MINS", "1ST HALF", "2ND HALF"]

    _fixture_header = namedtuple('odds_format', ['under', 'over', 'home', 'draw', 'away', 'yes', 'no'])
    FIXTURE_HEADER = _fixture_header(under='UNDER', over='OVER', home='HOME', draw='DRAW', away='AWAY', yes='YES', no='NO')

    # Competitions details page
    _competition_details_page_tabs = namedtuple('comp_tabs', ['matches', 'outrights', 'results', 'standings'])
    COMPETITION_DETAILS_PAGE_TABS = _competition_details_page_tabs(matches='MATCHES', outrights='OUTRIGHTS',
                                                                   results='RESULTS', standings='STANDINGS')

    __SPORT_TABS_INTERNAL_NAMES = namedtuple('sport_tabs_internal_ids', ('matches',
                                                                         'competitions',
                                                                         'coupons',
                                                                         'outrights',
                                                                         'accumulators',
                                                                         'in_play',
                                                                         'jackpot',
                                                                         'specials'))

    SPORT_TABS_INTERNAL_NAMES = __SPORT_TABS_INTERNAL_NAMES(matches='matches',
                                                            competitions='competitions',
                                                            coupons='coupons',
                                                            outrights='outrights',
                                                            accumulators='accumulators',
                                                            in_play='live',
                                                            jackpot='jackpot',
                                                            specials='specials')

    # Footer menu items
    HOME_FOOTER_ITEM = 'HOME'
    IN_PLAY_FOOTER_ITEM = 'IN-PLAY'
    GAMING_FOOTER_ITEM = 'GAMING'
    GAMING_HEADER_ITEM = 'CASINO'
    CASINO_FOOTER_ITEM = 'CASINO'
    ALL_SPORTS_FOOTER_ITEM = 'ALL SPORTS'
    MY_BETS_FOOTER_ITEM = 'MY BETS'

    EXPECTED_PLEASE_LOGIN_TO_VIEW_FAVOURITES = 'To view and add matches into your favourites, please log in to your account.'
    WATCH_LIVE_LABEL = 'WATCH LIVE'

    # Some widgets names
    LEAGUE_TABLE_LABEL = 'LEAGUE TABLE'

    # Domain URLs
    CORAL_TST_ENV_DOMAIN_URL = 'ss-tst2.coral.co.uk'
    LADS_TST_ENV_DOMAIN_URL = 'tst2-backoffice-lcm.ladbrokes.com'
    CORAL_PROD_ENV_DOMAIN_URL = 'ss-aka-ori.coral.co.uk'
    LADS_PROD_ENV_DOMAIN_URL = 'ss-aka-ori.ladbrokes.com'

    OOPS_ERROR_MESSAGE = 'Oops! We are having trouble loading this page. Please check your connection'

    # home page tabs
    HOME_FEATURED_NAME = 'FEATURED'

    # My Stable Constants
    VIEW_NOTES = 'VIEW NOTES'
    HIDE_NOTES = 'HIDE NOTES'
    ADD_NOTES = 'ADD NOTES'
    RECENTLY_ADDED = 'Recently Added'  # My Stable Dropdown Option
