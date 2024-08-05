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
class Test_C66114006_Verify_launch_and_close_the_stream_upon_clicking_on_Watch_icon_in_my_bets_area_When_the_sport_race_has_a_streaming_element_available(Common):
    """
    TR_ID: C66114006
    NAME: Verify launch and close the stream upon clicking on Watch icon in my bets area When the sport/race has a streaming element available
    DESCRIPTION: This test case is to Verify launch and close the stream upon clicking on Watch icon in my bets area When the sport/race has a streaming element available
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

    def test_003_place_single_and_multiple_bets_from_different_watch_live_events_race_and_verify(self):
        """
        DESCRIPTION: Place single and multiple bets from different watch live events (race) and verify
        EXPECTED: bet placement should be done successfully for watch live event
        """
        pass

    def test_004_go_to_my_bets_and_verify_watch_icon_under_open_for_placed_bet(self):
        """
        DESCRIPTION: Go to my bets and verify watch icon under open for placed bet
        EXPECTED: Watch' icon should be displayed at the location of above potential returns and inlined with odds vertically Note: LIVE icon should be displayed beside meeting/event name
        """
        pass

    def test_005_click_on_watch_icon_and_verify(self):
        """
        DESCRIPTION: Click on 'Watch' icon and verify
        EXPECTED: Should be able to see streaming after clicking on watch icon
        """
        pass

    def test_006_click_on_watch_icon_again_and_verify(self):
        """
        DESCRIPTION: Click on 'Watch' icon again and verify
        EXPECTED: Should be able to close the streaming screen under open bet
        """
        pass

    def test_007_repeat_step_3_to_step_7_and_verify_under_cashout(self):
        """
        DESCRIPTION: Repeat step 3 to step 7 and verify under cashout
        EXPECTED: Result should be same as above
        """
        pass
