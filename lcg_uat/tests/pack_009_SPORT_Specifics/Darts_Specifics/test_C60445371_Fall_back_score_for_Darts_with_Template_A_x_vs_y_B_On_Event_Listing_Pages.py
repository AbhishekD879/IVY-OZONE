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
class Test_C60445371_Fall_back_score_for_Darts_with_Template_A_x_vs_y_B_On_Event_Listing_Pages(BaseFallbackScoreboardTest):
    """
    TR_ID: C60445371
    NAME: Fall back score for Darts with Template A <x> vs <y> B On Event Listing Pages
    DESCRIPTION: 1. To show Scores on all In-play Listing Pages for Sports Team A vs Team B (Not anything with S and P ) When we dont have score anywhere other than event name
    DESCRIPTION: In-play Listing Pages as per below
    DESCRIPTION: In-play Home Page    https://sports.coral.co.uk/home/in-play
    DESCRIPTION: In-play /All Sports (Streaming)    https://sports.coral.co.uk/in-play/watchlive
    DESCRIPTION: In-Play/Sports    https://sports.coral.co.uk/in-play/cricket
    DESCRIPTION: Sports - Matches Tab    https://sports.coral.co.uk/sport/football/matches/today
    DESCRIPTION: Sports -In-play Tab    https://sports.coral.co.uk/sport/football/live
    DESCRIPTION: Competition Landing Page    https://sports.coral.co.uk/competitions/football/football-uefa-club-competitions/uefa-champions-league
    DESCRIPTION: Note : CMS changes should be present as per below Document.
    DESCRIPTION: https://coralracing-my.sharepoint.com/:w:/g/personal/animisha_uppuluri_ivycomptech_com/EX9s5-XmNhREhoyRIoN1VYcBVWRHVPpI3MMVhZ4u4UOkiw?email=Animisha.Uppuluri%40ivycomptech.com&e=4%3A0LdMbH&at=9&CID=AC96F282-B011-45FF-AAE0-76C75E7EE4BB&wdLOR=c6B47E59E-DA9E-428D-BAD5-983F641BFDB1
    PRECONDITIONS: Player A* (1) 0-0 (0) Player B
    PRECONDITIONS: Sets score is represented by the bracket x bracket within this string. and the Legs are taken from the x-x format within the middle of the string.
    PRECONDITIONS: If no score is passed within the event name or removed from the event name then the scoreboard layout should be removed.
    PRECONDITIONS: Serve Indicators - The serve indicator should be shown as per the GD. The indicator of serve (if applicable) is passed in the string and will show as an * against the Player/Team name
    PRECONDITIONS: Team/Player A* (0) 0-3 (1) Team/Player B
    """
    keep_browser_open = True
    set_legs_indicator_score = {'current': '* (0)1-6(1) '}

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

        preplay_event = self.ob_config.add_darts_event_to_darts_all_darts(is_live=True, perform_stream=True)

        self.__class__.set_legs_indicator_event_id = set_legs_indicator_event.event_id
        self.__class__.preplay_event_id = preplay_event.event_id
        self.__class__.set_legs_indicator_event1 = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.set_legs_indicator_event_id,
            query_builder=self.ss_query_builder)

    def test_001_verify_that_scores_are_in_team_a_x_vs_y_team_b_format(self):
        """
        DESCRIPTION: Verify that scores are in Team A <x> vs <y> Team B format
        EXPECTED: Score should be in next format
        EXPECTED: Team/Player A	2-1	Team/Player B
        EXPECTED: Team/Player A	15-28	Team/Player B
        EXPECTED: ![](index.php?/attachments/get/31356)
        EXPECTED: ![](index.php?/attachments/get/126299335)
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

    def test_002_verify_that_no_scores_available_in_the_event_name(self):
        """
        DESCRIPTION: Verify that no scores available in the event name
        EXPECTED: Should show :
        EXPECTED: - player/team names;
        EXPECTED: - event start time;
        EXPECTED: - watch/live icon next to start time
        EXPECTED: ![](index.php?/attachments/get/31357)
        """
        self.navigate_to_edp(event_id=self.preplay_event_id, sport_name='darts')
        self.site.wait_splash_to_hide()
        sleep(2)
        players_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertTrue(players_name, msg='Players names not displayed on the EDP')
        date_time = self.site.sport_event_details.event_title_bar.event_time
        self.assertTrue(date_time, msg='start and date time is not displayed')
        live_icon = self.site.sport_event_details.event_title_bar.live_now_icon
        self.assertTrue(live_icon, msg='"LIVE" icon is not displayed')
