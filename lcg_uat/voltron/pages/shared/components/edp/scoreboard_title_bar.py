from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class ScoreTitleBar(ComponentBase):
    _home_team_name = 'xpath=.//*[@data-crlat="teamH"]'
    _away_team_name = 'xpath=.//*[@data-crlat="teamA"]'
    _home_team_serving_ball_icon = 'xpath=.//*[@data-crlat="possH"]'

    @property
    def event_name(self):
        return self._get_webelement_text(we=self._we).replace('\n', ' ')

    @property
    def event_name_without_scores(self):
        return f'{self.home_team_name} v {self.away_team_name}'

    @property
    def home_team_name(self):
        return self._get_webelement_text(selector=self._home_team_name)

    @property
    def away_team_name(self):
        return self._get_webelement_text(selector=self._away_team_name)

    def has_serving_ball_icon_home_team(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._home_team_serving_ball_icon,
                                                   timeout=0) is not None,
            name=f'Serving ball status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def event_time(self):
        raise NotImplementedError(f'Event time property is not present on {self.__class__.__name__}')

    @property
    def live_now_icon(self):
        raise NotImplementedError(f'Live now icon property is not present on {self.__class__.__name__}')

    @property
    def is_live_now_event(self):
        raise NotImplementedError(f'Is live now event property is not present on {self.__class__.__name__}')

    @property
    def event_time_icon(self):
        raise NotImplementedError(f'Event time icon property is not present on {self.__class__.__name__}')
