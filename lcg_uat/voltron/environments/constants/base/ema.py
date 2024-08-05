from collections import namedtuple


class EMA(object):
    """
    src/app/lazy-modules/locale/translations/en-US/ema.lang.ts
    """
    EDIT_MY_BET = 'Edit My Bet'
    CANCEL = 'Cancel Editing'
    LEG_REMOVED = 'Removed'
    UNDO_LEG_REMOVE = 'Undo'
    CONFIRM_EDIT = 'Confirm'
    CONFIRM_SUSPENDED = 'Susp Confirm'
    EDIT_WARNING = 'Edit My Acca uses the cash out value of this bet and the latest odds of each selection'
    SUSPENSION_WARNING = 'Some of your selections are suspended'
    NO_ACTIVE_WARNING = 'Your Acca is no longer active'

    _edit_success = namedtuple('edit_success', ['caption', 'text'])
    _edit_success_caption = 'Acca Edited Successfully'
    _edit_success_text = 'Your new estimate return is: %1%2'
    EDIT_SUCCESS = _edit_success(caption=_edit_success_caption,
                                 text=_edit_success_text)

    _edit_cancel = namedtuple('edit_cancel', ['caption', 'text'])
    _edit_cancel_caption = 'Do you want to cancel editing?'
    _edit_cancel_text = 'Moving away from this page will cancel changes already made to this bet! Are you sure you want to cancel?'
    EDIT_CANCEL = _edit_cancel(caption=_edit_cancel_caption,
                               text=_edit_cancel_text)

    _history = namedtuple('history', ['original_bet', 'edited_bet', 'show_history', 'acca_history'])
    _history_original_bet = 'Original Bet'
    _history_edited_bet = 'Edited Bet'
    _history_show_history = 'Show Edit History'
    _history_acca_history = 'Edit Acca History'
    HISTORY = _history(original_bet=_history_edited_bet,
                       edited_bet=_history_edited_bet,
                       show_history=_history_show_history,
                       acca_history=_history_acca_history)

    _cashout_history = namedtuple('cashout_history', ['header', 'stake_used', 'cashed_out', 'cashout_used'])
    _cashout_history_header = 'Cash out history:'
    _cashout_history_stake_used = 'Stake used:'
    _cashout_history_cashed_out = 'Cashed out:'
    _cashout_history_cashout_used = '*£{0:.2f} was used to edit your bet'
    CASHOUT_HISTORY = _cashout_history(header=_cashout_history_header,
                                       stake_used=_cashout_history_stake_used,
                                       cashed_out=_cashout_history_cashed_out,
                                       cashout_used=_cashout_history_cashout_used)

    _terms = namedtuple('terms', ['in_play_score_information', 'retail', 'cashout', 'ema'])
    _terms_in_play_score_information = 'In-Play score information is for guidance only and can be subject to a delay'
    _terms_retail = 'See Retail Bets on Shop Bet Tracker'
    _terms_cashout = 'Cash Out Terms & Conditions'
    _terms_ema = 'Edit My Acca Terms & Conditions'
    TERMS = _terms(in_play_score_information=_terms_in_play_score_information,
                   retail=_terms_retail,
                   cashout=_terms_cashout,
                   ema=_terms_ema)
