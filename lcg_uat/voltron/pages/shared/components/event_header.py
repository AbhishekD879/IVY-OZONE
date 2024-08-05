from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.components.content_header import HeaderLine


class EventHeader(SportRacingPageBase):
    _header_line = 'xpath=.//*[@data-crlat="topBar"]'
    _header_line_type = HeaderLine

    @property
    def header_line(self):
        return self._header_line_type(selector=self._header_line)

    @property
    def sport_title(self):
        return self.header_line.page_title.sport_title

    def press_back(self):
        self.header_line.back_button.click()

    def go_to_sport_home(self):
        self.header_line.page_title.click()

    @property
    def back_button_exists(self):
        return self.header_line.has_back_button
