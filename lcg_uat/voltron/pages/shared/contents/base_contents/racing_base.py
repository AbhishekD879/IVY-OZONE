from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_tab_content import RacingTabContent, \
    GreyhoundRacingTabContent


class RacingPageBase(SportRacingPageBase):
    _tab_content_type = RacingTabContent


class GreyhoundPageBase(SportRacingPageBase):
    _tab_content_type = GreyhoundRacingTabContent
