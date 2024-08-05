from voltron.pages.shared import get_device_properties
from voltron.pages.shared.contents.football import SportPageDesktop
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import TennisCompetitionsTabContent, \
    TennisCompetitionsTabContentDesktop


class Tennis(SportPageDesktop):
    _url_pattern = r'^https?:\/\/.+\/tennis(?!\/event)'
    _league_icon = 'xpath=.//*[contains(@href, "search-leagues")]'

    @property   # need this for football league icon test
    def is_league_icon_present(self):
        return self._find_element_by_selector(selector=self._league_icon, timeout=2, context=self._we) is not None

    @property
    def _competitions_tab(self):
        return TennisCompetitionsTabContent if get_device_properties()['type'] != 'desktop' \
            else TennisCompetitionsTabContentDesktop
