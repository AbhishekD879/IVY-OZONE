import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59900120_Verify_displaying_of_Each_Way_checkbox_for_single_selection(Common):
    """
    TR_ID: C59900120
    NAME: Verify displaying of Each Way checkbox for single selection
    DESCRIPTION: Test case verifies displaying of "Each Way" checkbox for single selection
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Coral design: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?sid=5eaa983ae1344bbac8b9f021
    PRECONDITIONS: Ladbrokes design: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea97d244f68f62598af7515
    """
    keep_browser_open = True

    def test_001__tap_on_any_selection_of_the_event_where_for_selection_each_way_option_is_available_eg_events_from_horse_racinggreyhounds_etc(self):
        """
        DESCRIPTION: * Tap on any selection of the event where for selection "Each Way" option is available (e.g. Events from Horse Racing,Greyhounds etc.)
        EXPECTED: * Selected single selection added to Betslip
        EXPECTED: * Betslip in collapsed mode  displays the selection in the bottom of the screen
        EXPECTED: * "Each Way" checkbox is not displayed for current selection below stake field
        """
        pass

    def test_002__tap_on_selection_in_betslip(self):
        """
        DESCRIPTION: * Tap on selection in Betslip
        EXPECTED: * Betslip expands with current selection
        """
        pass

    def test_003__make_sure_that_each_way_checkbox_is__displayed_for_current_selection(self):
        """
        DESCRIPTION: * Make sure that "Each Way" checkbox is  displayed for current selection
        EXPECTED: * "Each Way" checkbox is  displayed below stake field in conformance to Coral/Ladbrokes  designs in Light theme
        EXPECTED: * "Each Way" checkbox is not ticked by default
        EXPECTED: Coral / Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/118935550) ![](index.php?/attachments/get/118935549)
        """
        pass

    def test_004__user_taps_on_each_way_checkbox(self):
        """
        DESCRIPTION: * User taps on "Each Way" checkbox
        EXPECTED: * "Each Way" checkbox is ticked
        EXPECTED: * Betslip remains expanded with current single selection
        """
        pass

    def test_005__collapse_betslip(self):
        """
        DESCRIPTION: * Collapse Betslip
        EXPECTED: * Betsip in collapsed mode displays current selection without "Each Way" checkbox below "Stake" filed
        """
        pass

    def test_006__tap_on_selection_to_expande_betslip(self):
        """
        DESCRIPTION: * Tap on selection to expande Betslip
        EXPECTED: * Betslip expands with current selection
        EXPECTED: * "Each Way" checkbox is  displayed below stake field
        EXPECTED: * "Each Way" checkbox is ticked
        """
        pass

    def test_007__user_taps_on_each_way_checkbox(self):
        """
        DESCRIPTION: * User taps on "Each Way" checkbox
        EXPECTED: * "Each Way" checkbox is  displayed below stake field as not ticked
        EXPECTED: * Betslip remains expanded
        """
        pass

    def test_008__enable_dark_theme_on_device(self):
        """
        DESCRIPTION: * Enable "Dark" theme on device
        EXPECTED: * "Dark" theme on device is  enabled
        """
        pass

    def test_009__make_sure_that_each_way_checkbox_is__displayed_for_current_selection(self):
        """
        DESCRIPTION: * Make sure that "Each Way" checkbox is  displayed for current selection
        EXPECTED: * "Each Way" checkbox is  displayed below stake field in conformance to Coral/Ladbrokes  designs in Dark theme
        EXPECTED: * "Each Way" checkbox is not ticked
        EXPECTED: Coral / Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/118935554) ![](index.php?/attachments/get/118935553)
        """
        pass

    def test_010__repeat_steps_4___7(self):
        """
        DESCRIPTION: * Repeat steps 4 - 7
        EXPECTED: * Results from 4 - 7
        EXPECTED: * Behaviour of "Each Way" checkbox conforms to Dark theme
        """
        pass
