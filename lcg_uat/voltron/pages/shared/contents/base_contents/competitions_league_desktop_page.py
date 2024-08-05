from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.market_selector_drop_down_desktop import MarketSelectorDesktopDropDown
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.competitions_league_page import CompetitionLeaguePage
from voltron.pages.shared.contents.competitions_league_page import CompetitionsMatchesTabContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class ResultWidgetSection(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class ResultsWidget(Accordion):
    _item = 'xpath=.//odds-card-result-component'
    _header_title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _show_button = 'xpath=.//*[@data-crlat="showAllButton"]'
    _list_item_type = ResultWidgetSection
    _team_1 = 'xpath=.//*[@data-crlat="firstTeam"]'
    _team_2 = 'xpath=.//*[@data-crlat="secondTeam"]'
    _team_1_score = 'xpath=.//*[@data-crlat="firstTeamScore"]'
    _team_2_score = 'xpath=.//*[@data-crlat="secondTeamScore"]'
    _team_1_scorer = 'xpath=.//*[@data-crlat="firstTeamScorers"]'
    _team_2_scorer = 'xpath=.//*[@data-crlat="secondTeamScorers"]'

    @property
    def header_label(self):
        return self._get_webelement_text(selector=self._header_title, context=self._we)

    @property
    def team1(self):
        return self._get_webelement_text(selector=self._team_1, context=self._we)

    @property
    def team2(self):
        return self._get_webelement_text(selector=self._team_2, context=self._we)

    @property
    def team1_score(self):
        return self._get_webelement_text(selector=self._team_1_score, context=self._we)

    @property
    def team2_score(self):
        return self._get_webelement_text(selector=self._team_2_score, context=self._we)

    @property
    def team1_scorer(self):
        return self._get_webelement_text(selector=self._team_1_scorer, context=self._we)

    @property
    def team2_scorer(self):
        return self._get_webelement_text(selector=self._team_2_scorer, context=self._we)

    @property
    def show_button(self):
        return ButtonBase(selector=self._show_button, context=self._we)


class StandingsWidgetSubTabItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="tab"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)


class StandingsWidgetSubTabs(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="tab.tpTabs"]'
    _list_item_type = StandingsWidgetSubTabItem
    _selected_item = 'xpath=.//*[@data-crlat="tab.tpTabs" and contains(@class, "active")]'

    @property
    def selected_item(self):
        return wait_for_result(lambda: self._list_item_type(selector=self._selected_item).name,
                               name='Event off time string',
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                               timeout=3)


class StandingsWidget(Accordion):
    _name = 'xpath=.//*[@data-crlat="resultTableName"]'
    _previous_arrow = 'xpath=.//*[@data-crlat="goToPrev"]'
    _next_arrow = 'xpath=.//*[@data-crlat="goToNext"]'
    _header_title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _headers = 'tag=th'
    _show_button = 'xpath=.//*[@data-crlat="showAllButton"]'
    _table_row = 'xpath=.//tbody/tr'
    _sub_tabs = 'xpath=.//*[@data-crlat="tabs"]'
    _sub_tabs_type = StandingsWidgetSubTabs
    _selected_item = 'xpath=.//*[@data-crlat="tab.tpTabs" and contains(@class, "active")]'
    _no_events_label = 'xpath=.//*[@data-crlat="noEventsFound"]'

    def has_no_events_label(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._no_events_label, timeout=0) is not None,
                               name=f'{self.__class__.__name__} "No events" label status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def sub_tabs(self):
        return StandingsWidgetSubTabs(selector=self._sub_tabs, context=self._we, timeout=3)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        # coral widget has just different structure than usual
        we = self._find_element_by_selector(selector='xpath=.//*[@data-crlat="accordion"]', timeout=timeout)

        result = wait_for_result(lambda: 'is-expanded' in we.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    @property
    def season_name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def previous_arrow(self):
        return ComponentBase(selector=self._previous_arrow)

    @property
    def next_arrow(self):
        return ComponentBase(selector=self._next_arrow)

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
    def show_button(self):
        return ButtonBase(selector=self._show_button)

    def has_show_button(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_button, timeout=0) is not None,
                               name=f'{self.__class__.__name__} "Show All" button status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def row_number(self):
        return len(self._find_elements_by_selector(selector=self._table_row))


class TitleSectionDesktop(ComponentBase):
    _type_name = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _competition_selector = 'xpath=.//*[@data-crlat="dropdown"]'

    @property
    def type_name(self):
        return TextBase(selector=self._type_name, context=self._we)

    @property
    def competition_selector_link(self):
        return ButtonBase(selector=self._competition_selector, context=self._we)


class CompetitionsMatchesTabContentDesktop(CompetitionsMatchesTabContent):
    _dropdown_market_selector_type = MarketSelectorDesktopDropDown


class CompetitionsOutrightsTabContentDesktop(TabContent, Accordion):
    _accordions_list = 'xpath=.//competitions-outrights-tab-one-event | .//competitions-outrights-tab-multiple-events'


class CompetitionLeagueDesktopPage(CompetitionLeaguePage):
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers"]'
    _tab_content = 'xpath=.//*[@data-crlat="tabContent"]'

    _title_section = 'xpath=.//*[@data-crlat="topBar"]'
    _title_section_type = TitleSectionDesktop

    _standings_widget = 'xpath=.//*[@data-crlat="tableWidget"]'
    _results_widget = 'xpath=.//results-widget'

    @property
    def standings_widget(self):
        return StandingsWidget(selector=self._standings_widget)

    @property
    def results_widget(self):
        return ResultsWidget(selector=self._results_widget)

    @property
    def tab_content(self):
        if self._find_element_by_selector(selector=self._tab_sports_selector, timeout=1):
            return CompetitionsMatchesTabContentDesktop(selector=self._tab_sports_selector)
        elif self._find_element_by_selector(selector=self._tab_matches_selector, timeout=1):
            return CompetitionsMatchesTabContentDesktop(selector=self._tab_matches_selector)
        elif self._find_element_by_selector(selector=self._tab_outrights_selector, timeout=1):
            return CompetitionsOutrightsTabContentDesktop(selector=self._tab_outrights_selector)
        else:
            raise VoltronException('Tab content was not defined')

    @property
    def title_section(self):
        return self._title_section_type(selector=self._title_section, context=self._we)
