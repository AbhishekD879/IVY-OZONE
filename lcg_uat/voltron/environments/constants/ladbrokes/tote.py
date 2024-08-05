from collections import namedtuple

from voltron.environments.constants.base.tote import Tote


class LadbrokesTote(Tote):
    """
    src/platforms/ladbrokesMobile/lazy-modules/locale/translations/en-US/tt.lang.ts
    """
    BETTING_RULES_MSG = 'All bets are accepted with the <a href="https://help.ladbrokes.com/s/"">Ladbrokes Betting Rules</a> as published on this site.'

    _tote_tabs = namedtuple('tote_tabs', ('win', 'place', 'exacta', 'trifecta', 'quadpot', 'placepot', 'jackpot'))
    TOTE_TABS = _tote_tabs(win='Win', place='Place', exacta='Exacta', trifecta='Trifecta', quadpot='Quadpot',
                           placepot='Placepot', jackpot='Jackpot')
