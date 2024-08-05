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
class Test_C66114005_Verify_watch_icon_alongside_insights_text_display_for_the_bets_in_my_bets_area_When_the_race_has_a_streaming_element_available(Common):
    """
    TR_ID: C66114005
    NAME: Verify watch icon alongside 'insights' text display for the bets in my bets area When the race has a streaming element available
    DESCRIPTION: This test case is to verify Verify watch icon alongside 'insights' text display for the bets in my bets area When the race has a streaming element available
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

    def test_002_go_to_hr_sports_landing_page_from_sports_ribbona_z_menu_and_click_on_uk_amp_irish_races(self):
        """
        DESCRIPTION: Go to HR sports landing page from sports ribbon/A-Z menu and click on uk &amp; irish races
        EXPECTED: should be able to navigate to uk and irish race
        """
        pass

    def test_003_place_single_and_multiple_bets_from_different_watch_live_preplay_events_sportsrace_and_verify(self):
        """
        DESCRIPTION: Place single and multiple bets from different watch live preplay events (sports/race) and verify
        EXPECTED: bet placement should be done successfully for watch live event
        """
        pass

    def test_004_go_to_my_bets_and_verify_watch_icon_under_open_for_placed_bet(self):
        """
        DESCRIPTION: Go to my bets and verify watch icon under open for placed bet
        EXPECTED: Watch and insights' icon should be displayed at the location of above potential returns and inlined with odds vertically
        """
        pass

    def test_005_repeat_step_3_to_step_5_under_cashout_tab(self):
        """
        DESCRIPTION: Repeat step 3 to step 5 under cashout tab
        EXPECTED: Result should be same as above
        """
        pass

    def test_006_verify_watch_amp_insights_under_settled_by_performing_cashed_out(self):
        """
        DESCRIPTION: Verify Watch &amp; Insights under settled by performing cashed out
        EXPECTED: Watch and insights' icon should not be displayed under settled bet
        """
        pass

    def test_007_verify_watch_amp_insights_under_settled_once_race_got_completed(self):
        """
        DESCRIPTION: verify watch &amp; Insights under settled once race got completed
        EXPECTED: TBD
        """
        pass

    def test_008_repeat_step3_to_step8_and_verify_by_placing_bets_for_sports(self):
        """
        DESCRIPTION: Repeat step3 to step8 and verify by placing bets for sports
        EXPECTED: Watch' icon should be display in open,cashout and settled tabs after race become live only
        """
        pass
