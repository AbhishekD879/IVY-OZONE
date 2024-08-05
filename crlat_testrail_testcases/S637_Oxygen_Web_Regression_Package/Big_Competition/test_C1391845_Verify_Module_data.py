import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1391845_Verify_Module_data(Common):
    """
    TR_ID: C1391845
    NAME: Verify Module data
    DESCRIPTION: This test case verifies Module data within Tab / Sub Tab
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        EXPECTED: * GET request with Tab ID is sent to Big Competition MS
        """
        pass

    def test_003_go_to_module_area(self):
        """
        DESCRIPTION: Go to Module area
        EXPECTED: 
        """
        pass

    def test_004_verify_the_number_of_modules_displayed_within_tab(self):
        """
        DESCRIPTION: Verify the number of Modules displayed within Tab
        EXPECTED: The number of Sub Tabs corresponds to the quantity of items in **competitionModules** array in GET tab response
        """
        pass

    def test_005_verify_modules_ordering(self):
        """
        DESCRIPTION: Verify Modules ordering
        EXPECTED: Modules are ordered in ascending order as received in **competitionModules** array in GET tab response
        """
        pass

    def test_006_verify_module_name_correctness(self):
        """
        DESCRIPTION: Verify Module name correctness
        EXPECTED: Module name corresponds to **competitionModules.[i].name** attribute from GET tab by ID response
        EXPECTED: where i - the number of Modules received for particular Tab
        """
        pass

    def test_007_verify_module_panel(self):
        """
        DESCRIPTION: Verify Module panel
        EXPECTED: * Its possible to expand Module by taping '+' sign or Module panel
        EXPECTED: * Its possible to collapse Module by taping '-' sign or Module panel
        """
        pass

    def test_008_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Competition page is opened
        EXPECTED: * GET request with Tab ID is sent to Big Competition
        EXPECTED: * Content of Tab is loaded
        """
        pass

    def test_009_navigate_to_tab_that_has_sub_tabs_with_active_modules(self):
        """
        DESCRIPTION: Navigate to Tab that has Sub Tabs with active Modules
        EXPECTED: * Default Sub Tab is opened (e.g. Group A)
        EXPECTED: * GET request with Sub Tab ID is sent to Big Competition MS
        """
        pass

    def test_010_repeat_steps_3_8_but_note_that_data_is_received_from_get_sub_tab_id_request(self):
        """
        DESCRIPTION: Repeat steps #3-8, but note that data is received from GET Sub Tab ID request
        EXPECTED: 
        """
        pass
