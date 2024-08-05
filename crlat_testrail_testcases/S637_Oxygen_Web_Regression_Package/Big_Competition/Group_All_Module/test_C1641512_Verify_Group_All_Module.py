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
class Test_C1641512_Verify_Group_All_Module(Common):
    """
    TR_ID: C1641512
    NAME: Verify Group All Module
    DESCRIPTION: This test case verifies Group All Module on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'GROUP_ALL' should be created, enabled and set up in CMS
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_group_all_module(self):
        """
        DESCRIPTION: Go to Group All Module
        EXPECTED: 
        """
        pass

    def test_004_verify_group_all_module(self):
        """
        DESCRIPTION: Verify Group All Module
        EXPECTED: Group All Module is a table that consists of the next elements:
        EXPECTED: * 'POS' label and country position displayed in the column
        EXPECTED: * Country flag and abbreviation
        EXPECTED: * 'PTS' label and total matches value
        EXPECTED: * Market name and price odds for the first market (if available)
        EXPECTED: * Market name and price odds for the second market (if available)
        """
        pass

    def test_005_verify_country_position(self):
        """
        DESCRIPTION: Verify country position
        EXPECTED: Selected country position determines qualified teams within one Group (colored in dark blue)
        """
        pass

    def test_006_verify_markets_available(self):
        """
        DESCRIPTION: Verify markets available
        EXPECTED: * Maximum two markets can be displayed within Group All module
        EXPECTED: * The number of markets displayed corresponds to quantity of items recieved in **markets** array for Group All module from GET tab/sub tab response
        """
        pass
