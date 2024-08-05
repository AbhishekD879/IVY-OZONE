from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.international_tote_carousel import ToteEventsCarousel
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.racing_accordions_list import LadbrokesRacingEventsAccordionsList
from voltron.pages.shared.components.build_card import BuildCard


class LadbrokesToteEventsCarousel(ToteEventsCarousel):
    _meeting_name = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'


class LadbrokesRacingTabContent(TabContent):
    _accordions_list_type = LadbrokesRacingEventsAccordionsList
    _build_own_card_type = BuildCard
    _build_own_card = 'xpath=.//*[@data-crlat="buildCardContainer"]'
    _tote_carousel = 'tag=tote-slider'

    def _wait_active(self, timeout=0):
        self._find_element_by_selector(selector=self._selector, context=get_driver())
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._accordions_list_type._item,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector)

    @property
    def build_card(self):
        return self._build_own_card_type(selector=self._build_own_card, context=self._we)

    @property
    def tote_events_carousel(self):
        return LadbrokesToteEventsCarousel(selector=self._tote_carousel, context=self._we)
