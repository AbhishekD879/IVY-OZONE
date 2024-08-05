from voltron.environments.constants.base.sportsbook import SB


class CoralSB(SB):
    """
    src/app/lazy-modules/locale/translations/en-US/sb.lang.ts
    """
    PROMOTIONS = SB.PROMOTIONS.upper()
    PRIVATE_MARKETS_TERMS_AND_CONDITIONS = SB.PRIVATE_MARKETS_TERMS_AND_CONDITIONS.upper()
    INSURANCE_MARKETS = SB.INSURANCE_MARKETS.upper()
    HOME = SB.HOME.upper()
    DRAW = SB.DRAW.upper()
    AWAY = SB.AWAY.upper()
    NO_GOAL = SB.NO_GOAL.upper()
    FIRST_GOALSCORER_SCORECAST = SB.FIRST_GOALSCORER_SCORECAST.upper()
    LAST_GOALSCORER_SCORECAST = SB.LAST_GOALSCORER_SCORECAST.upper()
    FAVOURITE_MATCHES = SB.FAVOURITE_MATCHES.upper()
    ALL_SPORTS = SB.ALL_SPORTS.upper()
