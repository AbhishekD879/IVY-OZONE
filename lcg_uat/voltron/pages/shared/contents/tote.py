from collections import OrderedDict

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.accordions_container import AccordionHeader
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.base_contents.racing_base_components.base_components import Event
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_results import ResultsByMeeting
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_results import ResultTable
from voltron.pages.shared.contents.base_contents.racing_base_components.today_tomorrow_components import \
    TodayTomorrowEventGroupListItem
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.utils.waiters import wait_for_result


class ToteEventGroup(TodayTomorrowEventGroupListItem):
    _header = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = Event

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class ToteResultTable(ResultTable):
    _header_type = AccordionHeader


class ToteResultsSubsection(ResultsByMeeting):
    _item = 'xpath=.//*[contains(@data-crlat,"racingTabResults.byMeetings.event")]/*[@data-crlat="accordion"] ' \
            '| .//*[@data-crlat="racingTabResults.byLatest.results"]'

    _list_item_type = ToteResultTable

    @property
    def event_name(self):
        return self.name


class ToteResultsByMeeting(Accordion):
    _item = 'xpath=.//*[@data-crlat="racingTabResults.byMeetings"]/*[@data-crlat="accordion"]'
    _list_item_type = ToteResultsSubsection


class ToteResultsByLatestResult(AccordionsList):
    _list_item_type = ToteResultsSubsection


class ToteEventsAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceGrid.sectionRace"]'
    _list_item_type = ToteEventGroup


class ToteByTimeEvent(Event):
    _name = 'xpath=.//*[@data-crlat="raceList.raceTime"]'
    _horse_icon = 'xpath=.//*[@data-crlat="oddsIcon"]'
    _odds_stream_icon = 'xpath=.//*[@data-crlat="oddsIconStream"]'
    _race_card_link = 'xpath=.//*[@data-crlat="linkRaceCard"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)

    @property
    def horse_icon(self):
        return ComponentBase(selector=self._horse_icon, timeout=0.5, context=self._we)

    def has_odds_stream_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._odds_stream_icon,
                                                                      timeout=0.5),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon shown status to be {expected_result}')

    @property
    def race_card(self):
        return LinkBase(selector=self._race_card_link, timeout=0.5, context=self._we)


class ToteByTimeEventsAccordionsList(ToteEventsAccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceList.eventEntity"]'
    _list_item_type = ToteByTimeEvent


class ToteTabContent(TabContent):
    _show_more_button = 'xpath=.//*[@data-crlat="raceList.buttonShowAll"]'

    @property
    def has_show_more_button(self):
        return self._find_element_by_selector(selector=self._show_more_button, timeout=0.2) is not None

    @property
    def show_more_button(self):
        return ButtonBase(selector=self._show_more_button)

    @property
    def _accordions_list_type(self):
        list_type = ToteEventsAccordionsList
        current_url = get_driver().current_url
        url = current_url.split('/')[-1]
        if url == 'by-time':
            list_type = ToteByTimeEventsAccordionsList
        elif url in ['results', 'by-latest-results']:
            list_type = ToteResultsByLatestResult
        elif url == 'by-meetings':
            list_type = ToteResultsByMeeting
        self._logger.debug(f'*** Recognized "{list_type.__name__}" on "{current_url}"')
        return list_type


class Tote(SportRacingPageBase):
    _url_pattern = r'^http[s]?:\/\/.+\/tote(?!\/event)'
    _tab_content = 'xpath=.//tote-sport | .//tote-tabs-results'
    _tab_content_type = ToteTabContent
    _tabs_menu = 'xpath=.//*[contains(@data-crlat, "panel.tabs") and not(contains(@class, "ng-hide"))]'
    _tabs_menu_type = TabsMenu
