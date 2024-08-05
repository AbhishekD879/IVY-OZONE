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
class Test_C49062065_Verify_content_of_5_A_Side_overlay_on_5_A_Side_tab(Common):
    """
    TR_ID: C49062065
    NAME: Verify content of  '5-A-Side' overlay on 5-A-Side tab
    DESCRIPTION: This test case verifies content displaying on '5-A-Side' overlay for 5 A Side
    PRECONDITIONS: 1. Configure 5-A-Side feature in CMS:
    PRECONDITIONS: * Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: * Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: * 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: * Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: * Event is prematch (not live)
    PRECONDITIONS: * Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: 2. Create formations:
    PRECONDITIONS: * Fill all fields in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Navigate to Football event details page that has all 5-A-Side configs and created formations
    PRECONDITIONS: 5. Click on '5-A-Side' tab
    PRECONDITIONS: 6. Click 'Build' button
    """
    keep_browser_open = True

    def test_001_verify_header_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Header content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * 'Ladbrokes/Coral 5-A-Side' title (depends on brand)
        EXPECTED: * 'Select a formation and build your team' instruction text
        EXPECTED: * Formation toggles carousel with created formations:
        EXPECTED: * formation icon (corresponding to selected in CMS 'Actual formation' dropdown) ![](index.php?/attachments/get/57668477)
        EXPECTED: * formation name below the icon (corresponding to entered in CMS 'Title' input field)
        EXPECTED: * Close 'x' button
        """
        pass

    def test_002_verify_subheader_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Subheader content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * Event name
        EXPECTED: * Team names on '5-A-Side' overlay should be equal to ones from Event Details Page
        EXPECTED: * Formation (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * 'Ladbrokes'/'Coral' (depends on brand) two logos:
        EXPECTED: ![](index.php?/attachments/get/111268948)
        """
        pass

    def test_003_verify_body_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Body content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * Add buttons
        EXPECTED: * Player Information:
        EXPECTED: * Positions (corresponding to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        EXPECTED: * 'Odds / Place Bet' button
        EXPECTED: * Background Pitch Image (colour - linear-gradient(to bottom, #009d64 12%, #006742))
        """
        pass
