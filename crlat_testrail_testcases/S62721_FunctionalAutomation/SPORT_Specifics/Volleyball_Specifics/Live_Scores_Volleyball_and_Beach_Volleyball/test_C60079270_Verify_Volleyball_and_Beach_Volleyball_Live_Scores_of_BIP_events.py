import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60079270_Verify_Volleyball_and_Beach_Volleyball_Live_Scores_of_BIP_events(Common):
    """
    TR_ID: C60079270
    NAME: Verify Volleyball and Beach Volleyball Live Scores of BIP events
    DESCRIPTION: This test case verifies Volleyball and Beach Volleyball Live Score of BIP events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) Create Volleyball and Beach Volleyball live event in OB tool using format |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
    PRECONDITIONS: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
    PRECONDITIONS: Update scores within event name or receive events from BetGenius.
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: ["IN_PLAY_SPORTS::::LIVE_EVENT",…]
    PRECONDITIONS: Look at the attributes on Event level:
    PRECONDITIONS: **teams** - home or away
    PRECONDITIONS: **name** - team name
    PRECONDITIONS: **score** - Set - total score for team - (displayed on FE in grey color)
    PRECONDITIONS: **currentPoints** - PointsInCurrentSet - current score for team (displayed on FE in black color)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_volleyball_page(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Volleyball page
        EXPECTED: Sports landing page is opened
        """
        pass

    def test_002_check_volleyball_event_with_scores_is_available_on_volleyball__in_play_tab_for_desktop_in_play_module_for_mobile(self):
        """
        DESCRIPTION: Check Volleyball event with scores is available on 'Volleyball' > 'In-Play' tab for desktop (In-Play module for Mobile)
        EXPECTED: Volleyball event with Game Scores is available
        """
        pass

    def test_003_verify_total_score_sets_and_pointsincurrentset_displaying_for_event(self):
        """
        DESCRIPTION: Verify Total score (Sets) and PointsInCurrentSet displaying for event
        EXPECTED: * Total score (Sets) in grey color and PointsInCurrentSet in black color for particular team are shown:
        EXPECTED: - vertically at the same row as team's name near the Price/Odds button >>**for mobile/tablet**
        EXPECTED: - horizontally below Event name and next to 'Live' label >> **for desktop**
        """
        pass

    def test_004_verify_total_score_sets_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Total score (Sets) correctness for each player
        EXPECTED: Set corresponds to the **score** attribute from WS
        """
        pass

    def test_005_verify_total_score_sets_ordering(self):
        """
        DESCRIPTION: Verify Total score (Sets) ordering
        EXPECTED: **For mobile:**
        EXPECTED: * Score for the home player is shown in the first row
        EXPECTED: * Score for the away player is shown in the second row
        EXPECTED: **For desktop:**
        EXPECTED: Scores are shown below event name in the format 'x - y', where
        EXPECTED: x=Score for the home player
        EXPECTED: y=Score for the away player
        EXPECTED: Note: use comments: {teams: {away: {name: "Volero Zurich Women", score: 2,}} for matching Player and Score
        """
        pass

    def test_006_verify_pointsincurrentset_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet correctness for each player
        EXPECTED: * PointsInCurrentSet corresponds to the**'currentPoints'** attribute from the WS
        """
        pass

    def test_007_verify_pointsincurrentset_ordering(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet ordering
        EXPECTED: **For mobile:**
        EXPECTED: * PointsInCurrentSet for the home player is shown in the first row
        EXPECTED: * PointsInCurrentSet for the away player is shown in the second row
        EXPECTED: **For desktop:**
        EXPECTED: Scores are shown below event name in the format 'x - y', where
        EXPECTED: x=Score for the home player
        EXPECTED: y=Score for the away player
        EXPECTED: Note: use comments: {teams: {away: {name: "Volero Zurich Women", currentPoints: 12,}} for matching Player and PointsInCurrentSet
        """
        pass

    def test_008_verify_live_label_under_event_name(self):
        """
        DESCRIPTION: Verify 'Live' label under Event name
        EXPECTED: 'Live' label is displayed
        """
        pass

    def test_009_verify_volleyball_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event which doesn't have LIVE Score available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * Total score (Sets) and PointsInCurrentSet are NOT displayed
        """
        pass

    def test_010_verify_total_score_sets_and_pointsincurrentset_for_outright_events(self):
        """
        DESCRIPTION: Verify 'Total score (Sets) and PointsInCurrentSet for 'Outright' events
        EXPECTED: * 'Total score (Sets) and PointsInCurrentSet are not shown for Outright events
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_011_go_to_in_play_page_all_sports_sorting_type_and_repeat_steps_3_11(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'All Sports' sorting type and repeat steps #3-11
        EXPECTED: 
        """
        pass

    def test_012_go_to_in_play_page_volleyball_sorting_type_and_repeat_steps_3_11(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Volleyball' sorting type and repeat steps #3-11
        EXPECTED: 
        """
        pass

    def test_013_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_3_11(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps #3-11
        EXPECTED: 
        """
        pass

    def test_014_go_to_featured_tab_and_repeat_steps_3_11(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps #3-11
        EXPECTED: 
        """
        pass

    def test_015_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_repeat_steps_3_10_for_both_in_play_and_live_stream(self):
        """
        DESCRIPTION: **For Desktop**:
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and repeat steps #3-10 for both 'In-play' and 'Live Stream'
        EXPECTED: 
        """
        pass

    def test_016_repeat_steps_1_15_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps #1-15 for Beach Volleyball
        EXPECTED: 
        """
        pass
