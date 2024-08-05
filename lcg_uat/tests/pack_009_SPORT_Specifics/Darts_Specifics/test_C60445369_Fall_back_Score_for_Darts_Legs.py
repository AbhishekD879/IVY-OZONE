import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Can not create events on prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C60445369_Fall_back_Score_for_Darts_Legs(BaseFallbackScoreboardTest):
    """
    TR_ID: C60445369
    NAME: Fall back Score for Darts Legs
    DESCRIPTION: List of pages to be checked:
    DESCRIPTION: In-play Home Page https://sports.coral.co.uk/home/in-play
    DESCRIPTION: In-play /All Sports https://sports.coral.co.uk/in-play/watchlive
    DESCRIPTION: In-Play/Sports https://sports.coral.co.uk/in-play/cricket
    DESCRIPTION: Sports - Matches Tab https://sports.coral.co.uk/sport/football/matches/today
    DESCRIPTION: Sports -In-play Tab https://sports.coral.co.uk/sport/football/live
    DESCRIPTION: Note : CMS changes should be present as per below Document.
    DESCRIPTION: https://coralracing-my.sharepoint.com/:w:/g/personal/animisha_uppuluri_ivycomptech_com/EX9s5-XmNhREhoyRIoN1VYcBVWRHVPpI3MMVhZ4u4UOkiw?email=Animisha.Uppuluri%40ivycomptech.com&e=4%3A0LdMbH&at=9&CID=AC96F282-B011-45FF-AAE0-76C75E7EE4BB&wdLOR=c6B47E59E-DA9E-428D-BAD5-983F641BFDB1
    PRECONDITIONS: This template will apply to any event where there is not an Opta / Bwin fed scoreboard where the string in the event name appears as
    PRECONDITIONS: Player A* (1) 0-0 (0) Player B
    PRECONDITIONS: Sets score is represented by the bracket x bracket within this string. and the Legs are taken from the x-x format within the middle of the string.
    PRECONDITIONS: If no score is passed within the event name or removed from the event name then the scoreboard layout should be removed.
    PRECONDITIONS: Serve Indicators - The serve indicator should be shown as per the GD. The indicator of serve (if applicable) is passed in the string and will show as an * against the Player/Team name
    PRECONDITIONS: Team/Player A* (0) 0-3 (1) Team/Player B
    """
    keep_browser_open = True
    set_legs_indicator_score = {'current': '* (0)1-6(1) '}
    legs_indicator_score = {'current': '* 1-6 '}
    legs_score = {'current': ' 1-6 '}
    team1 = 'Kennedy Gerlach/Jones Wachaczyk'
    team2 = 'John Heisen/Harry Hobgarski'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.darts_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.darts_config.category_id)
        self.check_sport_presence_on_inplay(sport_name='darts')
        set_legs_indicator_event = self.ob_config.add_darts_event_to_darts_all_darts(
            score=self.set_legs_indicator_score,
            is_live=True,
            perform_stream=True)
        self.__class__.set_legs_indicator_team1 = set_legs_indicator_event.team1
        self.__class__.set_legs_indicator_team2 = set_legs_indicator_event.team2

        legs_indicator_event = self.ob_config.add_darts_event_to_darts_all_darts(
            score=self.legs_indicator_score,
            is_live=True,
            perform_stream=True)

        self.__class__.legs_indicator_team1 = legs_indicator_event.team1
        self.__class__.legs_indicator_team2 = legs_indicator_event.team2

        legs_no_indicator_event = self.ob_config.add_darts_event_to_darts_all_darts(
            score=self.legs_score,
            is_live=True,
            perform_stream=True)

        self.__class__.legs_no_indicator_team1 = legs_no_indicator_event.team1
        self.__class__.legs_no_indicator_team2 = legs_no_indicator_event.team2

        preplay_event = self.ob_config.add_darts_event_to_darts_all_darts(is_live=True, perform_stream=True)
        long_name_event = self.ob_config.add_darts_event_to_darts_all_darts(team1=self.team1, team2=self.team2,
                                                                            score=self.set_legs_indicator_score,
                                                                            is_live=True,
                                                                            perform_stream=True)

        self.__class__.set_legs_indicator_event_id = set_legs_indicator_event.event_id
        self.__class__.legs_indicator_event_id = legs_indicator_event.event_id
        self.__class__.legs_no_indicator_event_id = legs_no_indicator_event.event_id
        self.__class__.preplay_event_id = preplay_event.event_id
        self.__class__.long_name_event_id = long_name_event.event_id
        self.__class__.set_legs_indicator_event1 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.set_legs_indicator_event_id,
            query_builder=self.ss_query_builder)
        self.__class__.legs_indicator_event1 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.legs_indicator_event_id,
            query_builder=self.ss_query_builder)
        self.__class__.legs_no_indicator_event1 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.legs_no_indicator_event_id,
            query_builder=self.ss_query_builder)
        self.__class__.long_name_event1 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.long_name_event_id,
            query_builder=self.ss_query_builder)

    def test_001_verify_that_darts_basic_score_board_with_no_serve_indicator(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With No Serve Indicator
        EXPECTED: String should be Team/Player A 0-3 B Team/Player without serve indicator
        """
        self.navigate_to_edp(event_id=self.legs_no_indicator_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        title = self.site.sport_event_details.scoreboard_title_bar
        self.assertFalse(title.has_serving_ball_icon_home_team(), msg='Serving ball icon is not shown')
        expected_event_name = f'{self.legs_no_indicator_team1}  1-6  {self.legs_no_indicator_team2}'
        actual_event_name = self.legs_no_indicator_event1[0]['event']['name']
        self.assertEqual(expected_event_name, actual_event_name,
                         msg=f'Actual : {actual_event_name} Expected : {expected_event_name}')

    def test_002_verify_that_darts_basic_score_board_with_serve_indicator_with_legs(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With Serve Indicator with Legs
        EXPECTED: String should be Team/Player A* 0-3 Team/Player B with serve indicator
        EXPECTED: ![](index.php?/attachments/get/128017834)
        """
        self.navigate_to_edp(event_id=self.legs_indicator_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        title = self.site.sport_event_details.scoreboard_title_bar
        self.assertTrue(title.has_serving_ball_icon_home_team(), msg='Serving ball icon is not shown')
        expected_event_name = f'{self.legs_indicator_team1} * 1-6  {self.legs_indicator_team2}'
        actual_event_name = self.legs_indicator_event1[0]['event']['name']
        self.assertEqual(expected_event_name, actual_event_name,
                         msg=f'Actual : {actual_event_name} Expected : {expected_event_name}')

    def test_003_verify_that_darts_basic_score_board_with_serve_indicator_with_sets__legs(self):
        """
        DESCRIPTION: Verify that Darts basic Score Board With Serve Indicator with Sets & Legs
        EXPECTED: String should be Team/Player A* (0) 0-3 (1) Team/Player B with serve indicator
        EXPECTED: ![](index.php?/attachments/get/122183505)
        """
        self.navigate_to_edp(event_id=self.set_legs_indicator_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        title = self.site.sport_event_details.scoreboard_title_bar
        self.assertTrue(title.has_serving_ball_icon_home_team(), msg='Serving ball icon is not shown')

        expected_event_name = f'{self.set_legs_indicator_team1} * (0)1-6(1)  {self.set_legs_indicator_team2}'
        actual_event_name = self.set_legs_indicator_event1[0]['event']['name']
        self.assertEqual(expected_event_name, actual_event_name,
                         msg=f'Actual : {actual_event_name} Expected : {expected_event_name}')

    def test_004_verify_that_there_is_no_score_for_the_match(self):
        """
        DESCRIPTION: Verify that there is no score for the match
        EXPECTED: Should show:
        EXPECTED: - players name
        EXPECTED: - start and date time
        EXPECTED: ![](index.php?/attachments/get/122183499)
        """
        self.navigate_to_edp(event_id=self.preplay_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        players_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertTrue(players_name, msg='Players names not displayed on the EDP')
        date_time = self.site.sport_event_details.event_title_bar.event_time
        self.assertTrue(date_time, msg='start and date time is not displayed')

    def test_005_verify_that_for_double_and_long_name_truncation_is_applied(self):
        """
        DESCRIPTION: Verify that for double and long name truncation is applied
        EXPECTED: K. Gerlach/J. Wachaczyk* (0) 1-1 (0) V. Heisen/K. Hobgarski
        EXPECTED: For long and doubles name truncation should applied as on scoreboards
        """
        self.navigate_to_edp(event_id=self.long_name_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertTrue(event_name, msg='Players names not displayed on the EDP')
