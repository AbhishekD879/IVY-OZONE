import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2321111_Verify_Scoop6_Racecard(Common):
    """
    TR_ID: C2321111
    NAME: Verify Scoop6 Racecard
    DESCRIPTION: This test case verifies the content of the UK Tote Scoop6 racecard
    PRECONDITIONS: * Enable UK Tote feature in CMS (check the checkbox) and save changes
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: * The HR event should have Scoop6 markets available
    """
    keep_browser_open = True

    def test_001_tap_on_scoop6_subtab(self):
        """
        DESCRIPTION: Tap on Scoop6 subtab
        EXPECTED: * Scoop6 subtab content is loaded
        EXPECTED: * First leg should be loaded by default
        """
        pass

    def test_002_verify_scoop6_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Scoop6 racecard for an active event
        EXPECTED: Scoop6 racecard consists of:
        EXPECTED: * **Current Pool** value
        EXPECTED: * Leg Header buttons
        EXPECTED: * Event name for each leg
        EXPECTED: * Checkboxes for each runner
        EXPECTED: * Runner number, name and information for each runner
        EXPECTED: * Runner silks (if available) for each runner
        EXPECTED: Unnamed Favourite is displayed at the end of list (BMA-50146)
        """
        pass

    def test_003_tap_on_each_leg_header_button(self):
        """
        DESCRIPTION: Tap on each Leg Header button
        EXPECTED: * Selected leg racecard content is loaded
        EXPECTED: * Content of racecard is the same as in step 2
        """
        pass

    def test_004_tap_on_runner_sportlight_section_to_expand(self):
        """
        DESCRIPTION: Tap on Runner Sportlight section to expand
        EXPECTED: * Spotlight section is expanded
        EXPECTED: * Section expand button is changed to collapse button
        EXPECTED: * Form & Spotlight information is displayed
        EXPECTED: * Show more link is available if description is lengthy
        EXPECTED: * Tapping on the collapse button closes the section
        """
        pass
