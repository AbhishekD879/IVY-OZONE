from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase, SportPageBase
from voltron.pages.shared.contents.football import Football
from voltron.pages.shared.contents.sports_tab_contents.outrights_tab_content import OutrightsTabContent


class Snooker(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/snooker(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class Cycling(SportRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/cycling(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class Cricket(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/cricket(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'


class Boxing(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/boxing(\/)?(competitions)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class Darts(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/darts(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'


class MotorSports(Football):
    _url_pattern = r'^https?:\/\/.+\/motor-sports(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class IceHockey(Football):
    _url_pattern = r'^https?:\/\/.+\/ice-hockey(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'


class MotorBikes(Football):
    _sections = 'xpath=.//*[@data-crlat="sportSectionHeader"]'
    _url_pattern = r'^https?:\/\/.+\/motor-bikes(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'
    _tab_content_type = OutrightsTabContent
    _section = 'xpath=.//*[@data-crlat="sportSectionHeader"]'

    @property
    def section(self):
        return TextBase(selector=self._section, context=self._we, timeout=5)

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)


class Diving(SportRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/diving(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class Triathlon(SportRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/triathlon(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class Formula1(Football):
    _url_pattern = r'^https?:\/\/.+\/formula-1(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'
    _sections = 'xpath=.//*[@data-crlat="sportSectionHeader"]'
    _tab_content_type = OutrightsTabContent

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)


class Volleyball(Football):
    _url_pattern = r'^https?:\/\/.+\/volleyball(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'


class Badminton(Football):
    _url_pattern = r'^https?:\/\/.+\/badminton(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'


class Golf(SportPageBase):
    _url_pattern = r'^https?:\/\/.+\/golf(\/)?(competitions)?(live|matches|coupons|outrights|specials|golf_matches(\/)allEvents|golf_matches)?(\/)?(today|tomorrow|future)?$'


class Esports(Football):
    _url_pattern = r'^https?:\/\/.+\/esports(\/)?(live|matches|coupons|outrights)?(\/)?(today|tomorrow|future)?$'


class TableTennis(SportRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/table-tennis(\/)?(live|matches|coupons|outrights|competitions)?(\/)?(today|tomorrow|future)?$'
