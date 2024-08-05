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
class Test_C1500834_Verify_Placepot_Racecard(Common):
    """
    TR_ID: C1500834
    NAME: Verify Placepot Racecard
    DESCRIPTION: This test case verifies the content of the UK Tote Placepot racecard
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
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- endpoint .symphony-solutions.eu)
    PRECONDITIONS: endpoint can be found using devlog
    """
    keep_browser_open = True

    def test_001_tap_on_placepot_subtab(self):
        """
        DESCRIPTION: Tap on Placepot subtab
        EXPECTED: * Placepot subtab content is loaded
        EXPECTED: * First leg should be loaded by default
        """
        pass

    def test_002_verify_placepot_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Placepot racecard for an active event
        EXPECTED: Placepot racecard consists of:
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

    def test_005_verify_placepot_racecard_with_a_suspended_selection(self):
        """
        DESCRIPTION: Verify Placepot racecard with a suspended selection
        EXPECTED: * All check boxes for suspended selection are disabled
        EXPECTED: * All check boxes for active selections are active
        EXPECTED: * Placepot subtab is greyed out
        """
        pass
