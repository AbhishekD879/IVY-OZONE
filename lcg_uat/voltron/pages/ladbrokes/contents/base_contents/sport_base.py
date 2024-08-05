from voltron.pages.ladbrokes.contents.sports_tab_contents.competitions_tab_content import \
    LadbrokesCompetitionsTabContent
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase
from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content_desktop import \
    CompetitionsTabContentDesktop


class LadbrokesSportPageBase(SportPageBase):
    _competitions_tab = LadbrokesCompetitionsTabContent
    _date_tab = 'xpath=.//*[contains(@data-crlat, "switchers") and not(contains(@class, "switchers no-paddings"))]'


class LadbrokesDesktopSportPageBase(SportPageDesktop):
    _competitions_tab = CompetitionsTabContentDesktop

    @property
    def _coupons_tab(self):
        return CompetitionsTabContentDesktop
