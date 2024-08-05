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
class Test_C60079273_To_Edit_Verify_Live_Scores_Displaying_when_PointsInCurrentSet_and_Set_were_Changed_for_HOME_Player(Common):
    """
    TR_ID: C60079273
    NAME: [To Edit] Verify Live Scores Displaying when PointsInCurrentSet and Set were Changed for HOME Player
    DESCRIPTION: This test case verifies live scores displaying when PointsInCurrentSet were changed for HOME player.
    DESCRIPTION: Note: Please add info about primary markets to this test case. According to BMA-45817, primary market for Beach Volleyball is Match betting Head/Head - while for Volleyball it is Match betting
    PRECONDITIONS: 1) In order to have a Volleyball and Beach Volleyball event should be BIP event.
    PRECONDITIONS: 2) Create Volleyball and Beach Volleyball live event in OB tool using format |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
    PRECONDITIONS: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
    PRECONDITIONS: Update scores within event name or receive events from BetGenius
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 3) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see update with particular score
    PRECONDITIONS: *   **role_code=HOME**  - to determine HOME team
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_volleyball_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Volleyball' icon from the Sports Menu Ribbon
        EXPECTED: 'Volleyball' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab_for_desktop_in_play_module_on_matches_tab_for_mobile(self):
        """
        DESCRIPTION: Tap 'In-Play' tab for Desktop (In-Play module on Matches tab for Mobile)
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_004_verify_volleyball_event_with_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event with score available
        EXPECTED: Total score (Sets) and PointsInCurrentSet in black color for particular team are shown vertically at the same row as team's name near the Price/Odds button
        """
        pass

    def test_005_change_pointsincurrentset_in_betgenius_tool_or_in_ob_ti_tool_within_event_name_for_home_player(self):
        """
        DESCRIPTION: Change PointsInCurrentSet in BetGenius tool or in OB TI tool within event name for HOME player
        EXPECTED: * PointsInCurrentSet immediately starts displaying new value for Home player
        EXPECTED: * PointsInCurrentSet corresponds to **event.scoreboard.CURRENT.value** received in WS where **role_code=HOME**
        """
        pass

    def test_006_change_set_score_in_betgenius_tool_or_ob_ti_tool_within_event_name_for_home_player(self):
        """
        DESCRIPTION: Change Set score in BetGenius tool or OB TI tool within event name for HOME player
        EXPECTED: * Set immediately starts displaying new value for Away player
        EXPECTED: * Set corresponds to **event.scoreboard.ALL.value** received in WS where **role_code=HOME**
        EXPECTED: * PointsInCurrentSet are updated automatically and corresponds to **event.scoreboard.CURRENT.value** received in WS where **role_code=HOME**
        """
        pass

    def test_007_verify_pointsincurrentset_and_set_change_for_home_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet and Set change for HOME player for sections in a collapsed state
        EXPECTED: If section is collapsed and PointsInCurrentSet and Set were changed, after expanding the section - updated PointsInCurrentSet will be shown there
        """
        pass

    def test_008_verify_pointsincurrentset_and_set_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet and Set change before application is opened
        EXPECTED: If application was not started/opened and PointsInCurrentSet and Set were changed for HOME player, after opening application and verified event - updated PointsInCurrentSet will be shown there
        """
        pass

    def test_009_verify_pointsincurrentset_and_set_change_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify PointsInCurrentSet and Set change when Details Page of verified event is opened
        EXPECTED: After tapping Back button updated PointsInCurrentSet and Set will be shown on Landing page
        """
        pass

    def test_010_go_to_in_play_page_all_sports_sorting_type_and_repeat_steps__4_9(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'All Sports' sorting type and repeat steps  #4-9
        EXPECTED: 
        """
        pass

    def test_011_go_to_in_play_page_volleyball_sorting_type_and_repeat_steps_4_9(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Volleyball' sorting type and repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_012_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_4_9(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_013_go_to_in_play_widget_and_repeat_steps_4_9(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_014_go_to_featured_tab_and_repeat_steps_4_9(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_2_14_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps #2-14 for Beach Volleyball
        EXPECTED: 
        """
        pass
