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
class Test_C1217999_Add_a_new_Tab(Common):
    """
    TR_ID: C1217999
    NAME: Add a new Tab
    DESCRIPTION: This case verifies adding new Tab within Competition in CMS
    PRECONDITIONS: Have at least one big competition created
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_big_competition_section(self):
        """
        DESCRIPTION: Go to Big Competition section
        EXPECTED: * Big Competition section is opened
        EXPECTED: * List of all competitions is displayed
        """
        pass

    def test_003_tap_on_a_competition_previously_created(self):
        """
        DESCRIPTION: Tap on a Competition previously created
        EXPECTED: * Competition details page is loaded
        """
        pass

    def test_004_tap_plus_create_tab_button(self):
        """
        DESCRIPTION: Tap '+ Create Tab' button
        EXPECTED: A 'Create a Tab' pop-up is displayed displaying:
        EXPECTED: * 'Tab Name', written field is present and empty by default
        EXPECTED: * 'Active' and 'Tab sub tabs' checkbox options are present and unselected by default
        """
        pass

    def test_005_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: * New Tab is NOT created
        EXPECTED: * Competition details page is loaded
        """
        pass

    def test_006_repeat_steps_3_4_but_fill_in_tab_name_and_tap_create_tab_button(self):
        """
        DESCRIPTION: Repeat steps #3-4 but fill in Tab name and tap 'Create tab' button
        EXPECTED: * New Tab is created
        EXPECTED: * Respective 'Big Competition' edit page is loaded
        EXPECTED: * New Tab is displayed at the bottom of the list of all existing Tabs for that 'Big Competition'
        EXPECTED: * Status is inactive (disabled icon is displayed in 'Enabled' column)
        EXPECTED: * Sub-tabs are disabled (disabled icon is displayed in 'Tab has sub-tabs' column)
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: A 'Create a Tab' pop-up is displayed displaying:
        EXPECTED: * 'Tab Name', written field is present and empty by default
        EXPECTED: * 'Active' and 'Tab sub tabs' checkbox options are present and unselected by default
        """
        pass

    def test_008_fill_in_tab_name_and_check_active_and_tab_sub_tabs_checkboxes(self):
        """
        DESCRIPTION: Fill in Tab name and check 'Active' and 'Tab sub tabs' checkboxes
        EXPECTED: 
        """
        pass

    def test_009_tap_create_tab_button(self):
        """
        DESCRIPTION: Tap 'Create tab' button
        EXPECTED: * New Tab is created
        EXPECTED: * Respective 'Big Competition' edit page is loaded
        EXPECTED: * New Tab is displayed at the bottom of the list of all existing Tabs for that 'Big Competition'
        EXPECTED: * Status is active (enabled icon is displayed in 'Enabled' column)
        EXPECTED: * Sub-tabs are enabled (enabled icon is displayed in 'Tab has sub-tabs' column)
        """
        pass
