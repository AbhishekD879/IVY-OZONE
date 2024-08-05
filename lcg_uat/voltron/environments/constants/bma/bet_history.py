
from voltron.environments.constants.base.bet_history import BetHistory


class CoralBetHistory(BetHistory):
    """
    src/app/lazy-modules/locale/translations/en-US/bethistory.lang.ts
    """
    TAB_TITLE = BetHistory.TAB_TITLE.upper()
    CASHOUT = BetHistory.CASHOUT.upper()
    START_BETTING = BetHistory.START_BETTING.upper()
    mybets_tab = ['CASH OUT', 'OPEN BETS', 'SETTLED BETS', 'SHOP BETS']

    FIVE_A_SIDE_BET_TYPE_NAME = '5-A-Side'
