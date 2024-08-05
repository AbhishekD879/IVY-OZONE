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
class Test_C66114003_Verify_watch_icon_display_for_the_bets_in_my_bets_area_When_the_sport_race_has_a_live_streaming(Common):
    """
    TR_ID: C66114003
    NAME: Verify watch icon display for the bets in my bets area When the sport/race has a live streaming
    DESCRIPTION: This test case is to Verify watch icon display for the bets in my bets area When the sport/race has a streaming
    PRECONDITIONS: 1. User should have enough balance to place bets using stake 2. Streaming enabled events data should be available
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

    def test_002_go_to_in_play_page_from_sports_ribbon_or_a_z_menu_and_click_on_watch_live_then_verify(self):
        """
        DESCRIPTION: Go to in-play page from sports ribbon or A-Z menu and click on Watch live then verify
        EXPECTED: should be able to click on watch live and able to see 'watch live' events data should be listed down in sport accordion wise
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

    def test_005_verify_the_watch_icon_under_open_for_acca_bets(self):
        """
        DESCRIPTION: Verify the watch icon under open for ACCA Bets
        EXPECTED: Watch' icon should be displayed at the location of above potential returns and inlined with odds vertically Note: LIVE icon should be displayed beside meeting/event name
        """
        pass

    def test_006_repeat_5th_step_under__cashout_tab_and_verify(self):
        """
        DESCRIPTION: Repeat 5th step under  cashout tab and verify
        EXPECTED: Result should be same as above
        """
        pass

    def test_007_repeat_3rd_to_6th_steps_and_verify_by_placing_the_bets_for_races(self):
        """
        DESCRIPTION: Repeat 3rd to 6th steps and verify by placing the bets for races
        EXPECTED: Result should be same as above
        """
        pass
