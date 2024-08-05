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
class Test_C1641513_Verify_Group_All_Module_data_correctness(Common):
    """
    TR_ID: C1641513
    NAME: Verify Group All Module data correctness
    DESCRIPTION: This test case verifies Group All Module data correctness on Big Competition page
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

    def test_004_verify_the_number_of_countiresteams_displayed_with_group_individual_module(self):
        """
        DESCRIPTION: Verify the number of countires/teams displayed with Group Individual Module
        EXPECTED: The number of countires/teams displayed with Group Individual Module corresponds to quantity fo itrems recieved in **teams** array from GET tab/sub tab response
        """
        pass

    def test_005_verify_number_of_qualified_countries(self):
        """
        DESCRIPTION: Verify number of qualified countries
        EXPECTED: The number of qualified countries corresponds to **competitionModules.[i].groupModuleData.numberQualifiers** attribute from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        """
        pass

    def test_006_verify_team_abbreviation_and_flag_correctness(self):
        """
        DESCRIPTION: Verify team abbreviation and flag correctness
        EXPECTED: * Team abbreviation value corresponds to **competitionModules[i].groupModuleData.data.[].team[j].abbreviation** GET tab/sub tab response
        EXPECTED: * Flag is displayed if **competitionModules[i].groupModuleData.data.[].team[j].svgId** attribute is present and NOT empty in  GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j -  the number of all team returned for particular Group
        """
        pass

    def test_007_verify_total_points_value_correctness(self):
        """
        DESCRIPTION: Verify total points value correctness
        EXPECTED: Total points value corresponds to **competitionModules[i].groupModuleData.data.[].team[j].totalPoints** GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j -  the number of all team returned for particular Group
        """
        pass

    def test_008_verify_name_of_market_correctness(self):
        """
        DESCRIPTION: Verify name of market correctness
        EXPECTED: Name of market corresponds to **competitionModules[i].groupModuleData.data.[].ssEvents.[].markets.[j].name** from GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j -  the number of markets returned from Group All module
        """
        pass

    def test_009_verify_price_odds_correctness(self):
        """
        DESCRIPTION: Verify price odds correctness
        EXPECTED: * Price odds corresponds to **competitionModules[i].groupModuleData.data.[].ssEvents.[].markets.[j].outcomes.[k].prices.priceDec** attribute in Decimal Format
        EXPECTED: * Price odds corresponds to **competitionModules[i].groupModuleData.data.[].ssEvents.[].markets.[j].outcomes.[k].prices.priceDen** / **priceDec** in Fractional format
        EXPECTED: * Price odds is set to **'N/A'** if **isDisplayed=true** attribute is NOT received on outcome/market/event levels in GET tab/sub tab response
        EXPECTED: where
        EXPECTED: i - the number of all Modules returned to particular Tab/Sub Tab
        EXPECTED: j -  the number of markets returned from Group All module
        EXPECTED: k - the number of outcomes returned for market
        """
        pass
