from multidict import MultiDict
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.base_components import LadbrokesMeeting
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_accordions_list import\
    RacingEventsAccordionsList, SpecialsEvent
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_accordions_list import Next4Section,\
    EnhancedMultiples, Specials, ResultsByLatestResult, ResultsByMeeting, RaceGridEventGroup, Antepost, AntepostEvent
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.enhanced_races_events import LadbrokesEnhancedRaces
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class LadbrokesAntepostEvent(AntepostEvent):
    _event_link = 'xpath=.//*[@data-crlat="couponName"]'
    _event_name = 'xpath=.//*[@data-crlat="couponName"]'


class LadbrokesAntepostDesktop(Antepost):
    _item = 'xpath=.//*[@data-crlat="race.antepost.event.desktop" and not(contains(@class, "cell"))]'


class LadbrokesAntepost(Antepost):
    _list_item_type = LadbrokesAntepostEvent


class LadbrokesRaceGridEventGroup(RaceGridEventGroup):
    _list_item_type = LadbrokesMeeting
    _meeting_name = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'

    @property
    def meeting_name(self):
        return self._get_webelement_text(selector=self._meeting_name)


class LadbrokesSpecialsEvent(SpecialsEvent):
    _name = 'xpath=.//*[@data-crlat="event.name"]'

    @property
    def event_name(self):
        return self._get_webelement_text(we=self._we)


class LadbrokesSpecials(Specials):
    _item = 'xpath=.//*[@data-crlat="race.specialsSectionEvent"]'
    _list_item_type = LadbrokesSpecialsEvent

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._wait_all_items()
        self._logger.debug(
            f'*** Found{len(items_we)}{self.__class__.name} - {self._list_item_type.__name__} items')
        items_ordered_dict = []
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.append((list_item.event_name, list_item))
        return MultiDict(items_ordered_dict)


class LadbrokesRacingEventsAccordionsList(RacingEventsAccordionsList):
    _item = 'xpath=.//*[@data-crlat="outerAccordion"] | .//*[@data-crlat="racing.futureEvents"]//accordion'

    _list_item_attribute_selector = 'xpath=.//*[contains(@data-crlat, "race.")] | .//*[contains(@data-crlat, "raceGrid.")]'

    _list_item_attribute_types = {
        'race.raceGrid': LadbrokesRaceGridEventGroup,
        'race.next4Carousel': Next4Section,
        'race.enhancedRacesCarousel': LadbrokesEnhancedRaces,
        'race.enhancedMultiplesCarousel': EnhancedMultiples,
        'race.specialsSection': Specials,  # desktop version
        'race.specialsSectionEvent': LadbrokesSpecials,  # mobile version
        'race.antepost.event': LadbrokesAntepost,
        'race.antepost.event.desktop': LadbrokesAntepostDesktop,
        'race.racingTabResults.byLatest.results': ResultsByLatestResult,
        'race.racingTabResults.byMeetings.event': ResultsByMeeting,
        'raceGrid.meeting': LadbrokesRaceGridEventGroup
    }
    _default_event_group = LadbrokesRaceGridEventGroup

    def _get_item(self, web_element):
        list_item_content_attr = self._find_element_by_selector(selector=self._list_item_attribute_selector,
                                                                context=web_element,
                                                                timeout=1)
        section_expanded = False
        if not list_item_content_attr:
            try:
                wait_for_result(lambda: self.scroll_to_we(web_element=web_element), timeout=2,
                                bypass_exceptions=VoltronException)
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
                self._logger.debug(f'*** Recognized "{list_item_content_type.__name__}" type on {self.__class__.__name__}')
            else:
                self._logger.warning(
                    f'*** Racing section type "{attr}" is not known, trying to evaluate by header title')
                header_title = self._get_webelement_text(selector='xpath=.//*[@data-crlat="containerHeader"]',
                                                         context=web_element,
                                                         timeout=1)
                if header_title == vec.racing.OFFERS_AND_FEATURED_RACES:
                    list_item_content_type = LadbrokesEnhancedRaces
                else:
                    list_item_content_type = self._default_event_group
                    self._logger.warning(
                        f'*** Racing section type "{attr}" is not known, assuming it is "{list_item_content_type.__name__}"')
        context = list_item_content_type(web_element=web_element)
        item_name, item_type = context.name, context
        if section_expanded:
            item_type.collapse()
        return item_name, item_type
