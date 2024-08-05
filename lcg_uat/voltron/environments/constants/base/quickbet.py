from collections import namedtuple


class Quickbet(object):
    """
    src/app/lazy-modules/locale/translations/en-US/quickbet.lang.ts
    """
    HANDICAP_CHANGED_VALUE = 'Handicap changed from {old} To {new}'
    QUICKBET_TITLE = 'Quick Bet'
    QUICK_DEPOSIT_TITLE = 'Quick Deposit'
    ODDS_LABEL = 'Odds'
    STAKE_LABEL = 'Total Stake'
    TOTAL_STAKE = 'Stake: '
    DEFAULT_AMOUNT_VALUE = 'Stake'
    EACH_WAY_LABEL = 'E/W'
    EST_RETURNS = 'Estimated Returns'
    IS_SP = 'SP'
    SINGLE_DISABLED = 'Your %1 has been suspended'
    PRICE_IS_CHANGED = 'Price change from {old} to {new}'
    REBOOST_PRICE_CHANGED = 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price'
    QUICKBET_DEPOSIT_NOTIFICATION = 'Please deposit a min of £{0:.2f} to continue placing your bet'
    INSUFFICIENT_FUNDS = 'Insufficient funds to place the bet.'
    EVENT_NOT_FOUND = 'Selection is no longer available'
    DEPOSIT_AND_PLACEBET_SUCCESS_MESSAGE = 'Your deposit was successful and your bet has been placed.'

    _buttons = namedtuple('buttons', ['place_bet', 'accept_place_bet', 'accept_place_bet_deposit', 'login_place_bet',
                                      'add_to_betslip', 'deposit_placebet', 'reuse_selection', 'make_quick_deposit',
                                      'done', 'back', 'deposit'])
    _buttons_place_bet = 'Place bet'
    _buttons_accept_place_bet = 'Accept & Place bet'
    _buttons_accept_place_bet_deposit = 'Accept (Deposit & Place Bet)'
    _buttons_login_place_bet = 'Login & Place bet'
    _buttons_add_to_betslip = 'ADD TO BETSLIP'
    _buttons_deposit_placebet = 'Deposit & Place bet'
    _buttons_reuse_selection = 'Reuse selection'
    _buttons_make_quick_deposit = 'Make a deposit'
    _buttons_done = 'Done'
    _buttons_back = 'Back'
    _buttons_deposit = 'Deposit'
    BUTTONS = _buttons(place_bet=_buttons_place_bet,
                       accept_place_bet=_buttons_accept_place_bet,
                       accept_place_bet_deposit=_buttons_accept_place_bet_deposit,
                       login_place_bet=_buttons_login_place_bet,
                       add_to_betslip=_buttons_add_to_betslip,
                       deposit_placebet=_buttons_deposit_placebet,
                       reuse_selection=_buttons_reuse_selection,
                       make_quick_deposit=_buttons_make_quick_deposit,
                       done=_buttons_done,
                       back=_buttons_back,
                       deposit=_buttons_deposit)

    ODDS = 'Odds '
    BET_ID = 'Bet ID: '
    UNIT_STAKE = 'Unit Stake '
    EWE = 'E/W'
    HANDICAP_ERROR = 'Line change from {old} to {new}'
    FREE_BET_STAKE = 'Free Bet Amount: '
    ESTIMATED_RESULTS = 'Est. Returns: '
    BET_RECEIPT_TITLE = 'bet receipt'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'
    FS = 'First Goal Scorecast'
    LS = 'Last Goal Scorecast'

    _bet_placement_errors = namedtuple('bet_placement_errors',
                                       ['selection_suspended', 'event_suspended', 'event_started', 'market_suspended',
                                        'outcome_suspended', 'price_changed', 'handicap_changed',
                                        'invalid_bet_document_id',
                                        'live_price_unavailable', 'insufficient_funds', 'other_bets_failed',
                                        'stake_mismatch', 'stake_too_low', 'stake_low', 'selection_removed',
                                        'odds_boost_not_allowed', 'place_invalid_access_token', 'stake_too_high',
                                        'stake_high', 'bad_price', 'invalid_price_value', 'bad_freebet_token',
                                        'account_not_active',
                                        'account_suspended', 'invalid_scorecast', 'eachway_terms_change',
                                        'eachway_price_change',
                                        'eachway_places_change', 'win_place_terms_changed', 'each_way_terms_changed',
                                        'bet_rejected', 'private_market', 'default_placebet_error',
                                        'pt_err_disable_gaming', 'timeout_error'])
    _bet_placement_errors_selection_suspended = 'Your event has been suspended'
    _bet_placement_errors_event_suspended = 'Your event has been suspended'
    _bet_placement_errors_event_started = 'Event Has Already Started.'
    _bet_placement_errors_market_suspended = 'Your market has been suspended'
    _bet_placement_errors_outcome_suspended = 'Your selection has been suspended'
    _bet_placement_errors_price_changed = 'Price Change from {old} to {new}'
    _bet_placement_errors_handicap_changed = 'Line change from {old} to {new}'
    _bet_placement_errors_invalid_bet_document_id = 'Invalid bet document ID.'
    _bet_placement_errors_live_price_unavailable = 'Live price is unavailable.'
    _bet_placement_errors_insufficient_funds = 'Insufficient funds to place the bet.'
    _bet_placement_errors_other_bets_failed = 'Error with bet in request.'
    _bet_placement_errors_stake_mismatch = 'Stake mismatch.'
    _bet_placement_errors_stake_too_low = 'The stake specified in the bet is too low'
    _bet_placement_errors_stake_low = 'Minimum stake is £{0:.2f}'
    _bet_placement_errors_selection_removed = 'Selection %1 is no longer available'
    _bet_placement_errors_odds_boost_not_allowed = 'Sorry, one of the selections cannot be boosted, please remove the selection and try again.'
    _bet_placement_errors_place_invalid_access_token = 'This Offer Applies To One Selection Only, Please Check & Try Again.'
    _bet_placement_errors_stake_too_high = 'The stake specified in the bet is too high'
    _bet_placement_errors_stake_high = 'Maximum stake is £{0:.2f}'
    _bet_placement_errors_bad_price = 'The bet contains invalid price value'
    _bet_placement_errors_invalid_price_value = 'The bet contains invalid price value'
    _bet_placement_errors_bad_freebet_token = 'The freebet token being redeemed is invalid or not applicable'
    _bet_placement_errors_account_not_active = 'The request contains bet for a customer inactive account'
    _bet_placement_errors_account_suspended = 'Your account is suspended'
    _bet_placement_errors_invalid_scorecast = 'The scorecast bet in the request is invalid'
    _bet_placement_errors_eachway_terms_change = 'Eachway terms change'
    _bet_placement_errors_eachway_price_change = 'The request contains bets for which each way price has changed'
    _bet_placement_errors_eachway_places_change = 'The request contains bets for which each way places have changed'
    _bet_placement_errors_win_place_terms_changed = 'Win place terms changed'
    _bet_placement_errors_each_way_terms_changed = 'Eachway terms change'
    _bet_placement_errors_bet_rejected = 'Bet rejected'
    _bet_placement_errors_private_market = 'Sorry, your private market is currently unavailable'
    _bet_placement_errors_default_placebet_error = 'Your bet has not been accepted. Please try again.'
    _bet_placement_errors_pt_err_disable_gaming = 'Your account is suspended'
    _bet_placement_errors_timeout_error = 'Sorry, there may have been a problem placing your bet. To confirm if your bet was placed please check your <a class="deposit-external-link" href="/open-bets">Open bets</a>.'
    BET_PLACEMENT_ERRORS = _bet_placement_errors(selection_suspended=_bet_placement_errors_selection_suspended,
                                                 event_suspended=_bet_placement_errors_event_suspended,
                                                 event_started=_bet_placement_errors_event_started,
                                                 market_suspended=_bet_placement_errors_market_suspended,
                                                 outcome_suspended=_bet_placement_errors_outcome_suspended,
                                                 price_changed=_bet_placement_errors_price_changed,
                                                 handicap_changed=_bet_placement_errors_handicap_changed,
                                                 invalid_bet_document_id=_bet_placement_errors_invalid_bet_document_id,
                                                 live_price_unavailable=_bet_placement_errors_live_price_unavailable,
                                                 insufficient_funds=_bet_placement_errors_insufficient_funds,
                                                 other_bets_failed=_bet_placement_errors_other_bets_failed,
                                                 stake_mismatch=_bet_placement_errors_stake_mismatch,
                                                 stake_too_low=_bet_placement_errors_stake_too_low,
                                                 stake_low=_bet_placement_errors_stake_low,
                                                 selection_removed=_bet_placement_errors_selection_removed,
                                                 odds_boost_not_allowed=_bet_placement_errors_odds_boost_not_allowed,
                                                 place_invalid_access_token=_bet_placement_errors_place_invalid_access_token,
                                                 stake_too_high=_bet_placement_errors_stake_too_high,
                                                 stake_high=_bet_placement_errors_stake_high,
                                                 bad_price=_bet_placement_errors_bad_price,
                                                 invalid_price_value=_bet_placement_errors_invalid_price_value,
                                                 bad_freebet_token=_bet_placement_errors_bad_freebet_token,
                                                 account_not_active=_bet_placement_errors_account_not_active,
                                                 account_suspended=_bet_placement_errors_account_suspended,
                                                 invalid_scorecast=_bet_placement_errors_invalid_scorecast,
                                                 eachway_terms_change=_bet_placement_errors_eachway_terms_change,
                                                 eachway_price_change=_bet_placement_errors_eachway_price_change,
                                                 eachway_places_change=_bet_placement_errors_eachway_places_change,
                                                 win_place_terms_changed=_bet_placement_errors_win_place_terms_changed,
                                                 each_way_terms_changed=_bet_placement_errors_each_way_terms_changed,
                                                 bet_rejected=_bet_placement_errors_bet_rejected,
                                                 private_market=_bet_placement_errors_private_market,
                                                 default_placebet_error=_bet_placement_errors_default_placebet_error,
                                                 pt_err_disable_gaming=_bet_placement_errors_pt_err_disable_gaming,
                                                 timeout_error=_bet_placement_errors_timeout_error)

    YOUR_CALL_BETRECEIPT = 'Bet Receipt'
    ODDS_BOOST_EXPIRED_OR_REDEEMED = 'Your Odds Boost has been expired/redeemed.'
    WIN_ALERTS = 'Win Alerts'
    ODDS_A_PLACES = 'Each Way Odds {num}/{den} Places {arr}'
    LINES_PER_STAKE = '{lines} Lines at {stake} per line'
    MAX_BET_MESSAGE = 'Sorry, the maximum stake for this bet is £{0:.2f}'
    BET_NOT_PERMITTED = 'Sorry, you are not allowed to place bet on this selection.'
