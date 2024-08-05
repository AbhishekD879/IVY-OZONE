from voltron.environments.constants.base.betslip import Betslip


class CoralBetslip(Betslip):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/bs.lang.ts
    """
    MULTIPLES = Betslip.MULTIPLES.upper()
    VOUCHER_FORM = Betslip.VOUCHER_FORM.upper()
    SHOW_CASH_HISTORY = Betslip.SHOW_CASH_HISTORY.upper()
    HIDE_CASH_HISTORY = Betslip.HIDE_CASH_HISTORY.upper()
    ERROR = Betslip.ERROR.upper()
    CLEAR_BETSLIP_CANCEL = Betslip.CLEAR_BETSLIP_CANCEL.upper()
    CLEAR_BETSLIP_CONTINUE = Betslip.CLEAR_BETSLIP_CONTINUE.upper()
    BETSLIP_SINGLES_NAME = 'Single'
    LOGIN_AND_BET_BUTTON_CAPTION = 'LOGIN & PLACE BET'
    LOGIN_AND_PLACE_BET_QUICK_BET = LOGIN_AND_BET_BUTTON_CAPTION
    ACCA_INSURANCE_QUALIFY_MSG = 'Your selections qualify for Acca Insurance'
