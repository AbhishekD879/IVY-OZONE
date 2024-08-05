import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60088734_Verify_Streaming_player_behaviour_on_TV_meeting_page_for_logged_in_users(Common):
    """
    TR_ID: C60088734
    NAME: Verify Streaming player behaviour on TV meeting page for logged in users
    DESCRIPTION: This test case verifies streaming player behaviour on Ladbrokes/Coral TV meeting page for logged in user
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56794**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: Static block for Always On Stream Channel is created in CMS
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?sid=5f748efe059ce64d59a70620
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5d24ab732fabd699077b9b8c/dashboard?sid=5f748e0c0bf7df38a687f767
    PRECONDITIONS: In CMS: System Configuration > Structure > %future streaming tv config name% -> set to enabled
    PRECONDITIONS: 1) Load app
    PRECONDITIONS: 2) User is **NOT logged in**
    PRECONDITIONS: 3) Navigate to Greyhounds Landing page
    """
    keep_browser_open = True

    def test_001_navigate_to_coralladbrokes_tv_meeting_page_but_not_from_watch_ladbrokescoral_tv_buttoneg_ladbrokes_only_from_next_races_tab__see_allmore_button_for_event_with_ladbrokes_tv_signposting_both_brands_from_regular_edp_of_any_greyhound_event__meetings_selector__pick_ladbrokes_tvcoral_tv_type(self):
        """
        DESCRIPTION: Navigate to Coral/Ladbrokes TV meeting page, but **NOT from Watch Ladbrokes/Coral TV button**
        DESCRIPTION: E.g.:
        DESCRIPTION: * [Ladbrokes only] from Next races tab > 'See all'/'More' button for event with Ladbrokes TV signposting
        DESCRIPTION: * [Both brands] From regular EDP of any Greyhound event > 'Meetings' selector > pick 'Ladbrokes TV'/'Coral TV' type
        EXPECTED: User is navigated to Ladbrokes/Coral TV meeting page
        """
        pass

    def test_002_observe_meeting_page_content(self):
        """
        DESCRIPTION: Observe meeting page content
        EXPECTED: * Placeholder message informing users of how they can gain access to the streamed content
        EXPECTED: * Message is configured in CMS > Static blocks
        """
        pass

    def test_003__log_in_with_user_with_balance_0_or_placed_bet_during_last_24_hours(self):
        """
        DESCRIPTION: * Log in with user with balance >0 or placed bet during last 24 hours
        EXPECTED: User is logged in
        """
        pass

    def test_004_navigate_to_coralladbrokes_tv_meeting_page_but_not_from_watch_ladbrokescoral_tv_buttoneg_ladbrokes_only_from_next_races_tab__see_allmore_button_for_event_with_ladbrokes_tv_signposting_both_brands_from_regular_edp_of_any_greyhound_event__meetings_selector__pick_ladbrokes_tvcoral_tv_type(self):
        """
        DESCRIPTION: Navigate to Coral/Ladbrokes TV meeting page, but **NOT from Watch Ladbrokes/Coral TV button**
        DESCRIPTION: E.g.:
        DESCRIPTION: * [Ladbrokes only] from Next races tab > 'See all'/'More' button for event with Ladbrokes TV signposting
        DESCRIPTION: * [Both brands] From regular EDP of any Greyhound event > 'Meetings' selector > pick 'Ladbrokes TV'/'Coral TV' type
        EXPECTED: * Streaming window is displayed for user
        EXPECTED: * Stream video is not started automatically
        """
        pass

    def test_005_activate_the_stream_by_tappress_on_play_button(self):
        """
        DESCRIPTION: Activate the stream by tap/press on Play button
        EXPECTED: * Stream video is started, user is able to watch the video
        EXPECTED: * Player controls and features are same as on regular event stream and depends on platform under test (web or native)
        EXPECTED: ![](index.php?/attachments/get/122251434)
        EXPECTED: ![](index.php?/attachments/get/122251435)
        """
        pass
