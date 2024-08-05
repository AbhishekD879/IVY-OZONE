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
class Test_C60079275_Verify_Volleyball_Total_Score_Set_Displaying_when_New_Set_appears(Common):
    """
    TR_ID: C60079275
    NAME: Verify Volleyball Total Score (Set) Displaying when New Set appears
    DESCRIPTION: This test case verifies updated sets displaying when new set appears.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) In order to have a Volleyball and Beach Volleyball event should be BIP
    PRECONDITIONS: 2) Create Volleyball and Beach Volleyball live event in OB tool using format |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name|
    PRECONDITIONS: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
    PRECONDITIONS: Update scores within event name or receive events from BetGenius
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 3) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 42["IN_PLAY_SPORTS::36::LIVE_EVENT",…]
    PRECONDITIONS: Look at the attributes on Event level:
    PRECONDITIONS: **teams** - home or away
    PRECONDITIONS: **name** - team name
    PRECONDITIONS: **score** - Set - total score for team - (displayed on FE in grey color)
    PRECONDITIONS: **currentPoints** - PointsInCurrentSet - current score for team (displayed on FE in black color)
    PRECONDITIONS: Score updates are received in response type: "EVENT" in Event.Names: (e.g. |Volero Zurich Women| (2) 12-5 (0) |CS Volei Alba Blaj Women|(BG)|)
    PRECONDITIONS: 4) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
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
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_verify_volleyball_event_with_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event with score available
        EXPECTED: * Total score (Sets) in grey color and PointsInCurrentSet in black color for particular team are shown:
        EXPECTED: - vertically at the same row as team's name near the Price/Odds button >> **for mobile/tablet**
        EXPECTED: - horizontally below Event name and next to 'Live' label >> **for desktop**
        """
        pass

    def test_005_trigger_the_following_situation_in_betgenius_tool_or_ob_ti_within_event_namenew_set_appears(self):
        """
        DESCRIPTION: Trigger the following situation in BetGenius tool or OB TI within event name:
        DESCRIPTION: **New set appears**
        EXPECTED: *   Total score (Sets) and PointsInCurrentSet immediately appears
        EXPECTED: * **PointsInCurrentSet** corresponds to value received in event name in WS
        EXPECTED: * **Set** corresponds to the value in brackets received in event name in WS
        """
        pass

    def test_006_verify_new_set_appearing_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify new Set appearing for sections in a collapsed state
        EXPECTED: If section is collapsed and new set appears, after expanding the section - PointsInCurrentSet of new set and updated set number will be shown there
        """
        pass

    def test_007_verify_new_set_appearing_before_application_is_opened(self):
        """
        DESCRIPTION: Verify new Set appearing before application is opened
        EXPECTED: If application was not started/opened and new set appears, after opening application and verified event - PointsInCurrentSet of new set and updated set number will be shown there
        """
        pass

    def test_008_verify_new_set_appearing_when_details_page_of_verified_event_is_opened(self):
        """
        DESCRIPTION: Verify new Set appearing when Details Page of verified event is opened
        EXPECTED: After tapping Back button score of new set and updated set number will be shown on Landing page
        """
        pass

    def test_009_go_to_in_play_page_all_sports_sorting_type_and_repeat_steps__4_8(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'All Sports' sorting type and repeat steps  #4-8
        EXPECTED: 
        """
        pass

    def test_010_go_to_in_play_page_volleyball_sorting_type_and_repeat_steps_4_8(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Volleyball' sorting type and repeat steps #4-8
        EXPECTED: 
        """
        pass

    def test_011_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_4_8(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps #4-8
        EXPECTED: 
        """
        pass

    def test_012_go_to_in_play_widget_and_repeat_steps_4_8(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps #4-8
        EXPECTED: 
        """
        pass

    def test_013_go_to_featured_tab_and_repeat_steps_4_8(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps #4-8
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps2_13_for_beach_volleyball(self):
        """
        DESCRIPTION: Repeat steps#2-13 for Beach Volleyball
        EXPECTED: 
        """
        pass
