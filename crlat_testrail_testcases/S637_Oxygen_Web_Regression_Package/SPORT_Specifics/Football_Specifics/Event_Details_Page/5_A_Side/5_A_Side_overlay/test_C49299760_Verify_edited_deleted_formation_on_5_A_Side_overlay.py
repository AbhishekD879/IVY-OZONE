import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C49299760_Verify_edited_deleted_formation_on_5_A_Side_overlay(Common):
    """
    TR_ID: C49299760
    NAME: Verify edited/deleted formation on '5-A-Side' overlay
    DESCRIPTION: This test case verifies edited/deleted formation on '5-A-Side' overlay
    PRECONDITIONS: 1. Configure 5-A-Side feature in CMS:
    PRECONDITIONS: * Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: * Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: * 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: * Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: * Event is prematch (not live)
    PRECONDITIONS: * Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: 2. Create formation in CMS -> BYB -> 5-A-Side
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Navigate to Football event details page -> 5-A-Side tab -> click 'Build' button -> click on created formation icon in formations carousel
    PRECONDITIONS: 5. Edit created formation in CMS -> BYB -> 5-A-Side -> formation name:
    PRECONDITIONS: * Rename 'Title' name
    PRECONDITIONS: * Change 'Actual formation' value
    PRECONDITIONS: * Rename 'Position 1' name
    PRECONDITIONS: * Delete 'Position 2' name (leave field empty)
    PRECONDITIONS: * Change 'Stat 1' value
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 6. Refresh the page with opened formation
    """
    keep_browser_open = True

    def test_001_verify_new_formation_data_is_displayed_on_5_a_side_overlay_corresponds_new_changes_in_cms_cms___byb___5_a_side___formation_name(self):
        """
        DESCRIPTION: Verify new formation data is displayed on '5-A-Side' overlay corresponds new changes in CMS (CMS -> BYB -> 5-A-Side -> formation name)
        EXPECTED: The following data should be changed:
        EXPECTED: * formations name and icon in formations carousel (corresponding to changed in CMS 'Title' name and 'Actual formation' dropdown)
        EXPECTED: * Formation in Subheader (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * Position 1 should be changed (corresponding to changed in CMS 'Position 1' input field)
        EXPECTED: * Position 2 should be empty (corresponding to changed in CMS 'Position 2' input field)
        EXPECTED: * Statistic 1(corresponding to changed in CMS 'Stat 1' dropdown)
        """
        pass

    def test_002_delete_created_formation_in_cms_cms___byb___5_a_siderefresh_the_page_with_opened_formation(self):
        """
        DESCRIPTION: Delete created formation in CMS (CMS -> BYB -> 5-A-Side)
        DESCRIPTION: Refresh the page with opened formation
        EXPECTED: * The first formation is displayed in formation carousel
        EXPECTED: * Deleted formation is not displayed in formation carousel
        """
        pass
