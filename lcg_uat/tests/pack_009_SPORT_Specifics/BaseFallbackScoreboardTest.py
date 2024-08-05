from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_score_update_from_inplay_ms, get_inplay_event_initial_data
from voltron.utils.waiters import wait_for_result


class BaseFallbackScoreboardTest(BaseSportTest):
    home_score_expected = '1'
    away_score_expected = '3'
    score = {'current': f'{home_score_expected}-{away_score_expected}'}
    new_home_score = '12'
    new_away_score = '10'
    resp_type = 'SCBRD'
    is_mobile = None
    home_set_scores = '1'
    away_set_scores = '1'
    home_game_score = '2'
    away_game_score = '2'
    final_home_score = '5'

    def verify_event_score_template(self, events: dict, serving_ball: bool = False, **kwargs) -> None:
        """
        This method verifies that Live scores are shown after editing/updating through OB name template
        :param events: list of events
        :param expected_home_score: Expected score for home player
        :param expected_away_score: Expected score for away player
        :param points_score: True if score template with points
        :param serving_ball: True if event has serving icon
        """
        event_name = kwargs.get('event_name', self.event_name)
        actual_event = events.get(event_name)
        self.assertTrue(actual_event, msg=f'"{event_name}" event not found among: {list(events.keys())}')
        expected_home_score = kwargs.get('expected_home_score', '')
        expected_away_score = kwargs.get('expected_away_score', '')

        expected_player1_points_score = kwargs.get('expected_player1_points_score', '')
        expected_player2_points_score = kwargs.get('expected_player2_points_score', '')

        expected_player1_game_score = kwargs.get('expected_player1_game_score', '')
        expected_player2_game_score = kwargs.get('expected_player2_game_score', '')

        if expected_home_score and expected_away_score:
            home_score_result = wait_for_result(lambda: events.get(event_name).score_table.match_score.home_score == expected_home_score,
                                                name=f'Home team score changed to {expected_home_score}',
                                                bypass_exceptions=(VoltronException, StaleElementReferenceException, AttributeError),
                                                timeout=5)
            self.assertTrue(home_score_result, msg=f'Actual score value "{events.get(event_name).score_table.match_score.home_score}" '
                                                   f'for Home team is not the same as expected: "{expected_home_score}"')

            home_score_result = wait_for_result(lambda: events.get(event_name).score_table.match_score.away_score == expected_away_score,
                                                name=f'Away team score changed to {expected_away_score}',
                                                bypass_exceptions=(
                                                VoltronException, StaleElementReferenceException, AttributeError),
                                                timeout=5)
            self.assertTrue(home_score_result, msg=f'Actual score value "{events.get(event_name).score_table.match_score.away_score}" '
                                                   f'for Away team is not the same as expected: "{expected_away_score}"')
        if expected_player1_points_score and expected_player2_points_score:
            player1_points_result = wait_for_result(lambda: events.get(event_name).score_table.points_score.home_score == expected_player1_points_score,
                                                    name=f'Player 1 points changed to {expected_player1_points_score}',
                                                    bypass_exceptions=(
                                                    VoltronException, StaleElementReferenceException, AttributeError),
                                                    timeout=5)
            self.assertTrue(player1_points_result, msg=f'Actual points value "{events.get(event_name).score_table.points_score.home_score}" '
                                                       f'for Player 1 is not the same as expected: "{expected_player1_points_score}"')

            player2_points_result = wait_for_result(lambda: events.get(event_name).score_table.points_score.away_score == expected_player2_points_score,
                                                    name=f'Player 2 points changed to {expected_player2_points_score}',
                                                    bypass_exceptions=(
                                                    VoltronException, StaleElementReferenceException, AttributeError),
                                                    timeout=5)
            self.assertTrue(player2_points_result, msg=f'Actual points value "{events.get(event_name).score_table.points_score.away_score}" '
                                                       f'for Away team is not the same as expected: "{expected_player2_points_score}"')

        if expected_player1_game_score and expected_player2_game_score:
            player1_game_result = wait_for_result(lambda: events.get(event_name).score_table.game_score.home_score == expected_player1_game_score,
                                                  name=f'Player 1 game score changed to {expected_player1_game_score}',
                                                  bypass_exceptions=(
                                                  VoltronException, StaleElementReferenceException, AttributeError),
                                                  timeout=5)
            self.assertTrue(player1_game_result, msg=f'Actual game score value "{events.get(event_name).score_table.game_score.home_score}" '
                                                     f'for Player 1 is not the same as expected: "{expected_player1_game_score}"')

            player2_game_result = wait_for_result(lambda: events.get(event_name).score_table.game_score.away_score == expected_player2_game_score,
                                                  name=f'Player 2 game score changed to {expected_player2_game_score}',
                                                  bypass_exceptions=(
                                                  VoltronException, StaleElementReferenceException, AttributeError),
                                                  timeout=5)
            self.assertTrue(player2_game_result, msg=f'Actual game score value "{events.get(event_name).score_table.game_score.away_score}" '
                                                     f'for Away team is not the same as expected: "{expected_player2_game_score}"')

        if serving_ball:
            self.softAssert(self.assertTrue, actual_event.has_serving_ball_icon(timeout=3),
                            msg='Serving ball icon is not shown')

    def get_scores_from_initial_data(self, category_id: str, event_id: str, delimiter: str = '42', timeout=40):
        expected_scores = {}
        result = wait_for_result(
            lambda: get_inplay_event_initial_data(category_id=category_id, delimiter=delimiter, event_id=event_id),
            timeout=timeout,
            name=f'WS message for {event_id} with category id {category_id} to appear',
            bypass_exceptions=(KeyError, ))
        self.assertTrue(result,
                        msg=f'WS message for {event_id} with category id {category_id} is not received')
        if not result[0].get('comments'):
            raise CmsClientException(f'Seems FallBack Scoreboards are not configured for category "{category_id}",'
                                     f' check BipScoreEvents setting in CMS system config structure')
        selections = result[0]['comments']['teams']
        for selection_name, selection_info in selections.items():
            expected_scores[selection_name] = selection_info['score']
        if result[0]['comments'].get('runningSetIndex') and result[0]['comments'].get('setsScores'):
            running_set_index = result[0]['comments']['runningSetIndex']
            expected_scores['running_set_score'] = {}
            for score_name, score_value in result[0]['comments']['setsScores'][str(running_set_index)].items():
                expected_scores['running_set_score'][score_name] = score_value
        return expected_scores

    def wait_for_score_update_from_inplay_ms(self, event_id: str, score: str, team: str, delimiter='42', score_type='ALL', timeout=70):
        """
        To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
        :param score: New Expected/changed score for home player
        :param team: Team name (home or away)
        :param delimiter: By default delimiter is 42
        """
        result = wait_for_result(
            lambda: get_score_update_from_inplay_ms(event_id=event_id, delimiter=delimiter, resp_type=self.resp_type,
                                                    score=score, team=team, score_type=score_type),
            poll_interval=1,
            timeout=timeout,
            name=f'WS message for {event_id} with type {self.resp_type}, team {team}, updated score {score} to appear',
            bypass_exceptions=(KeyError,))
        self._logger.info(f'{result}')
        self.assertTrue(result, msg=f'WS message for {event_id} with type {self.resp_type}, team {team}, updated score {score} is not received')

        selections = list(result['event']['scoreboard'][score_type])
        for selection in selections:
            if selection['role_code'] == team.upper():
                score_from_response = selection.get('value', '')
                self.assertEqual(score_from_response, score,
                                 msg=f'Actual response value home score "{score_from_response}" is not as expected "{score}"')
        return result

    def check_fallback_scoreboard_is_configured_for_sport(self, category_id):
        configured_categories = []
        fallback_scoreboard = self.get_initial_data_system_configuration().get('FallbackScoreboard')
        if not fallback_scoreboard:
            fallback_scoreboard = self.cms_config.get_system_configuration_item('FallbackScoreboard')
        if fallback_scoreboard:
            if fallback_scoreboard.get('enabled'):
                if fallback_scoreboard.get('Simple'):
                    configured_categories.extend(fallback_scoreboard.get('Simple').split(','))
                if fallback_scoreboard.get('GAA'):
                    configured_categories.extend(fallback_scoreboard.get('GAA').split(','))
                if fallback_scoreboard.get('SetsPoints'):
                    configured_categories.extend(fallback_scoreboard.get('SetsPoints').split(','))
                if fallback_scoreboard.get('SetsGamesPoints'):
                    configured_categories.extend(fallback_scoreboard.get('SetsGamesPoints').split(','))
                if fallback_scoreboard.get('BoxScore'):
                    configured_categories.extend(fallback_scoreboard.get('BoxScore').split(','))
        else:
            raise CmsClientException('Fallback Scoreboards are not configured is CMS')
        if str(category_id) not in configured_categories:
            raise CmsClientException(f'Fallback Scoreboards are not configured in CMS '
                                     f'for "{category_id}" sport category')

    def check_bip_score_is_configured_for_sport(self, category_id):
        configured_categories = []
        bip_score_events = self.get_initial_data_system_configuration().get('BipScoreEvents')
        if not bip_score_events:
            bip_score_events = self.cms_config.get_system_configuration_item('BipScoreEvents')
        if bip_score_events:
            for category, status in bip_score_events.items():
                if status:
                    configured_categories.append(category)
        else:
            raise CmsClientException('BIP Score Events are not configured is CMS')
        if str(category_id) not in configured_categories:
            raise CmsClientException(f'BIP Score Events are not configured in CMS for sport category "{category_id}"')

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.device_type == 'mobile' and tests.settings.cms_env != 'prd0':
            cms_config = cls.get_cms_config()
            if cls.in_play_event_count is not None:
                cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
            if cls.sport_number is not None and cls.sport_event_count is not None:
                cms_config.update_inplay_sport_event_count(sport_number=cls.sport_number,
                                                           event_count=cls.sport_event_count)
