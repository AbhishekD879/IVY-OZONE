from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class ScoreColumn(ComponentBase):
    _score_home = 'xpath=.//*[@data-crlat="scoreH"]'
    _score_away = 'xpath=.//*[@data-crlat="scoreA"]'
    _timeout = 2

    @property
    def name(self):
        return f'{self.home_score} - {self.away_score}'

    @property
    def home_score(self):
        return self._get_webelement_text(selector=self._score_home, timeout=1)

    def home_score_element(self):
        return self._find_element_by_selector(selector=self._score_home, timeout=1)

    @property
    def away_score(self):
        return self._get_webelement_text(selector=self._score_away, timeout=1)

    def away_score_element(self):
        return self._find_element_by_selector(selector=self._score_away, timeout=1)


class ScoreTable(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="scoreColumn"]'
    _list_item_type = ScoreColumn
    _timeout = 2

    # Tennis template SGP (Sets Games Points)
    @property
    def sets_score(self):
        items = self.items
        if len(items) == 3:
            return items[0]
        else:
            raise VoltronException('Sets score is not available')

    # Template SP (Sets Points)
    @property
    def sets_score_for_sp(self):
        items = self.items
        if len(items) == 2:
            return items[0]
        else:
            raise VoltronException('Sets score is not available')

    @property
    def game_score(self):
        items = self.items
        if len(items) == 3:
            return items[1]
        elif len(items) == 2:
            return items[0]
        else:
            raise VoltronException('Game score is not available')

    @property
    def points_score(self):
        items = self.items
        if len(items) == 3:
            return items[2]
        elif len(items) == 2:
            return items[1]
        else:
            raise VoltronException('Points score is not available')

    # Football, Baseball, Handball, Ice Hockey template
    @property
    def match_score(self):
        items = self.items
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return items[0]
        else:
            raise VoltronException('Match score is not available')
