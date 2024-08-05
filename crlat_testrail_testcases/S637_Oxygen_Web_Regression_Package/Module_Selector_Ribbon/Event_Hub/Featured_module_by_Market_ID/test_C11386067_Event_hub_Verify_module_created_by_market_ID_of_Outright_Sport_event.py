import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11386067_Event_hub_Verify_module_created_by_market_ID_of_Outright_Sport_event(Common):
    """
    TR_ID: C11386067
    NAME: Event hub: Verify module created by market ID of Outright <Sport> event
    DESCRIPTION: This test case verifies featured module created by market ID of Outright <Sport> event
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Outright event created in TI
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS >  Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True

    def test_001_navigate_to_module_from_preconditions_make_sure_its_expanded_and_verify_its_contents(self):
        """
        DESCRIPTION: Navigate to Module from preconditions. Make sure it's expanded and verify it's contents
        EXPECTED: * Module name corresponds to Name set in CMS
        EXPECTED: * Selections are ordered by:
        EXPECTED: Price / Odds in ascending order
        EXPECTED: Alphabetically by selection name - if prices are the same
        EXPECTED: * Price buttons located at the right of each selection containing prices set in TI
        EXPECTED: * No info about event name/start time present in the module
        """
        pass
