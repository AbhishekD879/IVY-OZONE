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
class Test_C1489743_Verify_Outright_Module_Subpanel_Data(Common):
    """
    TR_ID: C1489743
    NAME: Verify Outright Module Subpanel Data
    DESCRIPTION: This test case verifies Outright Module Subpanel Data
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * 1 Module with type = 'OUTRIGHTS' should be created, enabled and set up in CMS
    PRECONDITIONS: * A few active markets should be added to Outight Module
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab/module by ID request
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
        """
        pass

    def test_003_go_to_outright_module(self):
        """
        DESCRIPTION: Go to Outright Module
        EXPECTED: Outright Module consists of Subpanels and market data
        """
        pass

    def test_004_verify_the_number_of_market_subpanel_displayed_within_outright_module(self):
        """
        DESCRIPTION: Verify the number of Market Subpanel displayed within Outright Module
        EXPECTED: The number of Market Subpanel corresponds to the quantity of items in **markets** array in GET tab/subtab/module response
        """
        pass

    def test_005_verify_market_subpaneles_ordering(self):
        """
        DESCRIPTION: Verify Market Subpaneles ordering
        EXPECTED: Market Subpaneles are ordered in ascending order as received in **markers** array in GET tab/subtab/module response
        """
        pass

    def test_006_verify_market_subpanel_name_correctness(self):
        """
        DESCRIPTION: Verify Market Subpanel name correctness
        EXPECTED: Market Subpanel name corresponds to **competitionModules.[i].markets.[j].nameOverride** attribute from GET tab/subtab/module response
        EXPECTED: where
        EXPECTED: i - the number of all Modules created
        EXPECTED: j- the number of all Markets created in Market
        """
        pass

    def test_007_verify_market_subpanel_state(self):
        """
        DESCRIPTION: Verify Market Subpanel state
        EXPECTED: * Market Subpanel is displayed in collapsed state if **competitionModules.[i].markets.[j].collapsed**= **true** in GET tab/subtab/module response
        EXPECTED: * Market Subpanel is displayed in expanded state if **competitionModules.[i].markets.[j].collapsed**= **false** in GET tab/subtab/module response
        EXPECTED: where
        EXPECTED: i - the number of all Modules created
        EXPECTED: j- the number of all Markets created in Market
        """
        pass

    def test_008_verify_market_subpanel(self):
        """
        DESCRIPTION: Verify Market Subpanel
        EXPECTED: * Its possible to expand Market Subpanel  by taping '+' sign or Market Subpanel
        EXPECTED: * Its possible to collapse Market Subpanel by taping '-' sign or Market Subpanel
        """
        pass
