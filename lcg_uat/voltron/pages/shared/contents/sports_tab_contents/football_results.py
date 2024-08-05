from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroupHeader, EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class Match(ComponentBase):
    _first_team = 'xpath=.//*[@data-crlat="firstTeam"]'
    _first_score = 'xpath=.//*[@data-crlat="firstTeamScore"]'
    _first_scorers = 'xpath=.//*[@data-crlat="firstTeamScorers"]'
    _second_team = 'xpath=.//*[@data-crlat="secondTeam"]'
    _second_score = 'xpath=.//*[@data-crlat="secondTeamScore"]'
    _second_scorers = 'xpath=.//*[@data-crlat="secondTeamScorers"]'

    @property
    def first_team(self):
        return self._get_webelement_text(selector=self._first_team, timeout=2)

    @property
    def first_score(self):
        return self._get_webelement_text(selector=self._first_score, timeout=2)

    @property
    def first_scorers(self):
        return self._get_webelement_text(selector=self._first_scorers, timeout=2)

    @property
    def second_team(self):
        return self._get_webelement_text(selector=self._second_team, timeout=2)

    @property
    def second_score(self):
        return self._get_webelement_text(selector=self._second_score, timeout=2)

    @property
    def second_scorers(self):
        return self._get_webelement_text(selector=self._second_scorers, timeout=2)


class CompetitionHeader(EventGroupHeader):
    _title = 'xpath=.//*[@data-crlat="competition.name"]'


class Competition(EventGroup):
    _header_type = CompetitionHeader
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _item = 'xpath=.//*[@data-crlat="competitionItem"]'
    _list_item_type = Match


class DayGroup(AccordionsList, EventGroup):
    _list_item_type = Competition


class ResultsEventsAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="accordion" and not(contains(@class, "page-inner-container"))]'
    _list_item_type = DayGroup


class ResultsTabContent(TabContent):
    _accordions_list_type = ResultsEventsAccordionsList
    _show_more_button = 'xpath=.//*[@data-crlat="showMoreDates"]'

    @property
    def has_show_more_button(self):
        return ButtonBase(selector=self._show_more_button, context=self._we).is_displayed(
            timeout=2, name='Show All button is not displayed')

    @property
    def show_more_button(self):
        return ButtonBase(selector=self._show_more_button)
