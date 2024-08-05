from voltron.environments.constants.base.yourcall import Yourcall


class LadbrokesYourcall(Yourcall):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/yourCall.lang.ts
    """
    BUILD_YOUR_BET = 'Bet Builder'
    DASHBOARD_TITLE = 'Bet builder'.upper()
    YOURCALL_TAB_DIALOG_TITLE = 'New Bet Builder with Cashout'
    NO_LEAGUES = 'Sorry no Bet Builder events are available at this time'
    PATH_BUILD_YOUR_BET = 'bet-builder'

    OPEN = Yourcall.OPEN.upper()
    CLOSE = Yourcall.CLOSE.upper()
    SELECT_PLAYER = Yourcall.SELECT_PLAYER.upper()
    SELECT_STATISTIC = Yourcall.SELECT_STATISTIC.upper()
