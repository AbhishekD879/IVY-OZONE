import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C11087708_Featured_module_by_Sport_Event_ID_Price_Change(Common):
    """
    TR_ID: C11087708
    NAME: Featured module by <Sport> Event ID: Price Change
    DESCRIPTION: This test case verifies situation when price is changed for outcomes of  market on the EventHub tab (mobile/tablet)
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Module by <Sport> EventId(not Outright Event with primary market) is created in EventHub and contains event
    PRECONDITIONS: 3. User is on Homepage > EventHub tab
    PRECONDITIONS: 4. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
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