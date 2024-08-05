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
class Test_C1391844_Verify_Sub_Tabs_data(Common):
    """
    TR_ID: C1391844
    NAME: Verify Sub Tabs data
    DESCRIPTION: This test case verifies Sub Tab data within Tab
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET competition request
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
        EXPECTED: * GET competition request is sent to get Competition Sub Tab structure to Big Competition MS
        """
        pass

    def test_003_go_to_tab_that_has_sub_tabs_active(self):
        """
        DESCRIPTION: Go to Tab that has Sub Tabs active
        EXPECTED: 
        """
        pass

    def test_004_verify_the_number_of_sub_tabs_displayed_within_tab(self):
        """
        DESCRIPTION: Verify the number of Sub Tabs displayed within Tab
        EXPECTED: The number of Sub Tabs corresponds to the quantity of items in **competitionSubTabs** array in GET competition response
        """
        pass

    def test_005_verify_sub_tabs_ordering(self):
        """
        DESCRIPTION: Verify Sub Tabs ordering
        EXPECTED: Sub Tabs are ordered in ascending order as received in **competitionSubTabs** array in GET competition response
        """
        pass

    def test_006_verify_sub_tab_name_correctness(self):
        """
        DESCRIPTION: Verify Sub Tab name correctness
        EXPECTED: Sub Tab name corresponds to **competitionTabs.[i].competitionSubTabs.[j].name** attribute from GET competition response
        EXPECTED: where i - the number of all Tabs returned
        EXPECTED: j - the number of all Sub Tabs returned
        """
        pass

    def test_007_verify_navigation_between_sub_tabs(self):
        """
        DESCRIPTION: Verify navigation between Sub Tabs
        EXPECTED: Its possible to navigate between Sub Tabs via the switcher
        """
        pass

    def test_008_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * GET request with Sub Tab ID is sent to Big Competition
        EXPECTED: * Content of Sub Tab is loaded
        """
        pass
