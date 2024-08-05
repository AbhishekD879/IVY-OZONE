import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C60081182_Verify_displaying_of_Each_Way_checkbox_for_multiple_selections(Common):
    """
    TR_ID: C60081182
    NAME: Verify displaying of Each Way checkbox for multiple selections
    DESCRIPTION: Test case verifies displaying of "Each Way" checkbox for multiples selections
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Ladbrokes https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98b5819ca0523e33bb464
    PRECONDITIONS: Coral https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a5d581baec82fe5baa11
    """
    keep_browser_open = True

    def test_001_select_a_few_selections_of_the_event_where_each_way_option_is_available_eg_events_from_horse_racinggreyhounds_etc(self):
        """
        DESCRIPTION: Select a few selections of the event where "Each Way" option is available (e.g. Events from Horse Racing,Greyhounds etc.).
        EXPECTED: * Selections are added to the betslip.
        EXPECTED: * Betslip is collapsed.
        """
        pass

    def test_002_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the betslip.
        EXPECTED: * Betslip is expanded.
        EXPECTED: * E/W checkbox is displayed below stake field.
        EXPECTED: ![](index.php?/attachments/get/122011295)![](index.php?/attachments/get/122011294)
        """
        pass

    def test_003_tap_on_a_few_ew_checkboxes(self):
        """
        DESCRIPTION: Tap on a few E/W checkboxes.
        EXPECTED: * "Each Way" checkbox is ticked
        EXPECTED: * Betslip remains expanded with current selections.
        """
        pass

    def test_004_collapse_the_betslip(self):
        """
        DESCRIPTION: Collapse the betslip.
        EXPECTED: * Betslip is collapsed.
        """
        pass

    def test_005_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the betslip.
        EXPECTED: * Betslip is expanded.
        EXPECTED: * E/W checkbox is displayed below the stake field.
        EXPECTED: * E/W checkbox is the ticket.
        """
        pass

    def test_006_tap_on_the_ticket_ew_checkboxes(self):
        """
        DESCRIPTION: Tap on the ticket E/W checkboxes.
        EXPECTED: *"Each Way" checkboxes are displayed below stake field as not ticked
        EXPECTED: * Betslip remains expanded
        """
        pass

    def test_007_enable_the_dark_theme_on_the_device(self):
        """
        DESCRIPTION: Enable the "Dark" theme on the device
        EXPECTED: * "Dark" theme on the device is enabled
        """
        pass

    def test_008_make_sure_that_each_way_checkboxes_are_displayed_for_thecurrent_selection(self):
        """
        DESCRIPTION: Make sure that "Each Way" checkboxes are displayed for the
        DESCRIPTION: current selection
        EXPECTED: * "Each Way" checkboxes are displayed below stake field in conformance to Coral/Ladbrokes designs in Dark theme
        EXPECTED: * "Each Way" checkboxes are not ticked
        EXPECTED: ![](index.php?/attachments/get/122011301)![](index.php?/attachments/get/122011302)
        """
        pass

    def test_009_repeat_3_6_steps_in_dark_mode(self):
        """
        DESCRIPTION: Repeat 3-6 steps in Dark mode
        EXPECTED: 
        """
        pass
