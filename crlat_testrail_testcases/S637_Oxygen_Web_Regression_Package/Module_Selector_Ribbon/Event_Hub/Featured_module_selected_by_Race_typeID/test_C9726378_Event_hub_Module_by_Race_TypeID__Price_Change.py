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
class Test_C9726378_Event_hub_Module_by_Race_TypeID__Price_Change(Common):
    """
    TR_ID: C9726378
    NAME: Event hub: Module by <Race> TypeID - Price Change
    DESCRIPTION: This test case verifies situation when price is changed for  the 'Primary market' on the 'Event hub' tab (mobile/tablet) on a module by <Race> TypeID
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport pages > Event hub. Module by <Race> TypeID is created in Event Hub and contains events
    PRECONDITIONS: 2. User is on Homepage > Event hub tab
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
        EXPECTED: * The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Other buttons are not changed if they are available
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

    def test_006_trigger_price_change_for_3_outcomes_of_any_event_from_module(self):
        """
        DESCRIPTION: Trigger price change for 3 outcomes of any event from Module
        EXPECTED: The 'Price/Odds' buttons are displayed new prices immediately and they change its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        """
        pass
