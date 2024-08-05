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
class Test_C49253155_Verify_created_formation_on_5_A_Side_overlay(Common):
    """
    TR_ID: C49253155
    NAME: Verify created formation on '5-A-Side' overlay
    DESCRIPTION: This test case verifies created formation on '5-A-Side' overlay
    PRECONDITIONS: 1. Configure 5-A-Side feature in CMS:
    PRECONDITIONS: * Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: * Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: * 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: * Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: * Event is prematch (not live)
    PRECONDITIONS: * Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: 2. Create **formation 1**:
    PRECONDITIONS: * **Fill ALL fields** in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 3. Create **formation 2**:
    PRECONDITIONS: * **Fill only required fields** in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 4. Create **formation 3**:
    PRECONDITIONS: * **Fill required fields, 'Position 1' field, 'Position 2' field (Position 3/4/5 should be empty)** in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 5. Load the app
    PRECONDITIONS: 6. Navigate to Football event details page that has all 5-A-Side configs and created formations
    PRECONDITIONS: 7. Click on '5-A-Side' tab
    PRECONDITIONS: 8. Click 'Build' button
    PRECONDITIONS: 9. Click on **formation 1** icon in formations carousel
    """
    keep_browser_open = True

    def test_001_verify_formation_1_data_is_displayed_on_5_a_side_overlay_corresponds_to_filled_form_in_cms_cms___byb___5_a_side___formation_name(self):
        """
        DESCRIPTION: Verify **formation 1** data is displayed on '5-A-Side' overlay corresponds to filled form in CMS (CMS -> BYB -> 5-A-Side -> formation name)
        EXPECTED: The following data should be displayed:
        EXPECTED: * formations name and icon in formations carousel (corresponding to entered in CMS 'Title' name and 'Actual formation' dropdown)
        EXPECTED: * Formation in Subheader (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * Player Information below the each of 'Add Player' button:
        EXPECTED: * Positions should be displayed (corresponding to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        """
        pass

    def test_002_click_on_formation_2_icon_in_formations_carouselverify_formation_2_data_is_displayed_on_5_a_side_overlay_corresponds_to_filled_form_in_cms_cms___byb___5_a_side___formation_name(self):
        """
        DESCRIPTION: Click on **formation 2** icon in formations carousel
        DESCRIPTION: Verify **formation 2** data is displayed on '5-A-Side' overlay corresponds to filled form in CMS (CMS -> BYB -> 5-A-Side -> formation name)
        EXPECTED: The following data should be displayed:
        EXPECTED: * formations name and icon in formations carousel (corresponding to entered in CMS 'Title' name and 'Actual formation' dropdown)
        EXPECTED: * Formation in Subheader (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * Player Information below the each of 'Add Player' button:
        EXPECTED: * Positions **should NOT be displayed** (corresponding to 'Position' input field in CMS)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        """
        pass

    def test_003_click_on_formation_3_icon_in_formations_carouselverify_formation_3_data_is_displayed_on_5_a_side_overlay_corresponds_to_filled_form_in_cms_cms___byb___5_a_side___formation_name(self):
        """
        DESCRIPTION: Click on **formation 3** icon in formations carousel
        DESCRIPTION: Verify **formation 3** data is displayed on '5-A-Side' overlay corresponds to filled form in CMS (CMS -> BYB -> 5-A-Side -> formation name)
        EXPECTED: The following data should be displayed:
        EXPECTED: * formations name and icon in formations carousel (corresponding to entered in CMS 'Title' name and 'Actual formation' dropdown)
        EXPECTED: * Formation in Subheader (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * Player Information below the each of 'Add Player' button:
        EXPECTED: * Position 1 and Position 2 should be displayed (corresponding to 'Position' input field in CMS)
        EXPECTED: * Position 3/4/5 **should NOT be displayed** (corresponding to 'Position' input field in CMS)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        """
        pass
