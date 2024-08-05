import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C11049256_Featured_module_by_Market_ID_Price_Change(Common):
    """
    TR_ID: C11049256
    NAME: Featured module by Market ID: Price Change
    DESCRIPTION: This test case verifies situation when a price is changed for outcomes of the market on the 'Featured' tab (mobile/tablet) of a module by MarketID
    DESCRIPTION: Please update test case- race modules can not be collapsed/expanded. race modules should be created expanded only
    PRECONDITIONS: 1. Module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in CMS and contains event
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: Other buttons are not changed if they are available
        """
        pass

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: 
        """
        pass

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        pass

    def test_006_trigger_price_change_for_a_few_outcomes_from_the_same_market(self):
        """
        DESCRIPTION: Trigger price change for a few outcomes from the same market
        EXPECTED: All 'Price/Odds' buttons display new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        """
        pass
