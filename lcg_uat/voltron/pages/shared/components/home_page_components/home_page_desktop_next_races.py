from voltron.pages.shared.components.home_page_components.home_page_next_races_tab import HomePageNextRacesTabContent, \
    HomePageNextRacesItem
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4SectionLegacy
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class HomePageDesktopNextRacesEvent(HomePageNextRacesItem):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'
    _full_race_links = 'xpath=.//*[@data-crlat="raceNextLink"]'


class HomePageDesktopNextRacesSlideContainer(Next4SectionLegacy):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = HomePageDesktopNextRacesEvent


class HomePageDesktopNextRacesModuleContent(HomePageNextRacesTabContent):
    _accordions_list = 'xpath=.//*[@data-crlat="containerContent"]'
    _accordions_list_type = HomePageDesktopNextRacesSlideContainer
    _next_arrow = 'xpath=.//*[@data-crlat="sb.nextRaces"]'
    _prev_arrow = 'xpath=.//*[@data-crlat="sb.previousRaces"]'
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'

    def click_next_arrow(self):
        click(self._find_element_by_selector(selector=self._next_arrow, timeout=3))

    def click_prev_arrow(self):
        click(self._find_element_by_selector(selector=self._prev_arrow, timeout=3))

    @property
    def show_more_link(self):
        return LinkBase(selector=self._show_more, context=self._we)

    def has_show_more_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_more,
                                                   timeout=0) is not None,
            name=f'Show more link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

