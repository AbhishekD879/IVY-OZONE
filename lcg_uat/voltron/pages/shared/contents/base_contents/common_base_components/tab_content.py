from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.contents.sports_tab_contents.next_races_tab import NextRacesFilters
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.home_page_components.highlight_carousel import HighlightCarousel
from voltron.pages.shared.components.in_play_module import InPlayModule
from voltron.pages.shared.components.market_selector_drop_down import MarketSelectorDropDown
from voltron.pages.shared.components.quick_links_sport_pages import QuickLinksSportPages
from voltron.pages.shared.components.surface_bets_carousel import SurfaceBetsCarousel
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList, AccordionsListForCompetitions, AccordionsListForBigCompetitions
from voltron.pages.shared.contents.base_contents.common_base_components.sport_list_item import SportEventListItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.timeline_filters import TimelineFilters
from voltron.pages.shared.components.virtual_entry_point_banner import VirtualEntryPointBanner


class TabContent(ComponentBase):
    _grouping_selection_buttons = 'xpath=.//div[contains(@data-crlat, "switchers")]'
    _grouping_selection_buttons_type = GroupingSelectionButtons
    _accordions_list = 'xpath=.//*[not(ancestor::featured-module) and @data-crlat="accordionsList" and not(featured-quick-links) and not(surface-bets-carousel) and not(featured-highlight-carousel) and not (featured-inplay)][*] | .//*[@data-crlat="enhanceMultiplesMarket"]'
    _accordions_list_type = AccordionsList
    _big_competition_accordions_list = 'xpath=.//big-competition-tabs'
    _big_competition_accordions_list_type = AccordionsListForBigCompetitions
    _filters_list_type = NextRacesFilters
    _co_header_title = 'xpath=.//*[@class="co-header-title"]'
    _market_selector_module = 'xpath=.//*[@data-crlat="dropdown"]'
    _market_selector_element = 'xpath=.//*[@data-crlat="dropdown-menu"]'
    _timeline_filters = 'xpath=.//*[contains(@class, "competition-filters")]'
    _market_selector_sticky = 'xpath=.//*[@data-crlat="marketSelectorModule"]'
    _dropdown_market_selector_type = MarketSelectorDropDown
    _no_events_label = 'xpath=.//*[@data-crlat="noEventsFound"]'
    _quick_links_section = 'xpath=.//featured-quick-links'
    _surface_bets_carousel = 'xpath=.//*[@data-crlat="surfaceBetsCarousel"]'
    _odds_card = 'xpath=.//*[@data-crlat="eventEntity"][.//*[contains(@data-crlat, "oddsCard") and contains(@data-crlat, "Template")]]'
    _fade_out_overlay = True
    _opps_error = 'xpath=.//*[@data-crlat="requestError"] | .//*[class="item-inner text-center"]'
    _opps_error_message = 'xpath=.//*[@class="error-message"] | .//*[contains(text(), "Oops! We are having trouble")]'
    _try_again_button = 'xpath=.//*[@data-crlat="refresh"]'
    _highlight_carousel = 'xpath=.//*[@data-crlat="highlight-carousel-container"]'
    _highlight_carousel_type = HighlightCarousel
    _in_play_module = 'xpath=.//*[@data-crlat="inplayModule"]'
    _virtual_entry_point_banner_section = 'xpath=.//virtual-entry-point-banner/div'
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs)

    def has_inplay_module(self, name=None, expected_result=True, timeout=2):
        if not name:
            name = f'In Play module display status is: "{expected_result}"'
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._in_play_module, timeout=timeout),
                               expected_result=expected_result,
                               name=name,
                               timeout=timeout)

    @property
    def highlight_carousels(self):
        items_we = self._find_elements_by_selector(selector=self._highlight_carousel, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            highlight_carousel = self._highlight_carousel_type(web_element=item_we)
            items_ordered_dict[highlight_carousel.name] = highlight_carousel
        return items_ordered_dict

    @property
    def in_play_module(self):
        return InPlayModule(selector=self._in_play_module, context=self._we)
    def _wait_active(self, timeout=0):
        self._find_element_by_selector(selector=self._selector, context=get_driver())
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._accordions_list,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    def has_no_events_label(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._no_events_label, timeout=0) is not None,
                               name=f'{self.__class__.__name__} "No events" label status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_dropdown_market_selector(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._market_selector_module, timeout=0) is not None,
            name=f'Market selector dropdown status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_opps_error_message(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._opps_error, timeout=0) is not None,
            name=f'"Opps! We are having trouble..." message status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def opps_error_message(self):
        return self._find_element_by_selector(selector=self._opps_error_message, context=self._we, timeout=5)

    @property
    def try_again_button(self):
        return self._find_element_by_selector(selector=self._try_again_button, context=self._we, timeout=5)

    @property
    def timeline_filters(self):
        return TimelineFilters(selector=self._timeline_filters, timeout=5)

    def has_timeline_filters(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._timeline_filters, timeout=0) is not None,
            name=f'Time filter status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def market_selector_element(self):
        return self._find_element_by_selector(selector=self._market_selector_element, context=self._we, timeout=5)

    @property
    def dropdown_market_selector(self):
        return self._dropdown_market_selector_type(selector=self._market_selector_module, context=self._we, timeout=2)

    @property
    def is_market_selector_sticky(self):
        we = self._find_element_by_selector(selector=self._market_selector_sticky, timeout=0)
        if we.get_attribute('class'):
            sticky = 'sticky' in we.get_attribute('class')
            return sticky
        return False

    @property
    def has_grouping_buttons(self):
        return self._find_elements_by_selector(selector=self._grouping_selection_buttons, context=self._we, timeout=5) != []

    @property
    def grouping_buttons(self):
        if self.has_grouping_buttons:
            return self._grouping_selection_buttons_type(self._grouping_selection_buttons, context=self._we, timeout=5)
        else:
            raise VoltronException('No Grouping Buttons object found')

    @property
    def accordions_list(self):
        try:
            self._find_element_by_selector(selector=self._accordions_list,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=1)
        except StaleElementReferenceException:
            self._we = self._find_myself()
        return self._accordions_list_type(selector=self._accordions_list, context=self._we)

    @property
    def big_competition_accordions_list(self):
        return self._big_competition_accordions_list_type(selector=self._big_competition_accordions_list, context=self._we)

    @property
    def filters_list(self):
        return self._filters_list_type(web_element=self._we, selector=self._selector)

    @property
    def has_co_header_title(self):
        if self._find_element_by_selector(selector=self._co_header_title) == None:
            return False
        return True

    @property
    def accordions_list_for_competitions(self):
        try:
            self._find_element_by_selector(selector=self._accordions_list,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=1)
        except StaleElementReferenceException:
            self._we = self._find_myself()
        return AccordionsListForCompetitions(selector=self._accordions_list, context=self._we)

    @property
    def quick_links(self):
        return QuickLinksSportPages(selector=self._quick_links_section, context=self._we)

    def has_quick_links(self, timeout=5, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quick_links_section, timeout=0) is not None,
            name=f'Quick Links status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def surface_bets(self):
        return SurfaceBetsCarousel(selector=self._surface_bets_carousel, context=self._we, timeout=5)

    @property
    def selected_market_name(self):
        return self._get_webelement_text(selector=self._market_selector_sticky, timeout=2, context=self._we)

    def has_surface_bets(self, expected_result: bool = True, timeout: int = 1) ->bool:
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._surface_bets_carousel,
                                                                        context=self._we, timeout=0),
                                 expected_result=expected_result,
                                 name=f'Surface bet status to be "{expected_result}"',
                                 timeout=timeout)
        return result

    def get_events(self, number_of_events: int = None) -> OrderedDict:
        """
        Gets all events on page based on availability of @data-crlat="eventEntity" attribute
        :param number_of_events: Number of events returned
        :return:  OrderedDict where key is event name, value - SportTemplate object
        """
        events = self._find_elements_by_selector(selector=self._odds_card, context=self._we)
        self._logger.debug(
            f'*** Found {len(events)} {self.__class__.__name__} - {SportEventListItem.__name__} items')
        items_ordered_dict = OrderedDict()
        for event in events[:number_of_events]:
            list_item = SportEventListItem(web_element=event)
            if list_item.is_displayed():
                items_ordered_dict.update({list_item.event_name: list_item})
        return items_ordered_dict

    def get_all_sections_order(self, brand=None, device='mobile'):
        sections_names = OrderedDict()
        module_type_name = {'featured-highlight-carousel': 'HIGHLIGHTS_CAROUSEL',
                            'surface-bets-carousel': 'SURFACE_BET',
                            'featured-quick-links': 'QUICK_LINK',
                            }

        order = 0
        if device == 'desktop':
            sections = self._find_elements_by_selector(selector="xpath=.//featured-module/*")
        else:
            if brand != 'bma':
                sections = self._find_elements_by_selector(selector='xpath=.//*[@data-crlat="accordionsList"]/*')
            else:
                sections = self._find_elements_by_selector(selector='xpath=//div[@_ngcontent-ng-c2749732736 and not(@data-crlat="accordionsList")]/*')
        for section in sections:
            if section.tag_name in list(module_type_name.keys()):
                if module_type_name.get(section.tag_name) not in sections_names:
                    sections_names.update({module_type_name.get(section.tag_name): order})
                    order += 1
        return sections_names

    @property
    def virtual_entry_point_banner(self):
        return VirtualEntryPointBanner(selector=self._virtual_entry_point_banner_section, context=self._we, timeout=10)

    def has_virtual_entry_point_banner(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._virtual_entry_point_banner_section,
                                                   timeout=0) is not None,
            name=f'Virtual entry point banner status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
