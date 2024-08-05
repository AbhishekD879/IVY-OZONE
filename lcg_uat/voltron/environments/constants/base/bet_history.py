from collections import namedtuple


class BetHistory(object):
    """
    src/app/lazy-modules/locale/translations/en-US/bethistory.lang.ts
    """
    TAB_TITLE = 'My Bets'
    ODDS = 'Odds'
    CLOSE = 'Close'
    CASHOUT = 'Cash Out'
    CASHOUT_BUTTON_TEXT = 'CASH OUT '
    CONFIRM_CASHOUT_BUTTON_TEXT = 'CONFIRM '
    BETSLIP_CASH_OUT_TAB_TITLE = 'Betslip / Cash Out'
    STAKE = 'Unit Stake:'
    STAKE_PER_LINE = 'Stake:'
    NEW_STAKE_PER_LINE = 'New Stake:'
    TOTAL_STAKE = 'Total Stake:'
    NEW_TOTAL_STAKE = 'New Total Stake:'
    EACH_WAY_STAKE = '(Each/Way)'
    EWE = 'Each Way'
    SP = 'SP'
    SELECTION_INFORMATION = 'Selection Information'
    CLOSE_BUTTON = 'Close'
    _clock = namedtuple('clock', ['live', 'footballFT'])
    _clock_live = 'Live'
    _clock_footballFT = 'FT'
    CLOCK = _clock(live=_clock_live,
                   footballFT=_clock_footballFT)
    CASHED_OUT_LABEL = 'YOU CASHED OUT: £{0:.2f}'
    CASHED_OUT_LABEL_SETTLE_BET = 'YOU CASHED OUT:'
    YOU_WON_LABEL = 'You Won:'
    SUSPENDED = 'susp'
    VOID = 'void'
    RELOAD = 'Reload'
    TOTAL_RETURN = 'Estimated Returns:'
    NEW_TOTAL_RETURN = 'New Est. Returns'
    CASHOUT_BETS = 'Cash Out My Bet'
    NO_CASHOUT_BETS = 'You currently have no cash out bets.'
    CASHED_OUT_RETURNS = 'Cashed out returns:'
    STATUS_CASHED_OUT = 'Status: Cashed out'
    BEST_ODD_GURANTEED = 'Best Odds Guaranteed'

    _cashout_bet = namedtuple('cashout_bet', ['success_cashout', 'unsuccess_cashout', 'in_progress', 'confirm',
                                              'cash_out', 'full_cash_out', 'confirm_cash_out', 'cash_out_bet_suspended',
                                              'error_msg', 'decrease', 'bet_not_cashouted', 'free_bet_notification',
                                              'cashout_attempt_errors', 'cashout_unavailable'])
    _cashout_bet_cashout_attempt_errors = namedtuple('cashout_attempt_errors',
                                                     ['default', 'cashout_unavailable_cust_no_cashout',
                                                      'cashout_bet_cashed_out',
                                                      'cashout_bet_settled', 'cashout_cust_restrict_flag',
                                                      'cashout_unavailable_price_change', 'cashout_bet_no_cashout',
                                                      'cashout_bet_not_loaded', 'cashout_bettype_not_allowed',
                                                      'cashout_cust_error',
                                                      'cashout_disabled', 'cashout_freebet_used',
                                                      'cashout_hcap_changed',
                                                      'cashout_legsort_not_allowed', 'cashout_multis_not_allowed',
                                                      'cashout_no_odds',
                                                      'cashout_pricetype_not_allowed', 'cashout_seln_no_cashout',
                                                      'cashout_singles_not_allowed',
                                                      'cashout_value_change', 'cashout_seln_suspended'])
    _cashout_bet_cashout_unavailable = namedtuple('cashout_unavailable', ['bet_worth_nothing', 'default'])
    _cashout_bet_success_cashout = 'SUCCESSFUL CASH OUT'
    _cashout_bet_unsuccess_cashout = 'UNSUCCESSFUL CASH OUT'
    _cashout_bet_in_progress = 'IN PROGRESS'
    _cashout_bet_confirm = 'CONFIRM'
    _cashout_bet_cash_out = 'CASH OUT'
    _cashout_bet_full_cash_out = 'FULL CASH OUT'
    _cashout_bet_confirm_cash_out = 'CONFIRM CASH OUT'
    _cashout_bet_cash_out_bet_suspended = 'CASH OUT SUSPENDED'
    _cashout_bet_error_msg = 'Cash Out Unavailable.'
    _cashout_bet_decrease = 'The Cash Out value of this bet has changed. Please try again.'
    _cashout_bet_bet_not_cashouted = 'Bet isn\'t cashouted.'
    _cashout_bet_free_bet_notification = 'Free bets has a reduced Cash Out value'
    _cashout_bet_cashout_attempt_errors_default = 'Cash Out unsuccessful, please try again.'
    _cashout_bet_cashout_attempt_errors_cashout_unavailable_cust_no_cashout = 'Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be an error.'
    _cashout_bet_cashout_attempt_errors_cashout_cust_restrict_flag = 'Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be an error.'
    _cashout_bet_cashout_attempt_errors_cashout_bet_cashed_out = 'Your Cash Out attempt was unsuccessful, as your bet has already been Cashed Out.'
    _cashout_bet_cashout_attempt_errors_cashout_bet_settled = 'Your Cash Out attempt was unsuccessful, as your bet has already been settled.'
    _cashout_bet_cashout_attempt_errors_cashout_unavailable_price_change = 'Your Cash Out attempt was unsuccessful due to a price change. Please try again.'
    _cashout_bet_cashout_attempt_errors_cashout_bet_no_cashout = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_bet_not_loaded = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_bettype_not_allowed = 'Cash Out is unavailable on this bet type.'
    _cashout_bet_cashout_attempt_errors_cashout_cust_error = 'Sorry, we cannot authorise Cash Out from your location.'
    _cashout_bet_cashout_attempt_errors_cashout_disabled = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_freebet_used = 'Bets placed with a free bet or bets triggering a free bet offer cannot be Cashed Out.'
    _cashout_bet_cashout_attempt_errors_cashout_hcap_changed = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_legsort_not_allowed = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_multis_not_allowed = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_no_odds = 'One or more events in your bet are not available for in-play Cash Out.'
    _cashout_bet_cashout_attempt_errors_cashout_pricetype_not_allowed = 'Bets placed at starting price (SP) cannot be Cashed Out.'
    _cashout_bet_cashout_attempt_errors_cashout_seln_no_cashout = 'One or more events in your bet are not available for Cash Out.'
    _cashout_bet_cashout_attempt_errors_cashout_singles_not_allowed = 'Cash Out is unavailable on this bet.'
    _cashout_bet_cashout_attempt_errors_cashout_value_change = 'Your Cash Out attempt was unsuccessful due to a price change. Please try again.'
    _cashout_bet_cashout_attempt_errors_cashout_seln_suspended = 'Your Cash Out attempt was unsuccessful, your selection is suspended.'
    _cashout_bet_cashout_unavailable_bet_worth_nothing = 'Cash Out is unavailable because the offer is less than 0.00'
    _cashout_bet_cashout_unavailable_default = 'Cash Out is unavailable'
    CASHOUT_BET = _cashout_bet(success_cashout=_cashout_bet_cashout_unavailable,
                               unsuccess_cashout=_cashout_bet_unsuccess_cashout,
                               in_progress=_cashout_bet_in_progress,
                               confirm=_cashout_bet_confirm,
                               cash_out=_cashout_bet_cash_out,
                               full_cash_out=_cashout_bet_full_cash_out,
                               confirm_cash_out=_cashout_bet_confirm_cash_out,
                               cash_out_bet_suspended=_cashout_bet_cash_out_bet_suspended,
                               error_msg=_cashout_bet_error_msg,
                               decrease=_cashout_bet_decrease,
                               bet_not_cashouted=_cashout_bet_bet_not_cashouted,
                               free_bet_notification=_cashout_bet_free_bet_notification,
                               cashout_attempt_errors=_cashout_bet_cashout_attempt_errors(
                                   default=_cashout_bet_cashout_attempt_errors_default,
                                   cashout_unavailable_cust_no_cashout=_cashout_bet_cashout_attempt_errors_cashout_unavailable_cust_no_cashout,
                                   cashout_cust_restrict_flag=_cashout_bet_cashout_attempt_errors_cashout_cust_restrict_flag,
                                   cashout_bet_cashed_out=_cashout_bet_cashout_attempt_errors_cashout_bet_cashed_out,
                                   cashout_bet_settled=_cashout_bet_cashout_attempt_errors_cashout_bet_settled,
                                   cashout_unavailable_price_change=_cashout_bet_cashout_attempt_errors_cashout_unavailable_price_change,
                                   cashout_bet_no_cashout=_cashout_bet_cashout_attempt_errors_cashout_bet_no_cashout,
                                   cashout_bet_not_loaded=_cashout_bet_cashout_attempt_errors_cashout_bet_not_loaded,
                                   cashout_bettype_not_allowed=_cashout_bet_cashout_attempt_errors_cashout_bettype_not_allowed,
                                   cashout_cust_error=_cashout_bet_cashout_attempt_errors_cashout_cust_error,
                                   cashout_disabled=_cashout_bet_cashout_attempt_errors_cashout_disabled,
                                   cashout_freebet_used=_cashout_bet_cashout_attempt_errors_cashout_freebet_used,
                                   cashout_hcap_changed=_cashout_bet_cashout_attempt_errors_cashout_hcap_changed,
                                   cashout_legsort_not_allowed=_cashout_bet_cashout_attempt_errors_cashout_legsort_not_allowed,
                                   cashout_no_odds=_cashout_bet_cashout_attempt_errors_cashout_no_odds,
                                   cashout_multis_not_allowed=_cashout_bet_cashout_attempt_errors_cashout_multis_not_allowed,
                                   cashout_pricetype_not_allowed=_cashout_bet_cashout_attempt_errors_cashout_pricetype_not_allowed,
                                   cashout_seln_no_cashout=_cashout_bet_cashout_attempt_errors_cashout_seln_no_cashout,
                                   cashout_singles_not_allowed=_cashout_bet_cashout_attempt_errors_cashout_singles_not_allowed,
                                   cashout_value_change=_cashout_bet_cashout_attempt_errors_cashout_value_change,
                                   cashout_seln_suspended=_cashout_bet_cashout_attempt_errors_cashout_seln_suspended),
                               cashout_unavailable=_cashout_bet_cashout_unavailable(
                                   bet_worth_nothing=_cashout_bet_cashout_unavailable_bet_worth_nothing,
                                   default=_cashout_bet_cashout_unavailable_default))

    INFO_BET_PLACED = 'Bet Placed at'
    INFO_BET_TYPE = 'Bet Type'
    INFO_LINES_NUM = 'Lines'
    INFO_TOTAL_STAKE = 'Total Stake'
    INFO_TOTAL_RETURN = 'Est. Returns'
    INFO_WIN_LINES_NUM = 'Win Lines'

    CONFIRMATION = 'Confirmation'
    PARTIAL_CASH_OUT_CONFIRMATION_WINDOW_TEXT = 'Please confirm you want to proceed with your partial cash out for '
    FULL_CASH_OUT_CONFIRMATION_WINDOW_TEXT = 'Please confirm you want to proceed with your full cash out for '
    PARTIAL_CASH_OUT_VALUE_CHANGED = 'The Cash Out value of this bet has changed. Please try again.'
    PARTIAL_CASH_OUT_UNAVAILABLE = 'Partial Cash Out unavailable.'
    CASH_OUT_UNAVAILABLE = 'Cash Out Unavailable.'
    PARTIAL_CASH_OUT_SUCCESS = 'Partial Cash Out Successful'
    FULL_CASH_OUT_SUCCESS = 'Cash Out Successful'
    PARTIAL_CASH_OUT_BTN_TEXT = 'PARTIAL CASH OUT'
    PARTIAL_CASH_OUT_CONFIRM_BTN = 'Ok'
    PARTIAL_CASH_OUT_CANCEL_BTN = 'Cancel'

    _bet_types = namedtuple('bet_types', ['SGL', 'DBL', 'TBL', 'TRX', 'PAT', 'ACC4', 'ACC5', 'ACC6', 'ACC8', 'ACC9',
                                          'AC10', 'AC11', 'AC12', 'AC13', 'AC14', 'AC15', 'YAN', 'L15', 'L31',
                                          'L63', 'CAN', 'HNZ', 'SHNZ', 'GOL', 'P512', 'P513', 'P514', 'P413', 'P414',
                                          'P415', 'P416', 'P417', 'P712', 'P612', 'P912', 'P813', 'P613', 'P713',
                                          'P1014', 'P914', 'P1115', 'P1216', 'P1317', 'P1518', 'P1619', 'P1720',
                                          'P1821', 'P1922', 'P2023', 'P2124', 'P2225', 'DS2', 'SS2', 'SS3', 'ROB', 'FLG',
                                          'SS11', 'SS12', 'SS13', 'P913', 'SS14', 'SS15', 'AC16', 'AC17', 'AC18', 'AC19',
                                          'AC20', 'AC21', 'AC22', 'AC23', 'AC24', 'AC25', 'THREE_BY4', 'DS3', 'FOUR_BY5',
                                          'LY6', 'LY10', 'LY11', 'DS4', 'SS4', 'YAP', 'FSP', 'SS5', 'DS5', 'PON', 'DS6',
                                          'SS6', 'L7B', 'MAG7', 'SS7', 'DS7', 'SS8', 'DS8', 'UJK', 'SS9', 'DS9', 'SS10',
                                          'DS10', 'DS11', 'DS12', 'DS13', 'DS14', 'DS15', 'MAN'])
    _bet_types_SGL = 'Single'
    _bet_types_DBL = 'Double'
    _bet_types_TBL = 'Treble'
    _bet_types_TRX = 'Trixie'
    _bet_types_PAT = 'Patent'
    _bet_types_ACC4 = 'Acca (4)'
    _bet_types_ACC5 = 'Acca (5)'
    _bet_types_ACC6 = 'Acca (6)'
    _bet_types_ACC7 = 'Acca (7)'
    _bet_types_ACC8 = 'Acca (8)'
    _bet_types_ACC9 = 'Acca (9)'
    _bet_types_AC10 = 'Acca (10)'
    _bet_types_AC11 = 'Acca (11)'
    _bet_types_AC12 = 'Acca (12)'
    _bet_types_AC13 = 'Acca (13)'
    _bet_types_AC14 = 'Acca (14)'
    _bet_types_AC15 = 'Acca (15)'
    _bet_types_YAN = 'Yankee'
    _bet_types_L15 = 'Lucky 15'
    _bet_types_L31 = 'Lucky 31'
    _bet_types_L63 = 'Lucky 63'
    _bet_types_CAN = 'Canadian'
    _bet_types_HNZ = 'Heinz'
    _bet_types_SHNZ = 'Super Heinz'
    _bet_types_GOL = 'Goliath'
    _bet_types_P512 = 'Fivefolds from 12'
    _bet_types_P513 = 'Fivefolds from 13'
    _bet_types_P514 = 'Fivefolds from 14'
    _bet_types_P413 = 'Fourfolds from 13'
    _bet_types_P414 = 'Fourfolds from 14'
    _bet_types_P415 = 'Fourfolds from 15'
    _bet_types_P416 = 'Fourfolds from 16'
    _bet_types_P417 = 'Fourfolds from 17'
    _bet_types_P712 = 'Sevenfolds from 12'
    _bet_types_P612 = 'Sixfolds from 12'
    _bet_types_P912 = 'Ninefolds from 12'
    _bet_types_P813 = 'Eightfolds from 13'
    _bet_types_P613 = 'Sixfolds from 13'
    _bet_types_P713 = 'Sevenfolds from 13'
    _bet_types_P1014 = 'Tenfolds from 14'
    _bet_types_P914 = 'Ninefolds from 14'
    _bet_types_P1115 = 'Elevenfolds from 15'
    _bet_types_P1216 = 'Twelvefolds from 16'
    _bet_types_P1317 = 'Thirteenfolds from 17'
    _bet_types_P1518 = 'Fifteenfolds from 18'
    _bet_types_P1619 = 'Sixteenfolds from 19'
    _bet_types_P1720 = 'Seventeenfolds from 20'
    _bet_types_P1821 = 'Eighteenfolds from 21'
    _bet_types_P1922 = 'Nineteenfolds from 22'
    _bet_types_P2023 = 'Twentyfolds from 23'
    _bet_types_P2124 = 'Twenty-Onefolds from 24'
    _bet_types_P2225 = 'Twenty-Twofolds from 25'
    _bet_types_DS2 = 'Double Stakes About (2)'
    _bet_types_SS2 = 'Single Stakes About (2)'
    _bet_types_SS3 = 'Single Stakes About (3)'
    _bet_types_ROB = 'Round Robin'
    _bet_types_FLG = 'Flag'
    _bet_types_SS11 = 'Single Stakes About (11)'
    _bet_types_SS12 = 'Single Stakes About (12)'
    _bet_types_SS13 = 'Single Stakes About (13)'
    _bet_types_P913 = 'Ninefolds from 13'
    _bet_types_SS14 = 'Single Stakes About (14)'
    _bet_types_SS15 = 'Single Stakes About (15)'
    _bet_types_AC16 = 'Acca (16)'
    _bet_types_AC17 = 'Acca (17)'
    _bet_types_AC18 = 'Acca (18)'
    _bet_types_AC19 = 'Acca (19)'
    _bet_types_AC20 = 'Acca (20)'
    _bet_types_AC21 = 'Acca (21)'
    _bet_types_AC22 = 'Acca (22)'
    _bet_types_AC23 = 'Acca (23)'
    _bet_types_AC24 = 'Acca (24)'
    _bet_types_AC25 = 'Acca (25)'
    _bet_types_3BY4 = '3 By 4'
    _bet_types_DS3 = 'Double Stakes About (3)'
    _bet_types_4BY5 = '4 By 5'
    _bet_types_LY6 = 'Lucky 6'
    _bet_types_LY10 = 'Lucky 10'
    _bet_types_LY11 = 'Lucky 11'
    _bet_types_DS4 = 'Double Stakes About (4)'
    _bet_types_SS4 = 'Single Stakes About (4)'
    _bet_types_YAP = 'Yap'
    _bet_types_FSP = 'Fivespot'
    _bet_types_SS5 = 'Single Stakes About (5)'
    _bet_types_DS5 = 'Double Stakes About (5)'
    _bet_types_PON = 'Pontoon'
    _bet_types_DS6 = 'Double Stakes About (6)'
    _bet_types_SS6 = 'Single Stakes About (6)'
    _bet_types_L7B = 'Lucky 7 Bingo'
    _bet_types_MAG7 = 'Magnificent 7'
    _bet_types_SS7 = 'Single Stakes About (7)'
    _bet_types_DS7 = 'Double Stakes About (7)'
    _bet_types_SS8 = 'Single Stakes About (8)'
    _bet_types_DS8 = 'Double Stakes About (8)'
    _bet_types_UJK = 'Union Jack'
    _bet_types_SS9 = 'Single Stakes About (9)'
    _bet_types_DS9 = 'Double Stakes About (9)'
    _bet_types_SS10 = 'Single Stakes About (10)'
    _bet_types_DS10 = 'Double Stakes About (10)'
    _bet_types_DS11 = 'Double Stakes About (11)'
    _bet_types_DS12 = 'Double Stakes About (12)'
    _bet_types_DS13 = 'Double Stakes About (13)'
    _bet_types_DS14 = 'Double Stakes About (14)'
    _bet_types_DS15 = 'Double Stakes About (15)'
    _bet_types_MAN = 'Single'
    BET_TYPES = _bet_types(SGL=_bet_types_SGL,
                           DBL=_bet_types_DBL,
                           TBL=_bet_types_TBL,
                           TRX=_bet_types_TRX,
                           PAT=_bet_types_PAT,
                           ACC4=_bet_types_ACC4,
                           ACC5=_bet_types_ACC5,
                           ACC6=_bet_types_ACC6,
                           ACC8=_bet_types_ACC8,
                           ACC9=_bet_types_ACC9,
                           AC10=_bet_types_AC10,
                           AC11=_bet_types_AC11,
                           AC12=_bet_types_AC12,
                           AC13=_bet_types_AC13,
                           AC14=_bet_types_AC14,
                           AC15=_bet_types_AC15,
                           YAN=_bet_types_YAN,
                           L15=_bet_types_L15,
                           L31=_bet_types_L31,
                           L63=_bet_types_L63,
                           CAN=_bet_types_CAN,
                           HNZ=_bet_types_HNZ,
                           SHNZ=_bet_types_SHNZ,
                           GOL=_bet_types_GOL,
                           P512=_bet_types_P512,
                           P513=_bet_types_P513,
                           P514=_bet_types_P514,
                           P413=_bet_types_P413,
                           P414=_bet_types_P414,
                           P415=_bet_types_P415,
                           P416=_bet_types_P416,
                           P417=_bet_types_P417,
                           P712=_bet_types_P712,
                           P612=_bet_types_P612,
                           P912=_bet_types_P912,
                           P813=_bet_types_P813,
                           P613=_bet_types_P613,
                           P713=_bet_types_P713,
                           P1014=_bet_types_P1014,
                           P914=_bet_types_P914,
                           P1115=_bet_types_P1115,
                           P1216=_bet_types_P1216,
                           P1317=_bet_types_P1317,
                           P1518=_bet_types_P1518,
                           P1619=_bet_types_P1619,
                           P1720=_bet_types_P1720,
                           P1821=_bet_types_P1821,
                           P1922=_bet_types_P1922,
                           P2023=_bet_types_P2023,
                           P2124=_bet_types_P2124,
                           P2225=_bet_types_P2225,
                           DS2=_bet_types_DS2,
                           SS2=_bet_types_SS2,
                           SS3=_bet_types_SS3,
                           ROB=_bet_types_ROB,
                           FLG=_bet_types_FLG,
                           SS11=_bet_types_SS11,
                           SS12=_bet_types_SS12,
                           SS13=_bet_types_SS13,
                           P913=_bet_types_P913,
                           SS14=_bet_types_SS14,
                           SS15=_bet_types_SS15,
                           AC16=_bet_types_AC16,
                           AC17=_bet_types_AC17,
                           AC18=_bet_types_AC18,
                           AC19=_bet_types_AC19,
                           AC20=_bet_types_AC20,
                           AC21=_bet_types_AC21,
                           AC22=_bet_types_AC22,
                           AC23=_bet_types_AC23,
                           AC24=_bet_types_AC24,
                           AC25=_bet_types_AC25,
                           THREE_BY4=_bet_types_3BY4,
                           DS3=_bet_types_DS3,
                           FOUR_BY5=_bet_types_4BY5,
                           LY6=_bet_types_LY6,
                           LY10=_bet_types_LY10,
                           LY11=_bet_types_LY11,
                           DS4=_bet_types_DS4,
                           SS4=_bet_types_SS4,
                           YAP=_bet_types_YAP,
                           FSP=_bet_types_FSP,
                           SS5=_bet_types_SS5,
                           DS5=_bet_types_DS5,
                           PON=_bet_types_PON,
                           DS6=_bet_types_DS6,
                           SS6=_bet_types_SS6,
                           L7B=_bet_types_L7B,
                           MAG7=_bet_types_MAG7,
                           SS7=_bet_types_SS7,
                           DS7=_bet_types_DS7,
                           SS8=_bet_types_SS8,
                           DS8=_bet_types_DS8,
                           UJK=_bet_types_UJK,
                           SS9=_bet_types_SS9,
                           DS9=_bet_types_DS9,
                           SS10=_bet_types_SS10,
                           DS10=_bet_types_DS10,
                           DS11=_bet_types_DS11,
                           DS12=_bet_types_DS12,
                           DS13=_bet_types_DS13,
                           DS14=_bet_types_DS14,
                           DS15=_bet_types_DS15,
                           MAN=_bet_types_MAN)

    _what_link = namedtuple('what_link', ['part1', 'part2'])
    _what_link_part1 = 'What\'s '
    _what_link_part2 = 'Cashout?'
    WHAT_LINK = _what_link(part1=_what_link_part1, part2=_what_link_part2)

    _partial_cashout_button = namedtuple('partial_cashout_button', ['partial', 'cashout'])
    _partial_cashout_button_partial = 'Partial'
    _partial_cashout_button_cashout = 'Cashout'
    PARTIAL_CASHOUT_BUTTON = _partial_cashout_button(partial=_partial_cashout_button_partial,
                                                     cashout=_partial_cashout_button_cashout)

    FOOTBALL_JACKPOT = 'Football Jackpot'
    TOTEPOOL = 'Totepool'
    SINGLE = 'Single'

    INCORRECT_DATE_RANGE = 'Please select a valid time range'
    MORE_THAN_THREE_MONTH = 'We can only display results for the last 3 months. For more data send an email to <a href=\'mailto:support@coral.co.uk\'>support@coral.co.uk</a>'
    MORE_THAN_THREE_MONTH_RANGE = 'Specified date range is more than 3 months.'
    OVER_LIMIT_PERIOD_ERROR_MESSAGE = 'If you require account or gambling history over longer periods please <br> <a href=\'%1\' target=\'_blank\' class=\'underlined\'>contact us</a>'

    ACCOUNT_HISTORY_TABS_TITLE = 'Account History'
    _account_history_tabs = namedtuple('account_history_tabs', ['transactions', 'gaming', 'settled_bets'])
    _account_history_tabs_transactions = 'Transactions'
    _account_history_tabs_gaming = 'Gaming History'
    _account_history_tabs_settled_bets = 'Settled Bets'
    ACCOUNT_HISTORY_TABS = _account_history_tabs(transactions=_account_history_tabs_transactions,
                                                 gaming=_account_history_tabs_gaming,
                                                 settled_bets=_account_history_tabs_settled_bets)

    EMA_ERROR = 'Sorry, editing was unsuccessful, please try again.'
    CANCELLATION_SUCCESS = 'Your withdrawal has been successfully canceled!'
    CANCEL_WITHDRAW_MSG = 'Are you sure you wish to cancel the withdrawal?'
    CANCEL_WITHDRAW_TITLE = 'Cancel Withdrawal'
    WITHDRAW = 'Withdraw Funds'
    CONFIRM = 'Yes, cancel it!'
    DEPOSIT = 'Deposit'
    APPROVED = 'Approved'
    DECLINED = 'Declined'
    PENDING = 'Pending'
    WAITING = 'Waiting'
    DATE = 'Date/Time'
    GAME = 'Game'
    AMOUNT = 'Amount'
    WAGER = 'wager'
    NO_GAME_DATA = 'You have no gaming history.'
    LAST_WEEK = 'Showing all Transactions for the last 7 days.'
    CANCEL = 'Cancel'
    REFRESH = 'Refresh'
    EMPTY_HISTORY = 'You have no transaction history.'
    TRANSACTION_HISTORY_ERROR_MESSAGE = 'We are sorry. Transaction History service is currently unavailable, please try again later.'
    CONTACT_INFO = 'To download this information please visit <a href=\'http://www.coral.co.uk/\' target=\'_blank\'>Coral.co.uk</a> desktop site.'
    SUMMARY = 'Summary'
    T_STAKES = 'T. Stakes'
    T_RETURNS = 'T. Returns'
    TOTAL_STAKES = 'Total Stakes:'
    TOTAL_RETURNS = 'Total Returns:'
    RETURNS = 'Returns:'
    PROFIT_LOSS = 'Profit/Loss'
    ALL = 'All'
    SHOW = 'Show'
    TOTAL_NUMBER_OF_BETS = 'No. of bets'
    INVALID_RANGE_ERROR_MESSAGE = 'Please select a valid date range'
    NO_OPEN_BETS = 'You currently have no open bets.'
    NO_LOTTO_BETS = 'You currently have no lotto bets.'
    GOAL = 'GOAL'
    CORRECTION = 'CORRECTION'
    CRICKET_SECOND_INNING = '2nd '
    REGULAR = 'Regular'
    SPORTS = 'Sports'
    SB = 'Sports'
    POOL = 'Pools'
    LOTTO = 'Lotto'
    DELIMITER = '|'
    ALL_BETS_GAMES = 'All Betting & Gaming'
    DIGITAL_SPORT = 'Player Bets'
    NO_HISTORY_INFO = 'There are no settled bets to display.'
    LAST_TWO_DAYS = 'Last 2 days'
    BET_RECEIPT = 'Bet Receipt:'
    YOU_WON = 'You Won:'
    RULE_FOUR_MESSAGE_FIRST_PART = 'A Rule 4 Deduction of '
    RULE_FOUR_MESSAGE_SECOND_PART = ' has been added'
    RULE_FOUR_MESSAGE_THIRD_PART = 'More Info'
    NET_DEPOSITS_DIALOG_HEADER = 'WHAT ARE NET DEPOSITS?'
    RTS_WARNING_MESSAGE = 'Regular (Sports & Gaming), Lotto and Pools bets are included in the table above'
    SETTLED_BETA = 'Settled Bets'
    TODAY = 'Today'
    TOTE_MARKET_TITLE = 'Tote {pool_type} Pool'
    TOTE_RACE_TITLE = 'Race {race_number}'
    NET_DEPOSITS_DIALOG_MESSAGE = 'Net deposits are calculated by taking the sum of approved deposits (including any deposit corrections) and deducting approved withdrawals (including any withdrawal corrections)'
    BALANCES = 'BALANCES'
    DEPOSITS = 'DEPOSITS'
    WITHDRAWALS = 'Withdrawals'
    NET_DEPOSITS = 'Net Deposits'
    START_BETTING = 'Start betting'
    PROFIT_LOSS_LINK = 'See Profit / Loss'
    CASHOUT_NOT_AVAILABLE = 'CASH OUT NOT AVAILABLE'

    CASHOUT_PLEASE_LOGIN_MESSAGE = 'Please log in to see your cash out bets.'
    CASHOUT_SINGLE_BET_SELECTION_SUSPENDED = 'Your selection is suspended'
    CASHOUT_MULTIPLE_BET_SELECTION_SUSPENDED = 'At least one of your selections is suspended'
    EXPECTED_MY_BETS_EACH_WAY_FORMAT = '{ew_fac_num}/{ew_fac_den} odds - places {ew_places}'
    SETTLED_BETS_PLEASE_LOGIN_MESSAGE = 'Please log in to see your settled bets.'
    OPEN_BETS_PLEASE_LOGIN_MESSAGE = 'Please log in to see your open bets.'
    SORTING_BUTTON_TYPES_OPEN_BETS = ['REGULAR', 'LOTTO', 'PLAYER BETS', 'POOLS']
    SORTING_BUTTON_TYPES_SETTLED_BETS = ['SPORTS', 'LOTTO', 'POOLS']

    # My Bets tabs for desktop widget
    CASH_OUT_TAB_NAME = 'CASH OUT'
    OPEN_BETS_TAB_NAME = 'OPEN'
    SETTLED_BETS_TAB_NAME = 'SETTLED'
    IN_SHOP_BETS_TAB_NAME = 'SHOP BETS'
    BET_SLIP_TAB_NAME = 'BET SLIP'

    MY_BETS_SINGLE_STAKE_TITLE = 'SINGLE'
    MY_BETS_DOUBLE_STAKE_TITLE = 'DOUBLE'
    MY_BETS_TREBLE_STAKE_TITLE = 'TREBLE'
    MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE = 'BUILD YOUR BET'
    SINGLE_FORECAST_MY_BETS_NAME = 'SINGLE - FORECAST'
    SINGLE_REVERSE_FORECAST_MY_BETS_NAME = 'SINGLE - REVERSE FORECAST'
    SINGLE_COMBINATION_FORECAST_MY_BETS_NAME = 'SINGLE - COMBINATION FORECAST'
    SINGLE_TRICAST_MY_BETS_NAME = 'SINGLE - TRICAST'
    SINGLE_COMBINATION_TRICAST_MY_BETS_NAME = 'SINGLE - COMBINATION TRICAST'
    FIVE_A_SIDE_BET_TYPE = '5-A-SIDE'

    # open bets
    LOTTO_TAB_NAME = 'LOTTO'
    POOLS_TAB_NAME = 'POOLS'

    SINGLE_EACH_WAY_BET_TYPE = 'SINGLE (EACH WAY)'
    MY_BETS_TAB_NAMES = ['CASH OUT', 'OPEN BETS', 'SETTLED BETS', 'SHOP BETS']
