from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.home_page_components.highlight_carousel import HighlightCarousel
from voltron.pages.shared.components.in_play_module import InPlayModule
from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.surface_bets_carousel import SurfaceBetsCarousel
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4ColumnPanel
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4SectionFeatured
from voltron.pages.shared.contents.base_contents.racing_base_components.today_tomorrow_components import TodayTomorrowEventGroupListItem
from voltron.pages.shared.contents.edp.sport_event_details import EventDetails
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class MobileFeaturedNext4ColumnPanel(Next4ColumnPanel):

    @property
    def each_way_terms(self):
        self.scroll_to()
        return TextBase(selector=self._ew_container, context=self._we)


class FeaturedRacingEventGroup(Next4SectionFeatured):
    group_type = 'race card'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)

    @property
    def _list_item_type(self):
        device_type = get_device_properties()
        return Next4ColumnPanel if device_type == 'desktop' else MobileFeaturedNext4ColumnPanel


class FeaturedTodayTomorrowEventGroupListItem(TodayTomorrowEventGroupListItem):
    group_type = 'race grid'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)


class FeaturedSportEventGroupBySelection(EventGroup, SportTemplate):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Selection"]'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'
    group_type = 'sport event'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)

    @property
    def first_player_bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)


class FeaturedSportEventGroupByType(EventGroup):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Type"]'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'
    group_type = 'sport event'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)


class FeaturedSportEventGroupByClass(EventGroup):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Class"]'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'
    group_type = 'sport event'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)


class FeaturedSportEventGroupByCategory(EventGroup):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Category"]'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'
    group_type = 'sport event'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)


class EventHubOutcomes(EventGroup):
    _item = 'xpath=.//*[@class="odds-content"]'


class EventHubFeaturedEvent(EventGroup, EventDetails):
    _item = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _list_item_type = EventHubOutcomes
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'

    @property
    def show_more(self):
        return self._find_element_by_selector(selector=self._show_more, timeout=1)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._wait_all_items()
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item._we_text(item_we): list_item})
        return items_ordered_dict


class FeaturedSportEventGroupByEvent(EventGroup, SportTemplate):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Event"] | .//*[@data-crlat="featured.type.oddsCard.Market"]'
    _footer = 'xpath=.//*[@data-crlat="showMore"]'
    group_type = 'sport event'

    @property
    def footer(self):
        return LinkBase(selector=self._footer, context=self._we)


class FeaturedEnhancedMultiples(EventGroup):
    _item = 'xpath=.//*[@data-crlat="featured.type.oddsCard.Enhanced Multiples"]'


class FeaturedTabAccordionList(AccordionsList):
    _list_item_type = None
    _item = 'xpath=.//*[@data-crlat="accordion"][.//header]'

    _type_selector = 'xpath=.//*[contains(@data-crlat, "featured.type")]'
    _types_dict = {
        'featured.type.oddsCard.Type': FeaturedSportEventGroupByType,
        'featured.type.oddsCard.Selection': FeaturedSportEventGroupBySelection,
        'featured.type.racingGrid': FeaturedTodayTomorrowEventGroupListItem,
        'featured.type.raceCard raceCardCarousel': FeaturedRacingEventGroup,
        'featured.type.raceCard': FeaturedRacingEventGroup,
        'featured.type.oddsCard.Enhanced Multiples': FeaturedEnhancedMultiples,
        'featured.type.oddsCard.Event': FeaturedSportEventGroupByEvent,
        'featured.type.oddsCard.Market': FeaturedSportEventGroupByEvent,
        'featured.type.oddsCard.Class': FeaturedSportEventGroupByClass,
        'featured.type.oddsCard.Category': FeaturedSportEventGroupByCategory
    }

    def _get_section_type(self, section):
        # todo: may need extra investigation and improvements on future
        try:
            section_type = self._find_element_by_selector(selector=self._type_selector, context=section, timeout=1)
        except StaleElementReferenceException:
            section_type = self._find_element_by_selector(selector=self._type_selector, context=section, timeout=0.5)
        if not section_type:
            self._list_item_type = FeaturedSportEventGroupByType
            self._logger.warning('*** As template type is not recognized suppose it is Featured Sport section by Type')
        else:
            attribute = section_type.get_attribute('data-crlat')
            _list_item_type = self._types_dict.get(attribute)
            if not _list_item_type:
                raise VoltronException(
                    f'Cannot recognize "{self.__class__.__name__}" item type by attribute "{attribute}"')
            self._list_item_type = self._types_dict.get(section_type.get_attribute('data-crlat'))

        self._logger.info(f'*** Recognized "{self._list_item_type.__name__}" type section')

    def _get_section(self, num, section):
        self.scroll_to_we(section)
        # have to do this initialization to handle correct expanding - MG: this breaks the case with module created collapsed by default
        # MG: so I added collapse afterwards (if module was initially collapsed)
        tmp_section = EventGroup(web_element=section,
                                 timeout=2)  # for spinner, if it is shown, we won't wait whole 15 sec
        is_expanded = tmp_section.is_expanded()
        if not is_expanded:
            tmp_section.expand()

        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        section = items_we[num]
        self._get_section_type(section=section)
        item_component = self._list_item_type(web_element=section)
        try:
            component_name = item_component.name
        except StaleElementReferenceException:
            items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
            section = items_we[num]
            item_component = self._list_item_type(web_element=section)
            component_name = item_component.name
        if not is_expanded:
            try:
                tmp_section.collapse()
            except StaleElementReferenceException:
                tmp_section = EventGroup(web_element=section, timeout=2)
                tmp_section.collapse()
        return OrderedDict({component_name: item_component})

    @property
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_exception_type((StaleElementReferenceException, IndexError)),
           wait=wait_fixed(wait=5),
           reraise=True)
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        len_items = len(items_we)
        for num in range(0, len_items):
            try:
                section = items_we[num]
                items_ordered_dict.update(self._get_section(num=num, section=section))
            except VoltronException:
                items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
                section = items_we[num]
                items_ordered_dict.update(self._get_section(num=num, section=section))
        return items_ordered_dict

    @property
    def items(self):
        raise VoltronException('Deprecated property! Please use items_as_ordered_dict instead')


class HomePageFeaturedTabContent(TabContent):
    _accordions_list = 'xpath=.//*[@data-crlat="accordionsList"][*]'
    _accordions_list_type = FeaturedTabAccordionList
    _highlight_carousel = 'xpath=.//*[@data-crlat="highlight-carousel-container"]'
    _highlight_carousel_type = HighlightCarousel
    _inplay_module = 'xpath=.//*[@data-crlat="inplayModule"]'
    _module_type = InPlayModule
    _verify_spinner = True
    _featured_event = 'xpath=.//*[@class="featured-race-card"] | //*[@data-crlat="accordion"][.//header]'
    _featured_event_type = EventHubFeaturedEvent
    _subheader = 'xpath=.//*[@data-crlat="raceSubHeader"]'
    _see_all = 'xpath=.//*[@data-crlat="raceNextLink"]'

    @property
    def event_hub_items_dict(self):
        items_we = self._find_elements_by_selector(selector=self._featured_event, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            featured_event = self._featured_event_type(web_element=item_we)
            items_ordered_dict[featured_event.name] = featured_event
        return items_ordered_dict

    @property
    def subheader(self):
        return self._find_element_by_selector(selector=self._subheader, timeout=1)

    @property
    def see_all(self):
        return self._find_element_by_selector(selector=self._see_all, timeout=1)

    @property
    def highlight_carousels(self):
        items_we = self._find_elements_by_selector(selector=self._highlight_carousel, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            highlight_carousel = self._highlight_carousel_type(web_element=item_we)
            items_ordered_dict[highlight_carousel.name] = highlight_carousel
        return items_ordered_dict

    def has_highlight_carousels(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._highlight_carousel, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Highlight carousel status to be "{expected_result}"')

    @property
    def in_play_module(self):
        return self._module_type(selector=self._inplay_module, context=self._we)

    def has_in_play_module(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._inplay_module, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Inplay Module status to be "{expected_result}"')


class DesktopHomePageFeaturedTabContent(TabContent):
    _accordions_list_type = FeaturedTabAccordionList
    _highlight_carousel_type = HighlightCarousel
    _highlight_carousel = 'xpath=.//featured-highlight-carousel/*[@data-crlat="highlight-carousel-container"]'
    _surface_bets_carousel = 'xpath=.//*[@data-crlat="surfaceBetsCarousel"]'

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector)

    @property
    def highlight_carousels(self):
        items_we = self._find_elements_by_selector(selector=self._highlight_carousel, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            highlight_carousel = self._highlight_carousel_type(web_element=item_we)
            items_ordered_dict[highlight_carousel.name] = highlight_carousel
        return items_ordered_dict

    @property
    def surface_bets(self):
        return SurfaceBetsCarousel(selector=self._surface_bets_carousel, context=self._we, timeout=5)

    def has_highlight_carousels(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._highlight_carousel, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Highlight carousel status to be "{expected_result}"')

    def has_surface_bets(self, expected_result: bool = True, timeout: int = 1) -> bool:
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._surface_bets_carousel,
                                                                        context=self._we, timeout=0),
                                 expected_result=expected_result,
                                 name=f'Surface bet status to be "{expected_result}"',
                                 timeout=timeout)
        return result
