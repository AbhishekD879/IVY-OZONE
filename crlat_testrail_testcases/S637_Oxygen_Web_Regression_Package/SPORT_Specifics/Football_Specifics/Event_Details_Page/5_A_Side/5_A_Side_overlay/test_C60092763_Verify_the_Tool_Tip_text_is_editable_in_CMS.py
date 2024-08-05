import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60092763_Verify_the_Tool_Tip_text_is_editable_in_CMS(Common):
    """
    TR_ID: C60092763
    NAME: Verify the Tool Tip text is editable in CMS
    DESCRIPTION: Verify that Tool Tip text is editable in CMS
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_login_to_cms_and_navigate_to_tool_tip_edit_for_line_ups_not_availabe(self):
        """
        DESCRIPTION: Login to CMS and navigate to Tool Tip Edit for Line-Ups Not Availabe
        EXPECTED: User should be logged in and navigated to Tool Tip edit field
        """
        pass

    def test_002_configure_the_tool_tip_text_and_save(self):
        """
        DESCRIPTION: Configure the Tool Tip Text and save
        EXPECTED: User should be able to configure and Save
        """
        pass

    def test_003_launch_ladbrokes_app(self):
        """
        DESCRIPTION: Launch Ladbrokes app
        EXPECTED: User should be able launch the application successfully
        """
        pass

    def test_004_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User should be navigated to Football landing page
        """
        pass

    def test_005_navigate_to_any_football_event_that_has_5_a_side_available(self):
        """
        DESCRIPTION: Navigate to any football event that has 5-A side available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_006_navigate_to_5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to 5-A Side tab
        EXPECTED: User should be navigated to 5-A Side tab
        """
        pass

    def test_007_click_on_build_a_team(self):
        """
        DESCRIPTION: Click on Build a Team
        EXPECTED: 1: Pitch View should be displayed
        EXPECTED: 2: Balanced formation should be selected by default
        EXPECTED: 3: User should be able to select any formation displayed in the pitch view
        """
        pass

    def test_008_verify_the_display_of_line_ups_not_available(self):
        """
        DESCRIPTION: Verify the display of Line Ups Not available
        EXPECTED: 1: User should be displayed with Line-Ups Not Available
        EXPECTED: 2: It should be displayed below the event name
        """
        pass

    def test_009_click_on_the_info_icon(self):
        """
        DESCRIPTION: Click on the info icon
        EXPECTED: 1: User should be able to see the Tool tip text that is configured in CMS
        EXPECTED: 2: On clicking anywhere on the scree Tool Tip should be closed
        """
        pass
