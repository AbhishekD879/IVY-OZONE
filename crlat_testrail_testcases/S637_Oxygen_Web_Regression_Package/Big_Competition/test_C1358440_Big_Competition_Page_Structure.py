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
class Test_C1358440_Big_Competition_Page_Structure(Common):
    """
    TR_ID: C1358440
    NAME: Big Competition Page Structure
    DESCRIPTION: This test case verifies Big Competition Page Structure
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and choose GET competition request
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
        EXPECTED: * GET competition request is sent to get Competition Tab structure to Big Competition MS
        """
        pass

    def test_003_verify_competition_content(self):
        """
        DESCRIPTION: Verify Competition content
        EXPECTED: Competition page consists of:
        EXPECTED: * Back button
        EXPECTED: * Competition name
        EXPECTED: * Competition Tabs
        """
        pass

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is navigated to previous page after tapping Back button
        EXPECTED: [On sports and sports-hl it's redirection to main page]
        """
        pass

    def test_005_verify_competition_name_correctness(self):
        """
        DESCRIPTION: Verify Competition name correctness
        EXPECTED: Competition name corresponds to **name** attribute from GET competition response
        """
        pass

    def test_006_verify_the_number_of_tabs_displayed_within_competition(self):
        """
        DESCRIPTION: Verify the number of Tabs displayed within Competition
        EXPECTED: The number of Sub Tabs corresponds to the quantity of items in **competitionTabs** array in GET competition response
        """
        pass

    def test_007_verify_competition_tab_ordering(self):
        """
        DESCRIPTION: Verify Competition tab ordering
        EXPECTED: Tabs are ordered in ascending order as received in **competitionTabs** array in GET competition response
        """
        pass

    def test_008_verify_competition_tab_correctness(self):
        """
        DESCRIPTION: Verify Competition tab correctness
        EXPECTED: Competition tab corresponds to **competitionTabs.[i].title** attribute from GET competition response
        EXPECTED: where i - the number of all Tabs returned
        """
        pass
