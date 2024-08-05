from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.pages.shared.components.competions_selector_dropdown import CompetitionSelector
from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.competitions_list_dropdown import CompetitionListDropDown
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_active_selector


class TitleSection(ComponentBase):
    _type_name = 'xpath=.//*[@data-crlat="typeName"]'
    _competition_selector = 'xpath=.//*[@data-crlat="changeCompetition"]'

    @property
    def type_name(self):
        return TextBase(selector=self._type_name, context=self._we)

    @property
    def competition_selector_link(self):
        return ButtonBase(selector=self._competition_selector, context=self._we)


class CompetitionLeagueFixtureHeader(FixtureHeader):
    _date = 'xpath=.//*[@data-crlat="dateTitle"]'

    @property
    def date(self):
        return self._get_webelement_text(selector=self._date)


class CompetitionLeagueEventGroup(EventGroup):
    _fixture_header_type = CompetitionLeagueFixtureHeader

    @property
    def name(self):
        return self.fixture_header.date

    def expand(self):
        self._logger.warning('*** Accordions on Competition League page are not expandable')

    def collapse(self):
        self._logger.warning('*** Accordions on Competition League page are not collapsible')


class CompetitionLeagueEvents(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="competitionLeague.item"]'
    _list_item_type = CompetitionLeagueEventGroup


class CompetitionsMatchesTabContent(TabContent):
    _accordions_list_type = CompetitionLeagueEvents

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._selector,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=5)
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector)


class CompetitionsOutrightsTabContent(TabContent):
    _event_league = 'xpath=.//*[@data-crlat="couponName"]'

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._event_league,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=5)
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def event_league(self):
        return ButtonBase(selector=self._event_league)


class CompetitionsStandingsTabContent(TabContent):
    _results_table = 'xpath=.//*[@data-crlat="resultRows"]'
    _previous_arrow = 'xpath=.//*[@data-crlat="goToPrev"]'
    _next_arrow = 'xpath=.//*[@data-crlat="goToNext"]'
    _name = 'xpath=.//*[@data-crlat="resultTableName"]'
    _header_title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _headers = 'tag=th'
    _show_button = 'xpath=.//*[@data-crlat="showAllButton"]'
    _table_row = 'xpath=.//tbody/tr'

    @property
    def season_name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def header_label(self):
        return self._get_webelement_text(selector=self._header_title)

    @property
    def table_headers(self):
        table_headers = []
        headers = self._find_elements_by_selector(selector=self._headers)
        for header in headers:
            table_headers.append(header.text)
        return table_headers

    @property
    def row_number(self):
        return len(self._find_elements_by_selector(selector=self._table_row))

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._results_table,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=5)
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def results_table(self):
        return ComponentBase(selector=self._results_table)

    @property
    def previous_arrow(self):
        return ComponentBase(selector=self._previous_arrow)

    @property
    def next_arrow(self):
        return ComponentBase(selector=self._next_arrow)


class CompetitionLeaguePage(SportRacingPageBase):
    # _url_pattern = r'^http[s]?:\/\/.+\/(football|tennis|basketball)\/[a-z\.-]*\/[\w\-\.%\s]+'
    # Note: URL pattern is commented to use CompetitonLeaguePage Class for all other Sports.
    _title_section = 'xpath=.//*[@data-crlat="title"]'
    _title_section_type = TitleSection
    _competition_list = 'xpath=.//*[@data-crlat="competitionListContainer"]'
    _a_z_competition_list = 'xpath=.//*[@data-crlat="competitionItem"]'
    _competitions_selector = 'xpath=.//*[@data-crlat="dropdownMenu"]'
    _tab_sports_selector = 'tag=competitions-sport-tab'
    _tab_matches_selector = 'tag=competitions-matches-tab'
    _tab_outrights_selector = 'tag=competitions-outrights-tab'
    _tab_results_selector = 'tag=competitions-results-tab'
    _tab_standings_selector = 'tag=competitions-standings-tab'
    _fade_out_overlay = True
    _verify_spinner = True
    _tab_content_types = {
        _tab_sports_selector: CompetitionsMatchesTabContent,
        _tab_matches_selector: CompetitionsMatchesTabContent,
        _tab_outrights_selector: CompetitionsOutrightsTabContent,
        _tab_results_selector: TabContent,
        _tab_standings_selector: CompetitionsStandingsTabContent
    }
    _a_z_competition_label = 'xpath=.//*[@class="inter"] | .//*[@class="split-header"]'
    _bet_button = 'xpath=.//*[@data-crlat="oddsPrice"]'

    @property
    def bet_buttons(self):
        return self._find_elements_by_selector(selector=self._bet_button, context=self._we)

    @property
    def a_z_competition_label(self):
        return self._find_element_by_selector(selector=self._a_z_competition_label)

    @property
    def competitions_selector(self):
        return CompetitionSelector(selector=self._competitions_selector, context=self._we)

    @property
    def competition_list(self):
        return CompetitionListDropDown(selector=self._competition_list, context=self._we)

    @property
    def a_z_competition_list(self):
        return CompetitionListDropDown(selector=self._a_z_competition_list, context=self._we)

    @property
    def title_section(self):
        return self._title_section_type(selector=self._title_section, context=self._we)

    @property
    def current_tab_content(self):
        active_selector = get_active_selector(list(self._tab_content_types.keys()), timeout=5)
        tab_content_type = self._tab_content_types.get(active_selector)
        if tab_content_type:
            return tab_content_type, active_selector
        else:
            raise VoltronException('Tab content was not defined')

    @property
    def tab_content(self):
        tab_content_type, active_selector = self.current_tab_content
        selector = next((selector for selector, tab_content_class in self._tab_content_types.items()
                         if tab_content_class == tab_content_type and selector == active_selector), None)

        if selector:
            return tab_content_type(selector)
        else:
            raise VoltronException('Tab content selector was not defined')
