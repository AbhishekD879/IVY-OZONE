from collections import OrderedDict
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from voltron.pages.shared.components.accordions_container import Accordion, AccordionHeader
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.your_call_static_block import YourCallStaticBlock
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.date_tab import DateTab
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem, TabsMenu
from voltron.pages.shared.contents.base_contents.racing_base_components.base_components import Meeting
from voltron.pages.shared.contents.base_contents.racing_base_components.each_way_terms import EachWayTerms
from voltron.pages.shared.contents.base_contents.racing_base_components.enhanced_races_event import EnhancedRaces
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4Section
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_results import ResultsByLatestResult
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_results import ResultsByMeeting
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import get_css_property_text, scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class RacingDateTab(DateTab):
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = ButtonBase

    @property
    def current_date_tab(self):
        tab = next((tab_name for tab_name, tab in self.items_as_ordered_dict.items() if tab.is_selected()), None)
        if not tab:
            raise VoltronException('No active date tab found')
        return tab


class RaceGridEventGroup(EventGroup):
    _date_tab = 'xpath=.//*[contains(@data-crlat, "switchers")]'
    _date_tab_type = RacingDateTab
    _item = 'xpath=.//*[@data-crlat="raceGrid.meeting"]'
    _list_item_type = Meeting
    _virtual_race_carousel = 'xpath=.//*[text()="Virtual Race Carousel"]/../..//parent::accordion'

    def _wait_all_items(self, poll_interval=1, timeout=20):
        """
        Wait all items has no sense in race grid, so overriding it to return all items at once
        """
        return self._find_elements_by_selector(selector=self._item)

    @property
    def date_tab(self):
        return self._date_tab_type(selector=self._date_tab, context=self._we)

    @property
    def virtual_race_carousel(self):
        return VirtualRaceCarousel(selector=self._virtual_race_carousel, context=self._we)


class EnhancedMultiplesEvent(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'
    _outcome_name = 'xpath=.//*[@data-crlat="raceCard.outcomeName"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, timeout=1).get_attribute('innerHTML')

    @property
    def outcome_name(self):
        return self._find_element_by_selector(selector=self._outcome_name, timeout=1).get_attribute('innerHTML')

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def event_name(self):
        return '%s - %s' % (self.name.upper(), self.outcome_name)


class EnhancedMultiples(EventGroup):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = EnhancedMultiplesEvent


class SpecialsOutcome(ComponentBase):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _name = 'xpath=.//*[@data-crlat="outcomeName"]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._name, timeout=0, context=self._we)

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)


class SpecialsEvent(EventGroup):
    _date = 'xpath=.//*[@data-crlat="eventDate"]'
    _ew_container = 'xpath=.//*[@data-crlat="terms" or @data-crlat="eachWayContainer"]'
    _item = 'xpath=.//*[@data-crlat="outcomeEntity"]'
    _list_item_type = SpecialsOutcome
    _show_all_btn = 'xpath=.//*[@data-crlat="showAllButton"]'

    def _wait_all_items(self, poll_interval=1, timeout=20):
        """
        Wait all items has no sense in Specials, so overriding it to return all items at once
        """
        return self._find_elements_by_selector(selector=self._item, context=self._we)

    @property
    def event_name(self):
        return self.group_header.title_text

    @property
    def event_date(self):
        return self._get_webelement_text(selector=self._date, timeout=1)

    @property
    def each_way_terms(self):
        return EachWayTerms(selector=self._ew_container, context=self._we, timeout=1)

    def has_each_way_terms(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._ew_container,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Each Way terms status to be {expected_result}')

    @property
    def has_show_all_button(self):
        show_all = self._find_element_by_selector(selector=self._show_all_btn, timeout=1)
        return show_all.is_displayed() if show_all else False

    @property
    def show_all_button(self):
        return ButtonBase(selector=self._show_all_btn, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._wait_all_items()
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            if list_item.event_name == '':
                continue
            items_ordered_dict.update({list_item.event_name: list_item})
        return items_ordered_dict


class Specials(AccordionsList, EventGroup):
    _list_item_type = SpecialsEvent


class YourCallSpecialsEvent(EnhancedMultiplesEvent):
    _name = 'xpath=.//*[@data-crlat="oddsNames"]'

    @property
    def _event_name_we(self):
        return self._find_element_by_selector(selector=self._name)

    @property
    def event_name(self):
        return self.name

    def css_property_text(self, property_name=':before'):
        return get_css_property_text(self._event_name_we, property_name)


class YourCallTabsMenuItem(TabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="switcher.name"]'


class YourCallTabsMenu(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = YourCallTabsMenuItem


class HorseRacingYourCallStaticText(YourCallStaticBlock):
    _tweet_now_btn = 'xpath=.//*[contains(@class,"btn")]'
    _static_text = 'xpath=.//*[@data-crlat="yourcallStaticText"]/*//span'

    @property
    def tweet_now_button(self):
        return ButtonBase(selector=self._tweet_now_btn, context=self._we)

    @property
    def static_text(self):
        return ComponentBase(selector=self._static_text, context=self._we)


class YourCallSpecials(EventGroup):
    _bet_button = 'xpath=.//*[@data-crlat="selection"]'
    _market_tabs_list = 'xpath=.//*[contains(@data-crlat, "switchers")]'
    _market_tabs_list_type = YourCallTabsMenu

    @property
    def market_tabs_list(self):
        return self._market_tabs_list_type(selector=self._market_tabs_list, context=self._we)

    @property
    def bet_button(self):
        return BetButton(self._bet_button, timeout=0, context=self._we)


class YourCallSpecialsWidget(YourCallSpecials):
    _item = 'xpath=//*[not(contains(@class, "ng-hide"))]/div[@data-crlat="selection"]'
    _list_item_type = YourCallSpecialsEvent
    _view_all_link = 'xpath=.//*[@data-crlat="link.viewAllYC"]'

    @property
    def view_all_link(self):
        return LinkBase(selector=self._view_all_link, context=self._we)


class AntepostEvent(ComponentBase):
    _event_date = 'xpath=.//*[@data-crlat="event.date"]'
    _event_name = 'xpath=.//*[@data-crlat="event.name"]'
    _event_link = 'xpath=.//*[@data-crlat="event.link"]'

    @property
    def date(self):
        return self._get_webelement_text(selector=self._event_date, timeout=1)

    @property
    def type_name(self):
        return self._get_webelement_text(selector=self._event_name, timeout=1)

    @property
    def link(self):
        return ButtonBase(selector=self._event_link, context=self._we)

    @property
    def event_name(self):
        return self.date

    def click(self):
        self.link.click()


class Antepost(EventGroup):
    _item = 'xpath=.//*[@data-crlat="race.antepost.event" and not(contains(@class, "cell"))]'
    _list_item_type = AntepostEvent


class YourHorsesRunningTodayRaceCard(ComponentBase):
    _event_name = 'xpath=.//*[@data-crlat="mystableHeader"]'
    _horse_name = 'xpath=.//*[@data-crlat="raceCard.runner"]/*[1]'
    _jockey_name = 'xpath=.//*[@data-crlat="jockeyName"]'
    _trainer_name = 'xpath=.//*[@data-crlat="trainerName"]'
    _form_id = 'xpath=.//*[@data-crlat="raceCard.runnerFormGuide"]/*[2]'
    _horse_number = 'xpath=.//*[@class="race-runner-number"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, context=self._we)

    @property
    def horse_name(self):
        return self._get_webelement_text(selector=self._horse_name, context=self._we)

    @property
    def name(self):
        return self.horse_name

    @property
    def jockey_name(self):
        return self._get_webelement_text(selector=self._jockey_name, context=self._we)

    @property
    def trainer_name(self):
        return self._get_webelement_text(selector=self._trainer_name, context=self._we)

    @property
    def form_id(self):
        return self._get_webelement_text(selector=self._jockey_name, context=self._we)

    @property
    def horse_number(self):
        return self._get_webelement_text(selector=self._horse_number, context=self._we)

    @property
    def bet_button(self):
        return ButtonBase(selector=self._bet_button, context=self._we)


class YourHorsesRunningTodayAccordionHeader(AccordionHeader):
    _title = 'xpath= .//*[@data-crlat="headerTitle.centerMessage"]'


class YourHorsesRunningToday(Accordion):
    _header_type = YourHorsesRunningTodayAccordionHeader
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = YourHorsesRunningTodayRaceCard


class RacingEventsAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="outerAccordion"]/*[@data-crlat="accordion"]'
    _list_item_type = None

    # recognition of event group types
    _list_item_attribute_selector = 'xpath=.//*[contains(@data-crlat, "race.")] | .//*[@data-crlat="tabContent"]'

    _list_item_attribute_types = {
        'race.raceGrid': RaceGridEventGroup,
        'race.next4Carousel': Next4Section,
        'race.enhancedRacesCarousel': EnhancedRaces,
        'race.enhancedMultiplesCarousel': EnhancedMultiples,
        'race.specialsSection': Specials,  # desktop version
        'race.specialsSectionEvent': Specials,  # mobile version
        'race.yourCallSpecials': YourCallSpecialsWidget,
        'race.antepost.event': Antepost,
        'race.racingTabResults.byLatest.results': ResultsByLatestResult,
        'race.racingTabResults.byMeetings.event': ResultsByMeeting
    }
    _static_block = 'xpath=.//*[@data-crlat="yourcallStaticBlock"]'

    _default_event_group = RaceGridEventGroup
    _your_horses_running_today = 'xpath=.//mystable-horses-running-today-carousel'
    _your_horses_running_today_type = YourHorsesRunningToday

    @property
    def your_horses_running_today(self):
        return self._your_horses_running_today_type(selector=self._your_horses_running_today)

    def has_your_horses_running_today(self):
        return self._find_element_by_selector(selector=self._your_horses_running_today).is_displayed()

    @property
    def static_block(self):
        return HorseRacingYourCallStaticText(selector=self._static_block, context=self._we)

    def _get_item(self, web_element):
        list_item_content_attr = self._find_element_by_selector(selector=self._list_item_attribute_selector,
                                                                context=web_element,
                                                                timeout=1)
        section_expanded = False
        if not list_item_content_attr:
            try:
                self.scroll_to_we(web_element=web_element)
                accordion = Accordion(web_element=web_element)
                if not accordion.is_expanded(expected_result=False):
                    accordion.expand()
                    section_expanded = True
                list_item_content_attr = self._find_element_by_selector(selector=self._list_item_attribute_selector,
                                                                        context=web_element, timeout=1)
            except Exception:
                pass
        if not list_item_content_attr:
            self._logger.warning('*** Section content type is not recognised, assuming it is Race Grid')
            list_item_content_type = self._default_event_group
        else:
            attr = list_item_content_attr.get_attribute('data-crlat')
            known_racing_event_group = self._list_item_attribute_types.get(attr)
            if known_racing_event_group:
                list_item_content_type = known_racing_event_group
                self._logger.debug('*** Recognized "%s" type on %s' % (list_item_content_type.__name__, self.__class__.__name__))
            else:
                list_item_content_type = self._default_event_group
                self._logger.warning(
                    '*** Racing section type "%s" is not known, assuming it is %s' % (attr, list_item_content_type.__name__))
        context = list_item_content_type(web_element=web_element)
        item_name, item_type = context.name, context
        if section_expanded:
            item_type.collapse()
        return item_name, item_type

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            item_name, item = wait_for_result(lambda: self._get_item(web_element=item_we), timeout=5, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException,VoltronException))
            items_ordered_dict.update({item_name: item})
        return items_ordered_dict

    def get_items(self, bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException), timeout=2, **kwargs) -> OrderedDict:
        """
        Get a limited number of items from the container.
        Args:
            **kwargs: One of the below two keyword arguments is mandatory.
                - number (int): The number of items to retrieve.
                - name (str): The name of a specific item to retrieve.
        Returns:
            OrderedDict: An ordered dictionary containing item names as keys and corresponding web elements as values.
    """
        number = kwargs.get('number')
        name = kwargs.get('name')
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        search_scope = [item_we for item_we in items_we] if name else [item_we for item_we in items_we[:number]]
        items_ordered_dict = OrderedDict()
        for item_we in search_scope:
            list_item_name = item_we.text.split('\n')[0]
            if name and (list_item_name.upper() == name.upper()):
                scroll_to_center_of_element(item_we)
                item_name, item = wait_for_result(lambda: self._get_item(web_element=item_we), timeout=timeout,
                                                  bypass_exceptions=bypass_exceptions)
                items_ordered_dict.update({name: item})
                return items_ordered_dict
            elif not name:
                item_name, item = wait_for_result(lambda: self._get_item(web_element=item_we), timeout=timeout,
                                                  bypass_exceptions=bypass_exceptions)
                items_ordered_dict.update({item_name: item})
        return items_ordered_dict



class InternationalHorseRacingLabel(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class VirtualRaceCarouselEvents(ComponentBase):
    _name = 'xpath=.//*[@class="slide-title"]'
    _start_time = 'xpath=.//*[@class="start-time"]'
    _live_now_label = 'xpath=.//*[@class="live-now-label"]'
    _start_time_counter = 'xpath=.//*[@class="slide-body"]/child::*[@class="timer"]'
    _bet_now_link = 'xpath=.//*[@class="bet-now-link"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=5)

    @property
    def start_time(self):
        return self._find_element_by_selector(selector=self._start_time, context=self._we, timeout=5)

    def has_live_label(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._live_now_label,
                                                                      timeout=5),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'LIVE label shown status to be {expected_result}')

    @property
    def live_label(self):
        return self._find_element_by_selector(selector=self._live_now_label, context=self._we, timeout=5)

    @property
    def start_time_counter(self):
        return self._find_element_by_selector(selector=self._start_time_counter, context=self._we, timeout=5)

    @property
    def bet_now_link(self):
        return LinkBase(selector=self._bet_now_link, context=self._we, timeout=5)


class VirtualRaceCarousel(ComponentBase):
    _item = 'xpath=.//*[@class="slide"]'
    _list_item_type = VirtualRaceCarouselEvents
    _view_all_virtuals_link = 'xpath=.//*[@class="slide-body last-title"]'

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def view_all_virtuals_link(self):
        return self._find_element_by_selector(selector=self._view_all_virtuals_link, context=self._we, timeout=5)
