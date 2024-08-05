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
class Test_C1490520_Verify_Outright_Module_Selections_Data(Common):
    """
    TR_ID: C1490520
    NAME: Verify Outright Module Selections Data
    DESCRIPTION: This test case verifies Outright Module Selections data correctness
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
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

    def test_003_go_to_outright_module_in_grid_view(self):
        """
        DESCRIPTION: Go to Outright Module in **GRID** view
        EXPECTED: 
        """
        pass

    def test_004_verify_each_way_terms_correctness(self):
        """
        DESCRIPTION: Verify each-way terms correctness
        EXPECTED: Each-way terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes from GET tab/subtab/module response
        """
        pass

    def test_005_verify_date_correctness(self):
        """
        DESCRIPTION: Verify date correctness
        EXPECTED: Date corresponds to **markets.[i].data.startTime** attribute from GET tab/subtab/module response
        """
        pass

    def test_006_verify_selection_name_correctness(self):
        """
        DESCRIPTION: Verify selection name correctness
        EXPECTED: Selection name corresponds to **markets.[i].data.markets.[j].outcomes.[k].participants.HOME/AWAY.name** attribute from GET tab/subtab/module response
        """
        pass

    def test_007_verify_priceodds_correctness(self):
        """
        DESCRIPTION: Verify Price/odds correctness
        EXPECTED: * Price/odds value corresponds to **markets.[i].data.markets.[j].outcomes.[k].participants.prices.priceDec**  in Decimal format
        EXPECTED: * Price/odds value corresponds to **markets.[i].data.markets.[j].outcomes.[k].participants.prices.priceNum** /
        EXPECTED: **markets.[i].data.markets.[j].outcomes.[k].participants.prices.priceDen** in Fractional format
        """
        pass

    def test_008_verify_selection_ordering(self):
        """
        DESCRIPTION: Verify selection ordering
        EXPECTED: * Selections are ordered by Price/odds value in ascending order
        EXPECTED: * Selections are ordered by alphabetical order if Price/odds value is the same
        """
        pass

    def test_009_go_to_outright_module_in_list_view(self):
        """
        DESCRIPTION: Go to Outright Module in **LIST** view
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_4_8(self):
        """
        DESCRIPTION: Repeat steps #4-8
        EXPECTED: 
        """
        pass

    def test_011_go_to_outright_module_in_card_view(self):
        """
        DESCRIPTION: Go to Outright Module in **CARD** view
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_6_8(self):
        """
        DESCRIPTION: Repeat steps #6-8
        EXPECTED: 
        """
        pass
