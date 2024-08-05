from collections import namedtuple


class UKTote(object):
    """
    src/app/lazy-modules/locale/translations/en-US/uktote.lang.ts
    """
    TOTEPOOL = 'Totepool'
    WHAT_IS = 'What is %1?'
    POOL_SIZE_LABEL = 'Current pool:'
    CLEAR_SELECTION = 'Clear Selection'
    CLEAR_SELECTIONS = 'Clear Selections'
    BETS = 'Bets'
    BET = 'Bet'
    ADD_TO_BETSLIP = 'Add to betslip'
    TOTAL_STAKE = 'Total Stake'
    NO_LINES = 'No. Lines'
    STAKE_PER_LINE = 'Stake per line'
    CLOSE = 'Close'
    OPEN = 'Open'
    NON_RUNNER = 'N/R'
    ADD_TO_SLIP = 'Add to slip'
    NO_TOTE_EVENT = 'Event is currently unavailable'
    GUIDE = 'Guide'

    UWINUPLC = 'Win/Place'
    UWIN = 'Win'
    UPLC = 'Place'
    UEXA = 'Exacta'
    UTRI = 'Trifecta'
    UJKP = 'Jackpot'
    UPLP = 'Placepot'
    UQDP = 'Quadpot'
    USC6 = 'Scoop6'
    USC7 = 'Super7'
    USW = 'Swinger'
    UTD = 'Double'
    UTT = 'Treble'
    WN = 'Win'
    PL = 'Place'
    EX = 'Exacta'
    TR = 'Trifecta'
    P3 = 'Placepot'
    P6 = 'Quadpot'

    MIN_STAKE_PER_LINE = 'Stake must be greater than {value}'
    MAX_STAKE_PER_LINE = 'Stake must be lower than {value}'
    MIN_TOTAL_STAKE = 'Total stake must be greater than {value}'
    MAX_TOTAL_STAKE = 'Total stake must be lower than {value}'
    STAKE_INCREMENT_FACTOR = 'Stake must be in increments of {value}'

    STRAIGHT_EXACTA_BET = '1 EXACTA BET'
    REVERSE_EXACTA_BET = '1 REVERSE EXACTA BET'
    COMBINATION_EXACTA_BET = '{number} COMBINATION EXACTA BETS'
    STRAIGHT_TRIFECTA_BET = '1 TRIFECTA BET'
    COMBINATION_TRIFECTA_BET = '{number} COMBINATION TRIFECTA BETS'
    ONE_SELECTION_WIN_BET = '1 Win Selection'
    MULTIPLE_SELECTIONS_WIN_BET = '{number} Win Selections'
    ONE_SELECTION_PLACE_BET = '1 Place Selection'
    MULTIPLE_SELECTIONS_PLACE_BET = '{number} Place Selections'
    ADD_SELECTION = 'Please add another selection'
    LEG_1 = 'LEG 1'

    _uk_tote_tabs = namedtuple('UK_TOTE_TABS', ('win', 'place', 'exacta', 'trifecta', 'quadpot', 'placepot', 'jackpot', 'scoop6'))
    UK_TOTE_TABS = _uk_tote_tabs(win='WIN', place='PLACE', exacta='EXACTA', trifecta='TRIFECTA', quadpot='QUADPOT',
                                 placepot='PLACEPOT', jackpot='JACKPOT', scoop6='SCOOP6')
