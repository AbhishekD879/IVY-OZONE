from voltron.environments.constants.base.uk_tote import UKTote


class LadbrokesUKTote(UKTote):
    """
    src/app/lazy-modules/locale/translations/en-US/uktote.lang.ts
    """
    TOTEPOOL = UKTote.TOTEPOOL.upper()
    LEG_1 = 'Leg 1'

    UK_TOTE_TABS = UKTote._uk_tote_tabs(win='Win', place='Place', exacta='Exacta', trifecta='Trifecta', quadpot='Quadpot',
                                        placepot='Placepot', jackpot='Jackpot', scoop6='Scoop6')
