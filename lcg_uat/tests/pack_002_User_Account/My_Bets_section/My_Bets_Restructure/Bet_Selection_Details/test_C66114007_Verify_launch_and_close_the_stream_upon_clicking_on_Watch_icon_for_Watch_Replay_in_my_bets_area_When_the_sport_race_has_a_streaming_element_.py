import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66114007_Verify_launch_and_close_the_stream_upon_clicking_on_Watch_icon_for_Watch_Replay_in_my_bets_area_When_the_sport_race_has_a_streaming_element_available(Common):
    """
    TR_ID: C66114007
    NAME: Verify launch and close the stream upon clicking on 'Watch' icon for 'Watch Replay' in my bets area When the sport/race has a streaming element available
    DESCRIPTION: This test case is to Verify launch and close the stream upon clicking on 'Watch' icon for 'Watch Replay' in my bets area When the sport/race has a streaming element available
    PRECONDITIONS: 1. User should have enough balance to place bets using stake 2. Streaming enabled events data should be available under UK&IRISH races
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User should be able to login
        """
        pass

    def test_002_go_to_hr_sports_landing_page_from_sports_ribbona_z_menu_and_click_on_uk_amp_irish_races(self):
        """
        DESCRIPTION: Go to HR sports landing page from sports ribbon/A-Z menu and click on uk &amp; irish races
        EXPECTED: should be able to navigate to uk and irish race
        """
        pass

    def test_003_place_single_and_multiple_bets_from_different_watch_live_events_sportsrace_and_verify(self):
        """
        DESCRIPTION: Place single and multiple bets from different watch live events (sports/race) and verify
        EXPECTED: bet placement should be done successfully for watch live event
        """
        pass

    def test_004_go_to_my_bets_and_verify_watch_icon_under_open_for_placed_bet(self):
        """
        DESCRIPTION: Go to my bets and verify watch icon under open for placed bet
        EXPECTED: Watch' icon should be displayed at the location of above potential returns and inlined with odds vertically Note: LIVE icon should be displayed beside meeting/event name
        """
        pass

    def test_005_verify_the_watch_replay_signposting_under_settled(self):
        """
        DESCRIPTION: Verify the watch replay signposting under settled
        EXPECTED: REPLAY' Text should be display along with Watch icon under settled once race is completed
        """
        pass

    def test_006_click_on_watch_icon_in_watch_replay_and_verify(self):
        """
        DESCRIPTION: Click on 'Watch' icon in watch replay and verify
        EXPECTED: Should be able to see streaming after clicking on watch icon
        """
        pass

    def test_007_click_on_watch__icon_in_watch_replay_again_and_verify(self):
        """
        DESCRIPTION: Click on 'Watch'  icon in watch replay again and verify
        EXPECTED: Should be able to close the streaming screen under open bet
        """
        pass

    def test_008_verify_the_watch_replay_signposting_under_open_for_acca_bets(self):
        """
        DESCRIPTION: Verify the watch replay signposting under open for ACCA Bets
        EXPECTED: REPLAY' Text should be display along with Watch icon under settled once race is completed Note: Can see  watch replay in open when particular race completed and other bets are not got settled
        """
        pass

    def test_009_verify_7th_step_and_8th_under_settled(self):
        """
        DESCRIPTION: Verify 7th step and 8th under settled
        EXPECTED: Result should be same as above
        """
        pass

    def test_010_repeat_step3_to_step_9_and_verify_by_placing_bets_for_sports(self):
        """
        DESCRIPTION: Repeat step3 to step 9 and verify by placing bets for sports
        EXPECTED: Result should be same as above
        """
        pass
