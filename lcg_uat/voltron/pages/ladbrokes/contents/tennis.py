from voltron.pages.ladbrokes.contents.base_contents.sport_base import LadbrokesSportPageBase
from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import TennisCompetitionsTabContent, \
    TennisCompetitionsTabContentDesktop


class LadbrokesMobileTennis(LadbrokesSportPageBase):
    _url_pattern = r'^https?:\/\/.+\/tennis(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
    _competitions_tab = TennisCompetitionsTabContent


class LadbrokesDesktopTennis(SportPageDesktop):
    _url_pattern = r'^https?:\/\/.+\/tennis(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
    _competitions_tab = TennisCompetitionsTabContentDesktop
