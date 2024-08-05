from collections import namedtuple


class Betslip(object):
    """
    src/app/lazy-modules/locale/translations/en-US/bs.lang.ts
    """
    ACCA_INSURANCE = 'Acca Insurance'
    ACCA_SUGGESTED_OFFER_FOR_5_PLUS = 'ACCA INSURANCE: GET IN! Place this Acca to earn a FREE BET (up to £25.00) if ONE selection lets you down. Min stake £2'
    BACK = 'Back'
    CLOSE = 'Close'
    OK = 'OK'
    YOUR_BETS = 'Your Bets'
    SUCCESS_BET = 'Bet Placed Successfully'
    VIEW_ENTRY_TITLE = 'Your team has been entered into a 5-A-Side Leaderboard!'
    NOTICE = 'Notice'
    BETSLIP_BTN = 'Betslip'
    FAVOURITES = 'Favourites'
    BET_NOW = 'Place Bet'.upper()
    BET_NOW_LOG_IN = 'Login & Place Bet'
    ACCEPT_BET = 'ACCEPT & PLACE BET'
    ACCEPT_PLACE_BET_DEPOSIT = 'ACCEPT (DEPOSIT & PLACE BET)'
    PLAYER_BETS_NOW = ' Player Bets Bet Now'
    SINGLES = 'Singles'
    SINGLE = 'Single'
    MULTIPLES = 'Multiples'
    ACCA = 'Place your ACCA'
    MIN_STAKE = 'Minimum stake is £ {0:.2f}'
    MAX_STAKE = 'Maximum stake is £ {0:.2f}'
    INVALID_VALUE = 'Invalid value'
    ODDS = 'Odds:'
    ODDS_A_PLACE = 'odds a place'
    STAKE = 'Stake:'
    ODDS_A_PLACES = 'Each Way Odds {num}/{den} Places {arr}'
    LINES_PER_STAKE = '{lines} Lines at {currency}{stake} per line'
    LINE_PER_STAKE = '{lines} Line at {currency}{stake} per line'
    UNIT_STAKE = 'Unit Stake'
    STAKE_USED = 'Stake Used'
    QUICK_STAKE = 'Quick Stake:'
    ESTIMATED_RESULTS = 'Est. Returns:'
    NO_SELECTIONS = 'You have no selections in the slip.'
    NO_SELECTIONS_TITLE = 'Your betslip is empty'
    NO_SELECTIONS_MSG = 'Please add one or more selections to place a bet'
    START_BETTING = 'Go betting'
    CLEAR_BETSLIP_TITLE = 'Remove All?'
    CLEAR_BETSLIP_CANCEL = 'Cancel'
    CLEAR_BETSLIP_CONTINUE = 'Continue'
    TOTAL_EST_RETURNS = 'Estimated Returns'
    RETURNS = 'Total Returns: '
    RETURN = 'Winnings: '
    CASH_OUT_AMOUNT = 'Cash Out Amount'
    REMAINING_STAKE = 'Remaining Stake: '
    TOTAL_CASH_OUT = 'Total Cashed Out: '
    TOTAL_CASH_OUT_STAKE = 'Total Cashed Out Stake: '
    DATA_TIME = 'Date/Time'
    SP = 'SP'
    R_DETAILS = 'Runner Details'
    SELECTION_INFORMATION = 'Selection Information'
    SPORT = 'Sport'
    EVENT = 'Event'
    MARKET = 'Market:'
    TIME = 'Time'
    ALL_SINGLE_STAKES = 'All Single Stakes'

    _tote_bet_errors = namedtuple('tote_bet_errors', ['meeting_cancelled', 'sales_not_opened', 'pool_canceled', 'race_cancelled',
                                                      'race_void', 'race_off', 'race_closed', 'unit_stake', 'non_runner',
                                                      'default', 'stake_increment', 'credit', 'large_stake', 'small_stake'])
    _tote_bet_errors_meeting_cancelled = 'Sorry the event has been suspended'
    _tote_bet_errors_sales_not_opened = 'Sorry the event has been suspended'
    _tote_bet_errors_pool_canceled = 'Sorry the event has been suspended'
    _tote_bet_errors_race_cancelled = 'Unfortunately the race has been suspended'
    _tote_bet_errors_race_void = 'Unfortunately the race has been suspended'
    _tote_bet_errors_race_off = 'Unfortunately the race has been suspended'
    _tote_bet_errors_race_closed = 'Unfortunately the race has been suspended'
    _tote_bet_errors_unit_stake = 'Invalid unit stake, please amend'
    _tote_bet_errors_non_runner = 'Chosen selection is now a Non-Runner'
    _tote_bet_errors_default = 'Bet was not successful'
    _tote_bet_errors_stake_increment = 'Stake must be in increments of %1'
    _tote_bet_errors_credit = 'Please Deposit additional funds to place the bet'
    _tote_bet_errors_large_stake = 'Stake too high. The maximum stake per line is {currency}{stake_per_line}. The maximum stake per bet is {currency}{stake_per_bet}'
    _tote_bet_errors_small_stake = 'Stake too small. The minimum stake per line is {currency}{stake_per_line}. The minimum stake per bet is {currency}{stake_per_bet}'
    TOTE_BET_ERRORS = _tote_bet_errors(meeting_cancelled=_tote_bet_errors_meeting_cancelled,
                                       sales_not_opened=_tote_bet_errors_sales_not_opened,
                                       pool_canceled=_tote_bet_errors_pool_canceled,
                                       race_cancelled=_tote_bet_errors_race_cancelled,
                                       race_void=_tote_bet_errors_race_void,
                                       race_off=_tote_bet_errors_race_off,
                                       race_closed=_tote_bet_errors_race_closed,
                                       unit_stake=_tote_bet_errors_unit_stake,
                                       non_runner=_tote_bet_errors_non_runner,
                                       default=_tote_bet_errors_default,
                                       stake_increment=_tote_bet_errors_stake_increment,
                                       credit=_tote_bet_errors_credit,
                                       large_stake=_tote_bet_errors_large_stake,
                                       small_stake=_tote_bet_errors_small_stake)

    FULL_BET_SLIP = 'Betslip Full'
    MAX_SELECTION_MESSAGE = 'Maximum number of selections allowed on betslip is {max_number}'
    BETSLIP_LIMITATION_MESSAGE = 'You already have one or more selections in the betslip that can\'t be combined, please remove those selections to add any new selection'
    DEPOSIT = 'Deposit'
    BALANCE = 'Balance'
    SHOW_BALANCE = 'Show Balance'
    HIDE_BALANCE = 'Hide Balance'
    VOUCHER_FORM = 'Redeem Voucher'
    CASH_HISTORY = 'Partial Cash Out History'
    SHOW_CASH_HISTORY = 'Show Partial Cash Out History'
    HIDE_CASH_HISTORY = 'Hide Partial Cash Out History'
    ADD_ALL_TO_FAVOURITES = 'Favourite all'
    CLOSE_BUTTON = 'Close'
    GO_TO_FAVOURITES = 'Go to Favourites'
    USER_BALANCE = 'Your Balance is:'
    QUICK_DEPOSIT_BTN = 'Quick Deposit'
    NO_LOGIN_USER_BALANCE = 'Please log in to see your balance'
    STAKE_PRICE_CHANGE_MSG = 'Price Change from {old} to {new}'
    PRICE_CHANGE_BANNER_MSG = 'Some of your prices have changed!'
    REBOOST_PRICE_CHANGE_BANNER_MSG = 'The price has changed and new boosted odds will be applied to your bet.' \
                                      ' Hit Re-Boost to see your new boosted prices'

    COUNT_DOWN_TIMER_MESSAGE = 'Please wait while your bet is being placed'
    BETTING_DISABLED = 'Betting is disabled on this account.'
    PLACE_BET_ALERT_MESSAGE = 'Please Enter Stake For At Least One Bet.'
    SINGLE_DISABLED = 'Please beware one of your selections has been suspended'
    MULTIPLE_DISABLED = 'Please beware some of your selections have been suspended'
    BELOW_MULTIPLE_DISABLED = 'Some of your selections have been suspended'
    SELECTION_SUSPENDED = 'Sorry, the event has been suspended'
    EVENT_SUSPENDED = 'Sorry, the event has been suspended'
    EVENT_STARTED = 'Event has already started!'
    MARKET_SUSPENDED = 'Sorry, the market has been suspended'
    OUTCOME_SUSPENDED = 'Sorry, the outcome has been suspended'
    PRICE_CHANGED = 'Price Changed From %1 To %2.'
    HANDICAP_CHANGED = 'Handicap changed from %1 To %2'
    INTERNAL_ERROR = 'Internal error.'
    INVALID_BET_DOCUMENT_ID = 'Invalid bet document ID.'
    LIVE_PRICE_UNAVAILABLE = 'Live price is unavailable.'
    INSUFFICIENT_FUNDS = 'Insufficient funds to place the bet.'
    ODDS_BOOST_NOT_ALLOWED = 'Sorry, one of the selections cannot be boosted, please remove the selection and try again.'
    OTHER_BETS_FAILED = 'Error with bet in request.'
    STAKE_MISMATCH = 'Stake mismatch.'
    STAKE_TOO_LOW = 'Stake is too low'
    SELECTION_REMOVED = 'Selection %1 is no longer available'
    PLACE_INVALID_ACCESS_TOKEN = 'This Offer Applies To One Selection Only, Please Check & Try Again.'
    PLACE_INVALID_TOKEN = 'This Offer Applies To One Selection Only, Please Check & Try Again.'
    DUPLICATED_BET = 'Server is unavailable at the moment, please try again later.'
    INVALID_BET_TYPE = 'Invalid bet type'
    INVALID_BET_INDETERMINATE_LEGREF = 'The bet contains reference to non existent leg.'
    INVALID_BET_WRONG_NO_OF_LEGREF = 'The bet contains wrong number of legRefs'
    INVALID_BET_DUPLICATE_EXTERNALREF = 'The bet contains externalRefs that are not unique.'
    INVALID_BET_LEGREF_MISSING_ORDERING = 'The bet contains leg references that have no ordering'
    INVALID_BET_LEGREF_ORDERING_NOT_UNIQUE = 'The bet contains leg references that have duplicate ordering in the bet.'
    INVALID_PART_RESULTING_RULE = 'Invalid part resulting rule'
    INVALID_BET_REF_DOCUMENT_ID = 'The request contains invalid bet references'
    INVALID_BET_REF_ID = 'The request contains invalid bet reference ids'
    INVALID_LEG_DOCUMENT_ID = 'The request contains invalid bet document ids'
    INVALID_LEG_REF_DOCUMENT_ID = 'The request contains invalid legRef document id'
    INVALID_PART_PLACES = 'The request contains invalid part places.'
    INVALID_NUMBER_OF_PARTS = 'The request contains invalid number of parts.'
    INVALID_POOL_BET_MULTI_LEGS_SAME_POOL = 'The request contains multiple legs referencing the same pool.'
    INVALID_BET_MIXED_LEGS_NOT_ALLOWED = 'The request contains a bet with legs belonging to different flavors'
    INVALID_BET_MISSING_LEG_REFS = 'The request contains bet with missing legRefs'
    INVALID_BET_MISSING_STAKE_AMOUNT = 'The request contains bet with missing stake amount'
    INVALID_BET_MISSING_STAKE_PER_LINE = 'The request contains bet with missing stake per line'
    INVALID_BET_INDETERMINATE_BETSLIPREF = 'The request contains bet with indeterminate betslip reference'
    INVALID_BETSLIP_MISSING_CUSTOMER_REF = 'The request contains empty or missing customer references'
    INVALID_BETSLIP_INDETERMINATE_BETREF = 'The request contains indeterminate betRefs'
    INVALID_BETSLIP_INCOMPATIBLE_BET_TYPES = 'The request contains incompatible bet types in the betslip'
    INVALID_NUMBER_OF_LINES = 'The request contains missing or incorrect number of lines for a bet'
    PLACE_INVALID_STAKE = 'The request contains bet with invalid or incorrect stake'
    SAME_SELECTION = 'The request contains leg with references to same outcome'
    DUPLICATE_LEG_REF_DOCUMENT_ID = 'The bet contains duplicate legRef elements in a bet'
    INVALID_POOL_TYPE = 'The request contains bet with invalid pool type'
    INVALID_PRICETYPE_REF = 'The request contains bet with invalid priceTypeRef'
    UNSUPPORTED_PROVIDER = 'The request contains betRefs with unsupported providers'
    INVALID_OUTCOME_COMBI_REF = 'The request contains legs with invalid outcomeCombiRefs'
    INVALID_WIN_PLACE_REF = 'The request contains legs with invalid winPlaceRef'
    INVALID_STAKE = 'The request contains invalid stake'
    BAD_LOTTERY_PICKS = 'The request contains invalid lottery picks'
    MULTIPLE_CURRENCIES_ON_SLIP = 'The request contains multiple currencies on the betslip'
    BAD_LOTTERY_SUBSCRIPTION = 'The request contains an invalid lottery subscription'
    INVALID_NUMBER_OF_LOTTERY_PICKS = 'The request contains invalid number of lottery picks'
    INVALID_COUPON_COMBINATION = 'The request contains invalid coupon combination'
    INVALID_COUPON = 'The request contains invalid coupon'
    INVALID_COUPON_TYPE = 'The request contains invalid coupon type'
    INVALID_OUTCOME_REF = 'The request contains invalid outcomeRef'
    BLOCKBUSTER_EMPTY_GROUP = 'The request contains blockbuster coupons without at least one bet per group'
    BLOCKBUSTER_INCONSISTENT_SELNS_PER_GROUP = 'The request contains blockbuster coupons without same number bets per group'
    INVALID_LEGGROUP_LEGREF_MISSING_ORDERING = 'The request contains legRefs missing ordering'
    INVALID_LEGGROUP_LEGREF_ORDERING_NOT_UNIQUE = 'The request contains legRefs that have duplicate ordering in the bet'
    INVALID_LEGGROUP_INDETERMINATE_LEGREF = 'The request contains legRefs referencing a non existent leg'
    INVALID_PRICE_WRONG_ELEMENTS_NUMBER = 'The bet contains legs with wrong number of price elements'
    INVALID_PRICE_LEGTYPE = 'The bet contains invalid price legtype'
    INVALID_PRICE_VALUE = 'The bet contains invalid price value'
    INVALID_PLACE_TERMS = 'The bet contains invalid place terms'
    EACHWAY_BETS_UNAVAILABLE = 'The request contains bets for which each way is not available'
    PLACE_BETS_UNAVAILABLE = 'The request contains bets for which place is not available'
    WIN_PLACE_BETS_UNAVAILABLE = 'The request contains bets for which winplace is not available'
    BEST_PRICE_UNAVAILABLE = 'The request contains bets for which best price is not available'
    FORECASTS_UNAVAILABLE = 'The request contains bets for which forecast is not available'
    TRICASTS_UNAVAILABLE = 'The request contains bets for which tricast is not available'
    FIRST_SHOW_UNAVAILABLE = 'The request contains bets for which first show is not available.'
    SECOND_SHOW_UNAVAILABLE = 'The request contains bets for which second show is not available.'
    STARTING_PRICE_UNAVAILABLE = 'The request contains bets for which starting price is not available'
    NEXT_PRICE_UNAVAILABLE = 'The request contains bets for which next price is not available'
    SCORECAST_UNAVAILABLE = 'The request contains bets for which scorecast is not specified'
    NO_MARKET_HANDICAP = 'The request contains bets for which handicap market is not available'
    NO_LEG_SORT = 'The request contains bets for which leg sort is not provided'
    NO_LEG_TYPE = 'The request contains bets for which leg type is not provided'
    BIR_INDEX_CHANGED = 'The request contains bets for which BIR index has changed'
    POOL_SUSPENDED = 'The request contains bets for which pool is suspended for a selection'
    GAME_SUSPENDED = 'The request contains bets for which lottery is suspended'
    GAME_INACTIVE = 'The request contains bets for which lottery is inactive'
    MARKET_VALUE_CHANGED = 'Market value changed.'
    EACHWAY_TERMS_CHANGE = 'Eachway terms change'
    EACHWAY_PRICE_CHANGE = 'The request contains bets for which each way price has changed'
    EACHWAY_PLACES_CHANGE = 'The request contains bets for which each way places have changed'
    WIN_PLACE_TERMS_CHANGED = 'Win place terms changed'
    EACH_WAY_TERMS_CHANGED = 'Eachway terms change'
    BLOCKBUSTER_BONUS_AMOUNT_CHANGED = 'The request contains blockbuster coupons for which bonus amount has changed'
    GUEST_CANNOT_PLACE_BETS = 'Guest can not place bets'
    CUSTOMER_INACTIVE = 'Customer inactive'
    CUSTOMER_IN_PROBATION = 'The request contains bet for a customer with pending registration'
    ACCOUNT_NOT_FOUND = 'The request contains bet for a non existing customer'
    ACCOUNT_NOT_ACTIVE = 'The request contains bet for a customer inactive account'
    MUST_CHANGE_PASSWORD = 'Is required to change the password'
    CUSTOMER_BLOCKED_FOR_CHANNEL = 'The request contains bet for a customer who is blocked on a channel'
    ACCOUNT_CLOSED = 'The request contains bet for a customer with closed account'
    ACCOUNT_BETTING_DISABLED = 'The request contains bet for a customer who is not allowed to bet'
    ACCOUNT_SUSPENDED = 'Your account is suspended'
    STAKE_TOO_HIGH = 'The stake specified in the bet is too high'
    STAKE_HIGH = 'The stake is too high for one of your selections'
    BAD_LEG_SORT = 'One of the request elements used to determine the leg sort is invalid'
    PLACE_INVALID_STAKE_NOT_MULTIPLE = 'The stake provided is not a multiple of the configured base value'
    PLACE_INVALID_STAKE_NOT_WHOLE_INT = 'The stake provided is required to be an integer value'
    PLACE_INVALID_STAKE_MAX_NUM_LINES = 'The stake provided is required to be an integer value'
    PLACE_INVALID_STAKE_SYSTEM_BET = 'The stake provided is invalid for the given system bet'
    PLACE_INVALID_STAKE_SINGLE_SYSTEM = 'The stake provided is invalid for the given system bet'
    INVALID_MARKET = 'The market provided is invalid or does not exist'
    INVALID_OUTCOME = 'The outcome provided is invalid or does not exist'
    INVALID_LEG_TYPE = 'The leg type value mapped from the request is invalid'
    INVALID_SCORECAST = 'The scorecast bet in the request is invalid'
    NO_SUCH_OUTCOME = 'The outcome does not exist'
    INVALID_CALL_ID = 'The Call was not provided or is invalid'
    DUPLICATE_BET = 'The bet being placed has been detected as a duplicate'
    ODDS_PRODUCT_LIMIT_EXCEEDED = 'The current odds exceed the system permissible limit'
    COMBINATION_LIMIT_EXCEEDED = 'The current bet combination exceeds the system permissible limit'
    MISSING_CALL_ID = 'The call ID is missing in the request'
    CANCEL_FAILED = 'The attempt to cancel the given bet has failed'
    REGION_INACTIVE = 'The region of origin is not active for placing bets'
    BIR_UNAVAILABLE = 'BIR betting is not available'
    ALREADY_CANCELLED = 'The bet being cancelled is already cancelled'
    ID_NOT_UNIQUE = 'The unique ID provided for the bet already exists'
    BIR_FAILED = 'BIR bet failed'
    BAD_FREEBET_TOKEN = 'The freebet token being redeemed is invalid or not applicable'
    UNSUPPORTED_BET_TYPE = 'The operation requested does not support the given bet type'
    POOL_NOT_FOUND = 'Pool does not exist in the system'
    SELECTION_NOT_IN_POOL = 'Selection not in pool'
    BET_REJECTED = 'Bet rejected'
    BET_PENDING = 'Bet pending'
    LIVE_PRICE_NOT_PROVIDED = 'The live price for the selection is required but was not provided'
    GAME_NOT_FOUND = 'Game details are invalid/incomplete'
    INVALID_CURRENCY_SUPPLIED = 'Invalid currency supplied'
    INVALID_CURRENCY_FOR_CUSTOMER = 'Invalid currency for customer'
    NON_COMBINABLE_OUTCOMES = 'The outcomes given for an ncasttype bet are not combinable'
    INVALID_CHANNEL = 'The channel is invalid'
    NON_EXISTENT_SELECTION = 'Non existent selection'
    UNAVAILABLE_IN_REGION = 'Outcome is not available for your region'
    BLOCKBUSTER_INVALID_COUPON_ID = 'The blockbuster coupon ID in the request is invalid'
    BLOCKBUSTER_GROUP_MAX_SELNS_EXCEEDED = 'The number of selections in the blockbuster bet exceeds the allowed maximum'
    BLOCKBUSTER_COUPON_NOT_FOUND = 'Blockbuster coupon not found'
    BLOCKBUSTER_BET_PLACEMENT_FAILED = 'Blockbuster bet placement failed'
    WRONG_CUSTOMER = 'The cashout request is for a customer that does not match the customer of the original bet'
    PROXY_ERROR = 'Server is unavailable at the moment, please try again later.'
    PT_ERR_DISABLE_GAMING = 'Your account is suspended'
    DEFAULT_PLACEBET_ERROR = 'Your bet has not been accepted. Please try again.'
    RELOAD = 'Reload'
    TO_W = ' (To Win)'
    TO_E = ' (Each/Way)'
    EW = 'Each Way'
    EWE = 'E/W'
    WIN_ONLY = 'Win Only'
    SHOW_ALL = 'Show All'
    SELECTION_DETAILS = 'Selection details:'
    RESULT = 'Result:'
    STAKE_AND_RETURN = 'Stake and Return Details:'
    BET_PLACED = 'Bet Placed at:'
    BET_TYPE = 'Bet Type:'
    BET_LINES = 'Number of Lines:'
    BET_WIN_LINES = 'Number of win Lines:'
    TOTAL_STAKE = 'Total Stake'
    FREE_BET_STAKE = 'Free Bet Amount:'
    TOTAL_RETURNS = 'Total Returns:'
    TOTAL_ESTIMATED = 'Total Est. Returns'
    TOTAL_WINS = 'Total Wins:'
    WIN = '(Win)'
    WIN_OR_EACH_WAY = '(Win or Each Way)'
    LOTTERY = 'Lottery:'
    DRAW_TYPE = 'Draw Type:'
    DRAW_DATE = 'Draw Date:'
    YOUR_PICKS = 'Your picks:'
    ERROR = 'Error'
    SUCCESS = 'Success'
    PENDING_STAKE = 'Pending'
    OPEN_STAKE = 'Open'
    WON_STAKE = 'Won'.upper()
    CANCELLED_STAKE = 'Void'.upper()
    CASHOUT_STAKE = 'Cashed out'.upper()
    LOST_STAKE = 'Lost'.upper()
    _result_bet = namedtuple('result_bet', ['won', 'lost', 'pending', 'void', 'placed'])
    _result_bet_won = 'Won'
    _result_bet_lost = 'Lost'
    _result_bet_pending = 'Pending'
    _result_bet_void = 'Cancelled'
    _result_bet_placed = 'Placed'
    RESULT_BET = _result_bet(won=_result_bet_won,
                             lost=_result_bet_lost,
                             pending=_result_bet_pending,
                             void=_result_bet_void,
                             placed=_result_bet_placed)

    SELN_SELECTION = 'Selection'
    SELN_DATE = 'Date'
    SELN_ODDS = 'Odds'
    SELN_TERMS = 'E/W Terms'
    SELN_RESULTS = 'Result'
    EW_TEAMS = 'E/W Teams = '
    BOOSTED_MSG = 'This bet has been boosted!'
    BOOSTED_MSG_2 = 'Boosted!'
    MONEY_BACK_MSG = 'Money Back'
    EW_TERMS = '%eachWayNum/%eachWayDen odds, %eachWayPlaces places'
    NONE = 'None'
    MORE = 'More'
    REMOTE_PATTERN_ERROR_MSG = 'One or more of your selections are currently unavailable.'
    NO_LOGIN = 'You must log in to view {page}.'
    VOUCHER_SUCCESS = '%1\nHas been credited to your account.'
    VOUCHER_INVALID_LENGTH = 'Invalid voucher code length, please check and try again.'
    VOUCHER_INVALID = 'Invalid voucher code, please check and try again.'
    VOUCHER_ALREADY_REDEEMED = 'Voucher code has already been redeemed.'
    VOUCHER_CLAIMED_MAX = 'Exceeded maximum number of claims for this offer.'
    VOUCHER_NOT_YET_VALID = 'Voucher code not valid yet, see Voucher for Terms and Conditions.'
    VOUCHER_PAST_VALID = 'Voucher code has expired.'
    VOUCHER_NOT_REDEEMED = 'Invalid voucher code, please check and try again.'
    VOUCHER_SERVER_ERROR = 'Sorry there is a problem with the Voucher Code you have entered. Please try again and if the problem persists contact Customer Services.'
    VOUCHER_NO_DATA = 'Invalid voucher code, please check and try again.'
    SERVICE_ERROR = 'Sorry there is a problem with the Voucher Code you have entered. Please try again and if the problem persists contact Customer Services.'

    VOUCHER_FORMTITLE = 'Sports Voucher Code:'
    VOUCHER_FORMPLACE_HOLDER = 'Enter Promo Code'
    VOUCHER_FORMSUBMIT_BUTTON = 'Claim Now'
    VOUCHER_FORMVIEW_OFFERS = 'View all Offers'

    SF = 'Forecast'
    CF = 'Combination Forecast'
    RF = 'Reverse Forecast'
    TC = 'Tricast'
    CT = 'Combination Tricast'
    ES = 'Build Your Bet'
    BETS = 'Bets'
    SGL = 'Single'
    DBL = 'Double'
    TBL = 'Treble'
    TRX = 'Trixie'
    PAT = 'Patent'
    ACC4 = '4 Fold Acca'
    ACC5 = '5 Fold Acca'
    ACC6 = '6 Fold Acca'
    ACC7 = '7 Fold Acca'
    ACC8 = '8 Fold Acca'
    ACC9 = '9 Fold Acca'
    AC10 = '10 Fold Acca'
    AC11 = '11 Fold Acca'
    AC12 = '12 Fold Acca'
    AC13 = '13 Fold Acca'
    AC14 = '14 Fold Acca'
    AC15 = '15 Fold Acca'
    YAN = 'Yankee'
    L15 = 'Lucky 15'
    L31 = 'Lucky 31'
    L63 = 'Lucky 63'
    CAN = 'Canadian'
    HNZ = 'Heinz'
    SHNZ = 'Super Heinz'
    GOL = 'Goliath'
    P512 = 'Fivefolds from 12'
    P513 = 'Fivefolds from 13'
    P514 = 'Fivefolds from 14'
    P413 = 'Fourfolds from 13'
    P414 = 'Fourfolds from 14'
    P415 = 'Fourfolds from 15'
    P416 = 'Fourfolds from 16'
    P417 = 'Fourfolds from 17'
    P712 = 'Sevenfolds from 12'
    P612 = 'Sixfolds from 12'
    P912 = 'Ninefolds from 12'
    P813 = 'Eightfolds from 13'
    P613 = 'Sixfolds from 13'
    P713 = 'Sevenfolds from 13'
    P1014 = 'Tenfolds from 14'
    P914 = 'Ninefolds from 14'
    P1115 = 'Elevenfolds from 15'
    P1216 = 'Twelvefolds from 16'
    P1317 = 'Thirteenfolds from 17'
    P1518 = 'Fifteenfolds from 18'
    P1619 = 'Sixteenfolds from 19'
    P1720 = 'Seventeenfolds from 20'
    P1821 = 'Eighteenfolds from 21'
    P1922 = 'Nineteenfolds from 22'
    P2023 = 'Twentyfolds from 23'
    P2124 = 'Twenty-Onefolds from 24'
    P2225 = 'Twenty-Twofolds from 25'
    DS2 = 'Double Stakes About (2)'
    SS2 = 'Single Stakes About (2)'
    SS3 = 'Single Stakes About (3)'
    ROB = 'Round Robin'
    FLG = 'Flag'
    SS11 = 'Single Stakes About (11)'
    SS12 = 'Single Stakes About (12)'
    SS13 = 'Single Stakes About (13)'
    P913 = 'Ninefolds from 13'
    SS14 = 'Single Stakes About (14)'
    SS15 = 'Single Stakes About (15)'
    AC16 = '16 Fold Acca'
    AC17 = '17 Fold Acca'
    AC18 = '18 Fold Acca'
    AC19 = '19 Fold Acca'
    AC20 = '20 Fold Acca'
    AC21 = 'Accumulator (21)'
    AC22 = 'Accumulator (22)'
    AC23 = 'Accumulator (23)'
    AC24 = 'Accumulator (24)'
    AC25 = 'Accumulator (25)'
    THREE_BY4 = '3 By 4'
    DS3 = 'Double Stakes About (3)'
    FOUR_BY5 = '4 By 5'
    LY6 = 'Lucky 6'
    LY10 = 'Lucky 10'
    LY11 = 'Lucky 11'
    DS4 = 'Double Stakes About (4)'
    SS4 = 'Single Stakes About (4)'
    YAP = 'Yap'
    FSP = 'Fivespot'
    SS5 = 'Single Stakes About (5)'
    DS5 = 'Double Stakes About (5)'
    PON = 'Pontoon'
    DS6 = 'Double Stakes About (6)'
    SS6 = 'Single Stakes About (6)'
    L7B = 'Lucky 7 Bingo'
    MAG7 = 'Magnificent 7'
    SS7 = 'Single Stakes About (7)'
    DS7 = 'Double Stakes About (7)'
    SS8 = 'Single Stakes About (8)'
    DS8 = 'Double Stakes About (8)'
    UJK = 'Union Jack'
    SS9 = 'Single Stakes About (9)'
    DS9 = 'Double Stakes About (9)'
    SS10 = 'Single Stakes About (10)'
    DS10 = 'Double Stakes About (10)'
    DS11 = 'Double Stakes About (11)'
    DS12 = 'Double Stakes About (12)'
    DS13 = 'Double Stakes About (13)'
    DS14 = 'Double Stakes About (14)'
    DS15 = 'Double Stakes About (15)'
    AC_COMMON = 'Accumulator'
    SS_COMMON = 'Single Stakes About'
    DS_COMMON = 'Double Stakes About'
    CONFIRM_CLEAR_OF_BET_SLIP = 'Are you sure you want to clear your betslip?'
    CURRENCY = 'Currency: '
    BET_NO = 'Bet Number: '
    BET_ID = 'Bet ID:'
    BET_POTENTIAL = 'Bet Potential Win: '
    FOOTBALL_JD = 'Football Jackpot'
    WN = 'Win'
    PL = 'Place'
    SH = 'Show'
    EX = 'Exacta'
    TR = 'Trifecta'
    JACKPOT_SELECTION = 'Selection'
    DONE = 'Go Betting'
    GAME = 'Game'
    PLEASE_SELECT_ALL_15_BETS = 'Please Select All 15 bets To Place a Bet.'

    BET_RECEIPT_NO = 'Bet Receipt No: '
    FREE_BETS_AVAILABLE = 'Free Bets Available'
    BET_REJECTED_ERROR = 'Pool bet has been rejected by system.'
    INSUFICIENT_FOUNDS_ERROR = 'Bet is not placed due to insufficient funds. Please make a '
    DEPOSIT_SMALL = 'deposit.'
    TRX_INFO = '3 doubles and a treble'
    ACC_INFO = 'Accumulator Bet'
    SSDS_INFO = '(%1 Bets)'
    PAT_INFO = '3 singles, 3 doubles and a treble'
    YAN_INFO = '6 doubles, 4 trebles and a fourfold accumulator'
    CAN_INFO = '10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
    HNZ_INFO = '15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
    SHNZ_INFO = '21 doubles, 35 trebles, 35 fourfolds, 21 fivefolds, 7 sixfolds and a sevenfold accumulator'
    GOL_INFO = '28 doubles, 56 trebles, 70 fourfolds, 56 fivefolds, 28 sixfolds, 8 sevenfolds and an eightfold accumulator'
    L15_INFO = '4 singles, 6 doubles, 4 trebles and a fourfold accumulator'
    L31_INFO = '5 singles, 10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
    L63_INFO = '6 singles, 15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
    AC_COMMON_DIALOG_INFO = 'An Accumulator is a bet on four or more selections; all of which must win to gain a return.'
    SS_COMMON_DIALOG_INFO = 'This bet consists of 2 single bets on two selections, the stake on each successful selection is re-invested on the other selection.'
    DS_COMMON_DIALOG_INFO = 'Like Single Stakes About, but where returns from the 1st winning selection are invested at double the original stake on the 2nd selection.'
    DBL_DIALOG_INFO = 'A Double is a bet on two selections, both of which must win to gain a return.'
    TBL_DIALOG_INFO = 'A Treble is a bet on three selections; all three of which must win to gain a return.'
    TRX_DIALOG_INFO = 'A Trixie consists of four bets involving three selections from different events: 3 doubles and 1 treble. A minimum of 2 of your selections must be successful to get a return.'
    PAT_DIALOG_INFO = 'A Patent consists of 7 bets involving 3 selections from different events: 3 singles, 3 doubles and 1 treble. You need one successful selection to guarantee a return.'
    YAN_DIALOG_INFO = 'A Yankee consists of 11 bets involving 4 selections from different events: 6 doubles, 4 trebles and 1 fourfold accumulator.'
    L15_DIALOG_INFO = 'A Lucky 15 consists of 15 bets involving 4 selections in different events: 4 singles 6 doubles 4 trebles 1 accumulator. You need only 1 winner to guarantee a return. In the event of 1 winner and 3 losers, the odds for the winner are doubled. For 4 winners out of 4 a bonus of 10% is added. Please note: the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession.'
    CAN_DIALOG_INFO = 'A Super Yankee (or Canadian) consists of 26 bets involving 5 selections from different events: 10 doubles, 10 trebles, 5 four-fold accumulators and 1 five-fold accumulator. You need a minimum of 2 of your selections to win to get a return.'
    L31_DIALOG_INFO = 'A Lucky 31 consists of 31 bets involving 5 selections in different events: ' \
                      '5 singles 10 doubles 10 trebles 5 four-fold accumulators 1 five-fold accumulator You need only 1 winner to guarantee a return. ' \
                      'In the event of 1 winner and 4 losers, the odds for the winner are doubled. For 5 winners out of 5 a bonus of 20% is added. ' \
                      'Please note = the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. ' \
                      'Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession.'
    HNZ_DIALOG_INFO = 'A Heinz consists of 57 bets involving 6 selections from different events: 15 doubles, 20 trebles, 15 four-fold ' \
                      'accumulators, 6 five-fold accumulator and 1 six-fold accumulator. A minimum of 2 of your selections must be successful to get a return.'
    L63_DIALOG_INFO = 'A Lucky 63 consists of 63 bets involving 6 selections in different events: ' \
                      '6 singles 15 doubles 20 trebles 15 four-fold accumulators 6 five-fold accumulators 1 six-fold accumulator. ' \
                      'You need only 1 winner to guarantee a return. In the event of 1 winner and 5 losers, the odds for the winner are doubled. ' \
                      'For 5 winners out of 6 a bonus of 10% is added. For 6 winners out of 6 a bonus of 25% is added. ' \
                      'Please note = the above bonuses and concessions apply only to bets on horseracing, greyhounds or a combination of both. ' \
                      'Any accepted bet that includes a selection from a different sport will not qualify for any bonus or concession.'
    SHNZ_DIALOG_INFO = 'A Super Heinz consists of 120 bets involving 7 selections from different events: ' \
                       '21 doubles, 35 trebles, 35 four-fold accumulators, 21 five -fold accumulators 7 six-fold accumulators and 1 seven-fold accumulator. ' \
                       'A minimum of 2 of your selections must be successful to get a return.'
    GOL_DIALOG_INFO = 'A Goliath consists of 247 bets involving 8 selections from different events: ' \
                      '28 doubles, 56 trebles, 70 four-fold accumulators, 56 five-fold accumulators, 28 six-fold accumulators, 8 seven-fold accumulators ' \
                      'and 1 eight-fold accumulator. You need a minimum of 2 of your selections to be successful to get a return.'
    BETS_NUMBER = '%1 Bets'
    FS = 'First Goal Scorecast'
    LS = 'Last Goal Scorecast'
    BETSLIP_DEPOSIT_BTN = 'Deposit & Place Bet'
    BETSLIP_MAKE_QUICK_DEPOSIT_BTN = 'Make a deposit'.upper()
    BETSLIP_DEPOSIT_TITLE = 'Funds needed for bet'
    BETSLIP_QUICK_DEPOSIT_AMOUNT_FILED = '{amount} Min Deposit'
    BETSLIP_DEPOSIT_NOTIFICATION = 'Please deposit a min of £{0:.2f} to continue placing your bet'
    SUCCESS_DEPOSIT = 'Your deposit of {amount} was successful.'
    DEPOSIT_AND_PLACEBET_SUCCESS_MESSAGE = 'Your deposit was successful and your bet has been placed.'
    QD_BETSLIP_HEADER = 'Quick Deposit'
    BET_RECEIPT = 'Bet Receipt'
    REUSE_SELECTION = 'Reuse Selection'
    STAKE_IS_LOWER_THEN_FREE_BET = 'You must use all your free bet at once'
    NO_FREE_BETS_AVAILABLE = 'Don\'t Use Free Bet'
    SELECTIONS = 'Selections:'
    SELECTION = 'Selection:'
    START = 'Start:'
    POOL_TYPE = 'Pool type'
    TRICAST = 'Tricast'
    FORECAST = 'Forecast'
    REVERSE_FORECAST = 'Reverse Forecast'
    COMBINATION_FORECAST = 'Combination Forecast'
    COMBINATION_TRICAST = 'Combination Tricast'
    PRIVATE_MARKET = 'Free bet has expired.'
    BET_HISTORY_ERROR_MESSAGE = 'We\'re sorry. Bet History service is currently unavailable, please try again later.'
    ERROR_SERVICE_DEPARTMENT_MESSAGE = 'If this problem persists, contact our '
    ERROR_SERVICE_DEPARTMENT_LINK = 'Customer Service Department'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'

    _overask_messages = namedtuple('overask_messages', ['bet_accepted', 'customer_action_time_expired', 'bet_is_declined',
                                                        'some_bets_with_freebet', 'accept_offer'])
    _overask_messages_bet_accepted = 'This bet has been accepted'
    _overask_messages_customer_action_time_expired = 'Your bets were not placed as the offer has expired. Please try again.'
    _overask_messages_bet_is_declined = 'This bet has not been accepted by traders!'
    _overask_messages_some_bets_with_freebet = 'Freebet cannot be used with this bet'
    _overask_messages_accept_offer = 'You\'re accepting this Trade Offer'
    OVERASK_MESSAGES = _overask_messages(bet_accepted=_overask_messages_bet_accepted,
                                         customer_action_time_expired=_overask_messages_customer_action_time_expired,
                                         bet_is_declined=_overask_messages_bet_is_declined,
                                         some_bets_with_freebet=_overask_messages_some_bets_with_freebet,
                                         accept_offer=_overask_messages_accept_offer)

    _overask_elements = namedtuple('overask_elements', ['cancel_traders_offer', 'in_progress_notification',
                                                        'in_progress_notification_message', 'confirm_cancel_dialog_title',
                                                        'confirm_cancel_dialog_message', 'cancel_cancel_traders_offer',
                                                        'confirm_cancel_traders_offer', 'removed', 'undo', 'and_'])
    _overask_elements_cancel_traders_offer = 'Cancel'
    _overask_elements_in_progress_notification = 'Betslip is busy'
    _overask_elements_in_progress_notification_message = 'Please wait until the betslip is finished processing your bets before adding more selections. Thanks'
    _overask_elements_confirm_cancel_dialog_title = 'Cancel Offer?'
    _overask_elements_confirm_cancel_dialog_message = 'Moving away from this screen will cancel your offer. Are you sure you want to go ahead?'
    _overask_elements_cancel_cancel_traders_offer = 'NO, RETURN'
    _overask_elements_confirm_cancel_traders_offer = 'CANCEL OFFER'
    _overask_elements_removed = 'REMOVED'
    _overask_elements_undo = 'UNDO'
    _overask_elements_and = 'AND'
    OVERASK_ELEMENTS = _overask_elements(cancel_traders_offer=_overask_elements_cancel_traders_offer,
                                         in_progress_notification=_overask_elements_in_progress_notification,
                                         in_progress_notification_message=_overask_elements_in_progress_notification_message,
                                         confirm_cancel_dialog_title=_overask_elements_confirm_cancel_dialog_title,
                                         confirm_cancel_dialog_message=_overask_elements_confirm_cancel_dialog_message,
                                         cancel_cancel_traders_offer=_overask_elements_cancel_cancel_traders_offer,
                                         confirm_cancel_traders_offer=_overask_elements_confirm_cancel_traders_offer,
                                         removed=_overask_elements_removed,
                                         undo=_overask_elements_undo,
                                         and_=_overask_elements_and)

    OFFER = 'Offer'
    POT_BET_TITLE = '{number} Lines'
    LINES_NUMBER_TITLE = 'x%1 Lines'
    TOTAL_STAKE_TITLE = 'Stake {value}'
    UPGRADE_ACCOUNT = 'UPGRADE YOUR ACCOUNT & BET NOW'
    WIN_ALERTS = 'Win Alert'
    ODDS_BOOST_EXPIRED_OR_REDEEMED = 'Your Odds Boost has been expired/redeemed.'
    REMOVE_ALL_SELECTIONS = 'Remove All'.upper()
    YOUR_SELECTIONS = 'Your Selections'
    USE_FREE_BET = 'Use Free Bet'
    REMOVE_FREE_BET = 'Remove Free Bet'
    FREE_BETS_AVAILABLE_NUMBER = 'Free Bets Available (x%1)'
    USE_FREE_BET_TOOLTIP = 'Don\'t forget to use your Free Bets!'
    WHAT_IS_ACCA = 'What is an Acca?'
    BET_RESTRICTED = 'This bet is currently prohibited in your location'
    FREE_BET_NOT_ELIGIBLE = 'Free Bet Not Eligible'
    FREE_BET_CAN_NOT_BE_ADDED = 'Sorry, your free bet cannot be added.'
    SUSPENDED_LABEL = 'SUSPENDED'

    BETSLIP_SINGLE_STAKES_ABOUT = 'SINGLE STAKES ABOUT ({0})'
    BETSLIP_BETTYPES = ['SINGLE', 'DOUBLE', 'TREBLE', 'TRIXIE', 'PATENT', 'ACCA', 'LUCKY 15', 'YANKEE', '5-A-SIDE']
    SELECTION_DISABLED = 'One of your selections has been suspended'
    BETSLIP_BETSTATUS = ['LOST', 'WON', 'VOID', 'CASHED OUT']

    ACCA_SUGGESTED_OFFER_FOR_4_PLUS = 'ACCA INSURANCE: 1 away from a FREE BET! (up to £) if ONE selection ' \
                                      'lets you down. Acca odds must be at least 3/1. Min stake £2'
    ESTIMATED_RESULTS_NA = 'N/A'