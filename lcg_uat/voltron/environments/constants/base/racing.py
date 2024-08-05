from collections import namedtuple


class Racing(object):
    """
    src/app/lazy-modules/locale/translations/en-US/racing.lang.ts
    """
    STARTS_IN = 'Starts in'
    STARTS_AT = 'Starts at'
    DISTANCE = 'Distance'
    FLAT = 'Flat'
    GOING = 'Going'
    SPOTLIGHT_TITLE = 'Spotlight'
    OFFICIAL_RATING = 'OR'
    OFFICIAL_RATING_LADBROKES = 'RPR'
    AGE = 'Age'
    WEIGHT = 'Weight'
    NO_DETAILS = 'Currently there are no Details available.'
    SHOW_MORE = 'Show More'
    SHOW_LESS = 'Show Less'

    _race_stage = namedtuple('race_stage', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'O', 'P', 'R', 'W'])
    _race_stage_A = 'Parading'
    _race_stage_B = 'Going down'
    _race_stage_C = 'At the post'
    _race_stage_D = 'Delayed'
    _race_stage_E = 'Going behind'
    _race_stage_F = 'Approaching Traps'
    _race_stage_G = 'Going into Traps'
    _race_stage_H = 'Under orders'
    _race_stage_J = 'White flag'
    _race_stage_K = 'False start'
    _race_stage_M = 'Betting suspended'
    _race_stage_N = 'No race'
    _race_stage_O = 'Off'
    _race_stage_P = 'Back / Paddock'
    _race_stage_R = 'Hare'
    _race_stage_W = 'Awaiting Result'

    RACE_STAGE = _race_stage(A=_race_stage_A,
                             B=_race_stage_B,
                             C=_race_stage_C,
                             D=_race_stage_D,
                             E=_race_stage_E,
                             F=_race_stage_F,
                             G=_race_stage_G,
                             H=_race_stage_H,
                             J=_race_stage_J,
                             K=_race_stage_K,
                             M=_race_stage_M,
                             N=_race_stage_N,
                             O=_race_stage_O,  # noqa: E741
                             P=_race_stage_P,
                             R=_race_stage_R,
                             W=_race_stage_W)

    _racing_form_event_going = namedtuple('racing_form_event_going', ['AW', 'F', 'FT', 'G', 'GF', 'GS', 'GY', 'H', 'HD',
                                                                      'S', 'SD', 'SF', 'SH', 'SS', 'Y', 'YS', 'HY'])
    _racing_form_event_going_AW = 'All Weather'
    _racing_form_event_going_F = 'Firm'
    _racing_form_event_going_FT = 'Fast'
    _racing_form_event_going_G = 'Good'
    _racing_form_event_going_GF = 'Good to Firm'
    _racing_form_event_going_GS = 'Good to Soft'
    _racing_form_event_going_GY = 'Good to Yielding'
    _racing_form_event_going_H = 'Heavy'
    _racing_form_event_going_HD = 'Hard'
    _racing_form_event_going_HY = 'Heavy'
    _racing_form_event_going_S = 'Soft'
    _racing_form_event_going_SD = 'Standard'
    _racing_form_event_going_SF = 'Standard to Fast'
    _racing_form_event_going_SH = 'Soft to Heavy'
    _racing_form_event_going_SS = 'Standard to Soft'
    _racing_form_event_going_Y = 'Yielding'
    _racing_form_event_going_YS = 'Yielding to Soft'
    RACING_FORM_EVENT_GOING = _racing_form_event_going(AW=_racing_form_event_going_AW,
                                                       F=_racing_form_event_going_F,
                                                       FT=_racing_form_event_going_FT,
                                                       G=_racing_form_event_going_G,
                                                       GF=_racing_form_event_going_GF,
                                                       GS=_racing_form_event_going_GS,
                                                       GY=_racing_form_event_going_GY,
                                                       H=_racing_form_event_going_H,
                                                       HD=_racing_form_event_going_HD,
                                                       HY=_racing_form_event_going_HY,
                                                       S=_racing_form_event_going_S,
                                                       SD=_racing_form_event_going_SD,
                                                       SF=_racing_form_event_going_SF,
                                                       SH=_racing_form_event_going_SH,
                                                       SS=_racing_form_event_going_SS,
                                                       Y=_racing_form_event_going_Y,
                                                       YS=_racing_form_event_going_YS)

    _form_table = namedtuple('form_table', ['date', 'conditions', 'weight', 'analysis', 'jockey', 'official_rating',
                                            'top_speed', 'rpr'])
    _form_table_date = 'Date'
    _form_table_conditions = 'Conditions'
    _form_table_weight = 'Weight'
    _form_table_analysis = 'Analysis'
    _form_table_jockey = 'Jockey'
    _form_table_official_rating = 'OR'
    _form_table_top_speed = 'TS'
    _form_table_rpr = 'RPR'
    FORM_TABLE = _form_table(date=_form_table_date,
                             conditions=_form_table_conditions,
                             weight=_form_table_weight,
                             analysis=_form_table_analysis,
                             jockey=_form_table_jockey,
                             official_rating=_form_table_official_rating,
                             top_speed=_form_table_top_speed,
                             rpr=_form_table_rpr)

    _race_type = namedtuple('race_type', ['NHF', 'CHS', 'FLT', 'HDL', 'HNT', 'AWF', 'AWC', 'AWB', 'AWH'])
    _race_type_NHF = 'NH Flat'
    _race_type_CHS = 'Chase Turf'
    _race_type_FLT = 'Flat Turf'
    _race_type_HDL = 'Hurdle Turf'
    _race_type_HNT = 'Hunter Chase'
    _race_type_AWF = 'Flat AW'
    _race_type_AWC = 'Chase AW'
    _race_type_AWB = 'Bumper AW'
    _race_type_AWH = 'Hurdle AW'
    RACE_TYPE = _race_type(NHF=_race_type_NHF,
                           CHS=_race_type_CHS,
                           FLT=_race_type_FLT,
                           HDL=_race_type_HDL,
                           HNT=_race_type_HNT,
                           AWF=_race_type_AWF,
                           AWC=_race_type_AWC,
                           AWB=_race_type_AWB,
                           AWH=_race_type_AWH)

    VIEW_FULL_RACE = 'Full Race Card'
    RACE_STAGE_LABEL = 'Next Race'
    DAY_SUNDAY = 'Sunday'
    DAY_MONDAY = 'Monday'
    DAY_TUESDAY = 'Tuesday'
    DAY_WEDNESDAY = 'Wednesday'
    DAY_THURSDAY = 'Thursday'
    DAY_FRIDAY = 'Friday'
    DAY_SATURDAY = 'Saturday'
    DAY_SUN = 'Sun'
    DAY_MON = 'Mon'
    DAY_TUE = 'Tue'
    DAY_WED = 'Wed'
    DAY_THU = 'Thu'
    DAY_FRI = 'Fri'
    YOURCALL_SPECIALS = 'Yourcall Specials'
    DAY_SAT = 'Sat'
    EVFLAG_FT = 'Flat'
    EVFLAG_NH = 'National Hunt'
    EVFLAG_IT = 'International'
    BET_NOW = 'Bet Now'
    ADD_TO_BETSLIP = 'Add to betslip'
    LIVE_NOW = 'Live'
    RACE_OFF = 'Race Off'
    VIEW_ALL = 'View All'
    VIRTUALS = 'virtuals'
    SORT_BY = 'SORT BY = '
    VIEW_ALL_VIRTUALS = 'View all virtuals'
    RACE_GRADE = 'Race Grade'
    TRAINER = 'T'
    RATING = 'Rating'
    TIMEFORM_SUMMARY = 'Timeform Summary'
    VIEW_ALL_YC = 'View All #Yourcall Specials'
    NO_EVENTS_FOUND = 'No events found'
    TF = 'TF'
    PICK = 'Pick'
    SETTLED_RESULT = 'Settled Result'
    UNCONFIRMED_RESULT = 'Unconfirmed Result'
    DIVIDEND_FC = 'Forecast'
    DIVIDEND_TC = 'Tricast'
    DIVIDEND = 'DIVIDEND'
    RESULT = 'RESULT'
    RACE_RESULT = 'RACE RESULT'
    RULE_4 = 'Rule 4'
    PLACE = 'Place'
    SILK = 'Silk'
    RUNNERS = 'Runners'
    ODDS_COLUMN = 'ODDS'
    NON_RUNNERS = 'NON RUNNERS'
    DEDUCTION = 'DEDUCTION'
    NO_RACING_RESULTS_FOUND = 'No results found'
    OFFERS_AND_FEATURED_RACES = 'Offers and featured races'
    EXTRA_PLACE_TITLE = 'Extra Place Offer'.upper()
    ITV = 'ITV Races'
    FORM = 'Form'
    FORM_COLON = 'Form: '
    NON_RUNNER = 'N/R'
    BUILD_YOUR_OWN_RACE_CARD = 'Build Your Own Racecard'
    YOURCALL_SHOTS = ', you call the shots'
    BEGIN_TO = 'Begin to'
    SELECT_FROM_MEETINGS = 'Select up to 10 races from any UK, IRE and International meetings'
    BUILD_RACE_CARD = 'Build a Racecard'
    EXIT_BUILDER = 'Exit builder'
    CLEAR_SELECTIONS = 'Clear all selections'
    BUILD_YOUR_RACE_CARD = 'Build your racecard'
    BUILD_YOUR_RACE_CARD_LIMIT_MESSAGE = 'You cannot select anymore races for build your racecard'
    FOR_TRI_MSG = 'Pick the finishing order of the first {num} runners'
    INTERNATIONAL_TITLE = 'International'
    NEXT_RACES = 'Next Races'
    MEETINGS = 'Meetings'
    VIEW = 'view'
    THE_ODDS = 'the Odds'
    EXTRA_PLACE = 'Extra Place'
    ADD_SELECTION = 'Please add another selection'

    UNNAMED_FAVORITE = 'Unnamed Favourite'
    UNNAMED_FAVORITE_2ND = 'Unnamed 2nd Favourite'

    _racing_edp_market_tabs = namedtuple('RACING_EDP_MARKET_TABS', ('win_or_ew', 'forecast', 'tricast', 'win_only',
                                                                    'betting_wo', 'betting_without', 'to_finish', 'top_finish',
                                                                    'place_insurance', 'more_markets', 'totepool', 'antepost'))
    RACING_EDP_MARKET_TABS = _racing_edp_market_tabs(win_or_ew='WIN OR E/W',
                                                     forecast='FORECAST',
                                                     tricast='TRICAST',
                                                     win_only='WIN ONLY',
                                                     betting_wo='BETTING W/O',
                                                     betting_without='BETTING WITHOUT',
                                                     to_finish='TO FINISH',
                                                     top_finish='TOP FINISH',
                                                     place_insurance='PLACE INSURANCE',
                                                     more_markets='MORE MARKETS',
                                                     totepool='TOTEPOOL',
                                                     antepost='ANTEPOST')
    RACING_EDP_MARKET_TABS_NAMES = ['WIN OR E/W', 'FORECAST', 'TRICAST']

    DAYS = ['TODAY', 'TOMORROW', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    RACING_DEFAULT_TAB_NAME = 'FEATURED'
    RACING_FUTURE_TAB_NAME = 'FUTURE'
    RACING_SPECIALS_TAB_NAME = 'SPECIALS'
    RACING_YOURCALL_TAB_NAME = 'YOURCALL'  #yourcall feature is removed
    RACING_RESULTS_TAB_NAME = 'RESULTS'
    RACING_TAB_NAMES = [RACING_DEFAULT_TAB_NAME, RACING_FUTURE_TAB_NAME, RACING_SPECIALS_TAB_NAME]
    RACING_ANTEPOST_SWITCHERS = ['FLAT', 'NATIONAL HUNT', 'INTERNATIONAL']
    UK_AND_IRE_TYPE_NAME = 'UK And Irish Races'
    UK_TYPE_NAME = 'UK Races'
    YC_SPECIALS = 'YOURCALL SPECIALS'
    INTERNATIONAL_TYPE_NAME = 'International Races'
    INTERNATIONAL_TOTE_NAME = 'INTERNATIONAL TOTE CAROUSEL'
    VIRTUAL_TYPE_NAME = 'VIRTUAL RACE'
    LEGENDS_TYPE_NAME = 'Coral Legends'
    AUSTRALIA_TYPE_NAME = 'AUSTRALIA'
    SOUTH_AFRICA_TYPE_NAME = 'SOUTH AFRICA'
    FRANCE_TYPE_NAME = 'FRANCE'
    INDIA_TYPE_NAME = 'INDIA'
    UAE_TYPE_NAME = 'UAE'
    CHILE_TYPE_NAME = 'CHILE'
    USA_TYPE_NAME = 'USA'
    INTERNATIONAL_TAG_NAME = 'INTERNATIONAL'
    ENHANCED_MULTIPLES_NAME = 'ENHANCED MULTIPLES'
    FEATURED_OFFERS_SECTION_TITLE = 'OFFERS AND FEATURED RACES'
    RACING_SPECIALS_NAME = 'RACING SPECIALS'
    PRICE_BOMB_NAME = 'PRICE BOMB'
    MOBILE_EXCLUSIVE_NAME = 'MOBILE EXCLUSIVE'
    RACING_SPECIALS_CAROUSEL_LABEL = 'Specials'
    ENHANCED_RACES = 'ENHANCED RACES'

    JOCKEY_TEXT = 'J: {jockey}'
    TRAINER_TEXT = 'T: {trainer}'
    JOCKEY_TRAINER_TEXT = f'{JOCKEY_TEXT} / {TRAINER_TEXT}'
    VERDICT = 'VERDICT'

    _checkboxes = namedtuple('CHECKBOXES', ('first', 'second', 'third', 'any'))
    CHECKBOXES = _checkboxes(first='"1st"',
                             second='"2nd"',
                             third='"3rd"',
                             any='"ANY"')

    RACING_EDP_FORECAST_RACING_BUTTONS = [CHECKBOXES.first, CHECKBOXES.second, CHECKBOXES.any]
    RACING_EDP_TRICAST_RACING_BUTTONS = [CHECKBOXES.first, CHECKBOXES.second, CHECKBOXES.third, CHECKBOXES.any]

    RACING_EDP_DEFAULT_MARKET_TAB = 'WIN OR E/W'
    RACING_EDP_BETTING_WITHOUT = 'BETTING WITHOUT'
    RACING_EDP_BETTING_WITHOUT_SHORTCUT = 'BETTING W'
    RACING_EDP_BETTING_WITHOUT_SHORTCUT_DESKTOP = 'Betting W'
    RACING_EDP_FORECAST_MARKET_TAB = 'FORECAST'
    RACING_EDP_TRICAST_MARKET_TAB = 'TRICAST'
    RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME = 'WIN OR EACH WAY'
    RACING_EDP_WIN_OR_EACH_WAY_TAB = 'WIN/EACH WAY'
    TOP_FINISH_MARKET_NAME = 'TOP FINISH'
    TOP_FINISH_FIXTURE_HEADERS = ['TOP 2', 'TOP 3', 'TOP 4']
    TO_FINISH_MARKET_NAME = 'TO FINISH'
    TO_FINISH_FIXTURE_HEADERS = ['2ND', '3RD', '4TH']
    PLACE_INSURANCE_FIXTURE_HEADERS = TO_FINISH_FIXTURE_HEADERS
    BUILD_YOUR_RACECARD_BUTTON = 'BUILD A RACECARD'

    PRICE_SORTING_OPTION_SELECTED = 'Price'
    CARD_SORTING_OPTION_SELECTED = 'Racecard'
    CARD_SORTING_OPTION = 'Racecard'
    COUNTRY_SKIP_LIST = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL', 'ENHANCED RACES', 'NEXT RACES',
                         'OFFERS & FEATURED RACES', 'EXTRA PLACE RACES']

    # Racing Legacy Design
    DEFAULT_TIME_GROUPING_BUTTON_RACING = 'BY MEETING'
    BY_TIME_GROUPING_BUTTON_RACING = 'BY TIME'
    EXPECTED_TIME_GROUPING_BUTTONS_RACING = ['BY MEETING', 'BY TIME']

    HORSE_RACING_TAB_NAME = 'HORSE RACING'  # for some cases used property horse_racing_title from BaseRacing class

    VIRTUAL_SECTION_LIST = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL']
    SHOW_INFO_TEXT = 'Show Info'
    HIDE_INFO_TEXT = 'Hide Info'

    RACING_POST_STAR_RATING = 'Racing Post STAR RATING'.upper()
    RACING_POST_TIPS = 'Racing Post Tips'.upper()
    MOST_TIPPED = 'Most Tipped'.upper()
    int_filter_name = "International"
    uk_filter_name = 'UK & Irish'
    vr_filter_name = "VIRTUALS"

    # Font
    FONT_FAMILY = 'Lato'

