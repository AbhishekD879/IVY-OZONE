from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import get_shadow_root


class OptaScoreboardTitleBar(ComponentBase):
    _match_score = 'tag=match-score'
    _match_start = 'tag=match-start'
    _home_team = 'id=homeTeam'
    _away_team = 'id=awayTeam'
    _event_time = 'id=startTime'

    @property
    def event_name(self):
        match_score = self._find_element_by_selector(selector=self._match_score)
        if not match_score:
            raise VoltronException(f'Element "{self._match_score}" not found in Opta scoreboard bar')
        match_score_context = get_shadow_root(match_score)
        if not match_score_context:
            raise VoltronException(f'Shadow root for "{self._match_score}" not found in Opta scoreboard bar')
        team1 = self._get_webelement_text(selector=self._home_team, context=match_score_context, timeout=1)
        team2 = self._get_webelement_text(selector=self._away_team, context=match_score_context, timeout=1)

        return f'{team1} v {team2}'

    @property
    def event_name_without_scores(self):
        return self.event_name

    @property
    def event_time(self):
        match_start = self._find_element_by_selector(selector=self._match_start)
        if not match_start:
            raise VoltronException(f'Element "{self._match_start}" not found in Opta scoreboard bar')
        match_start_context = get_shadow_root(match_start)
        if not match_start_context:
            raise VoltronException(f'Shadow root for "{self._match_score}" not found in Opta scoreboard bar')
        event_time = self._get_webelement_text(selector=self._event_time, context=match_start_context, timeout=1)
        return event_time

    @property
    def live_now_icon(self):
        raise NotImplementedError(f'Live now icon property is not present on {self.__class__.__name__}')

    @property
    def is_live_now_event(self):
        raise NotImplementedError(f'Is live now event property is not present on {self.__class__.__name__}')

    @property
    def event_time_icon(self):
        raise NotImplementedError(f'Event time icon property is not present on {self.__class__.__name__}')
