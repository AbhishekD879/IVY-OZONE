from selenium.webdriver.support.select import Select
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.components.base import ComponentBase


class Season(ComponentBase):

    @property
    def selected_item(self):
        select = Select(self._we)
        return select.first_selected_option.text

    def select_by_text(self, text):
        select = Select(self._we)
        select.select_by_visible_text(text=text)


class Competitions(ComponentBase):
    _prev = 'xpath=.//*[@data-crlat="goToPrev"]'
    _next = 'xpath=.//*[@data-crlat="goToNext"]'
    _name = 'xpath=.//*[@data-crlat="competitionName"]'

    @property
    def previous_competition(self):
        self.scroll_to_we(web_element=self._we)
        return self._find_element_by_selector(selector=self._prev, context=self._we)

    @property
    def next_competition(self):
        self.scroll_to_we(web_element=self._we)
        return self._find_element_by_selector(selector=self._next, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class TableHead(ComponentBase):
    pass


class TableBody(ComponentBase):
    pass


class Table(ComponentBase):
    _head = 'xpath=.//thead'
    _head_type = TableHead
    _body = 'xpath=.//tbody'
    _body_type = TableBody

    @property
    def head(self):
        return self._head_type(selector=self._head)

    @property
    def body(self):
        return self._body_type(selector=self._body)


class Results(ComponentBase):
    _table = 'xpath=.//table'
    _table_type = Table

    @property
    def table(self):
        return self._find_element_by_selector(selector=self._table)


class LeaguePage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/leagues\/.+'
    _search_leagues_button = 'xpath=.//*[@data-crlat="statsSearchLeagues"]'
    _league_name = 'xpath=.//*[@data-crlat="area"]'
    _competitions = 'xpath=.//*[@data-crlat="competitions"]'
    _competitions_type = Competitions
    _results = 'xpath=.//*[@data-crlat="resultsLength"]'
    _results_type = Results
    _season = 'xpath=.//*[@data-crlat="seasons"]'
    _season_type = Season

    @property
    def search_leagues_button(self):
        return ButtonBase(selector=self._search_leagues_button)

    @property
    def league_name(self):
        return self._get_webelement_text(selector=self._league_name)

    @property
    def competitions(self):
        return self._competitions_type(selector=self._competitions)

    @property
    def results(self):
        return self._results_type(selector=self._results)

    @property
    def season(self):
        return self._season_type(selector=self._season)
