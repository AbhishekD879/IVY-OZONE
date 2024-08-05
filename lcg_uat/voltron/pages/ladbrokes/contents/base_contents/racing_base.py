from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.racing_tab_content import LadbrokesRacingTabContent


class LadbrokesRacingPageBase(SportRacingPageBase):
    _tab_content_type = LadbrokesRacingTabContent
