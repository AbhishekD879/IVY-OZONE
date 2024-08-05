from voltron.environments.constants.base.bet_history import BetHistory


class LadbrokesBetHistory(BetHistory):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/bethistory.lang.ts
    """
    TOTAL_RETURN = 'Potential Returns:'
    NEW_TOTAL_RETURN = 'New Potential Returns:'
    NO_CASHOUT_BETS = 'You currently have no bets available for cash out.'
    START_BETTING = 'Go betting'.upper()
    CASHOUT = BetHistory.CASHOUT.upper()

    CASHOUT_PLEASE_LOGIN_MESSAGE = 'Your cash out bets will appear here, \n Please login to view.'
    SETTLED_BETS_PLEASE_LOGIN_MESSAGE = 'Your settled bets will appear here, \n Please login to view.'
    OPEN_BETS_PLEASE_LOGIN_MESSAGE = 'Your open bets will appear here, \n Please login to view.'
    SORTING_BUTTON_TYPES_OPEN_BETS = ['Sports', 'Lotto', 'Pools']
    SORTING_BUTTON_TYPES_SETTLED_BETS = ['Sports', 'Lotto', 'Pools']
    mybets_tab = ['CASH OUT', 'OPEN', 'SETTLED']

    MY_BETS_SINGLE_BET_BUILDER_STAKE_TITLE = 'BET BUILDER'

    # Open bets
    LOTTO_TAB_NAME = 'Lotto'
    POOLS_TAB_NAME = 'Pools'

    FIVE_A_SIDE_BET_TYPE_NAME = '5-A-Side'
