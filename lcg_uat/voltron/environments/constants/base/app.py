from collections import namedtuple


class App(object):
    """
    src/app/lazy-modules/locale/translations/en-US/app.lang.ts
    """
    CASHOUT = 'cash out'
    DEPOSIT = 'Deposit'
    WATCH_LIVE = 'Watch Live'
    WATCH = 'Watch'
    NEW = 'New'
    LIVE = 'Live'
    DOWNLOAD = 'Download'
    SIGN_IN = 'Log In'
    LOBBY = 'Sports'
    ERROR_MESSAGE = 'An internal error occurred within the back end system. Contact Coral for more information.'
    SERVER_ERROR = 'Server is unavailable at the moment, please try again later.'
    ERROR_SERVICE_DEPARTMENT_MESSAGE = 'If this problem persists, contact our '
    ERROR_SERVICE_DEPARTMENT_LINK = 'Customer Service Department'
    REQUEST_ERROR_MESSAGE = 'Oops! We are having trouble loading this page. Please check your connection'
    TRY_AGAIN = 'Try Again'
    MORE_INFO = 'More Info'
    ACCEPT = 'Accept'
    PHONE_ROTATE = 'Please rotate your screen back in Portrait Mode. Please ensure you have \'screen rotate\' option active.'
    ACCEPT_AND_CLOSE = 'Accept & close'
    ERROR = 'Error'
    ERROR_TITLE_503 = '503 Error - Services Unavailable'
    ERROR_MESSAGE_503 = 'Please contact your support team for assistance'
    ERROR_TITLE_404 = '404 Error - The page you are looking for no longer exists'
    ERROR_MESSAGE_404 = 'Perhaps you can return back to the site’s homepage and see if you can find what you are looking for'
    ERROR_POPUP_MESSAGE = 'If this problem persists, contact our Customer Service Department'
    ERROR_POPUP_LINK = 'Contact Customer Services'
    LOGIN_TO_SEE_PAGE_MESSAGE = 'Please log in to see your {page}.'
    INTERNET_ERROR = 'No internet connection'
    CONNECTION_LOST_MESSAGE = 'You are currently experiencing issues connecting to the internet. ' \
                              'Please check your internet connection and try again.'

    _betslip_tabs = namedtuple('betslip_tabs', ['betslip', 'cashout', 'openbets', 'bet_receipt', 'tote_bet_receipt',
                                                'bet_history', 'in_shop_bets'])
    _betslip_tabs_betslip = 'Bet Slip'
    _betslip_tabs_cashout = 'Cash Out'
    _betslip_tabs_openbets = 'Open Bets'
    _betslip_tabs_bet_receipt = 'Bet Receipt'
    _betslip_tabs_tote_bet_receipt = 'Tote Bet Receipt'
    _betslip_tabs_bet_history = 'Settled Bets'
    _betslip_tabs_in_shop_bets = 'Shop Bets'
    BETSLIP_TABS = _betslip_tabs(betslip=_betslip_tabs_betslip,
                                 cashout=_betslip_tabs_cashout,
                                 openbets=_betslip_tabs_openbets,
                                 bet_receipt=_betslip_tabs_bet_receipt,
                                 tote_bet_receipt=_betslip_tabs_tote_bet_receipt,
                                 bet_history=_betslip_tabs_bet_history,
                                 in_shop_bets=_betslip_tabs_in_shop_bets)
    CHANGE = 'Change'

    _tooltip = namedtuple('tooltip', ['win_alerts', 'edit_my_acca', 'odds_boost_unavailable'])
    _tooltip_win_alerts = 'Turn on Win alerts and we will alert you when you win'
    _tooltip_edit_my_acca = 'Now you can remove selections from your acca to keep your bet alive'
    _tooltip_odds_boost_unavailable = 'Odds Boost is unavailable for this section'
    TOOLTIP = _tooltip(win_alerts=_tooltip_win_alerts,
                       edit_my_acca=_tooltip_edit_my_acca,
                       odds_boost_unavailable=_tooltip_odds_boost_unavailable)
    PENDING_VERIFICATION_DIALOG_TITLE = 'VERIFYING YOUR DETAILS'
