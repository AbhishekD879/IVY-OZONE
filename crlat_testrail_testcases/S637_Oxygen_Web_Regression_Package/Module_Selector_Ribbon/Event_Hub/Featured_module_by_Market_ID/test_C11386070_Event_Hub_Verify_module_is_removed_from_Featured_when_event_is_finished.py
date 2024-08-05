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
class Test_C11386070_Event_Hub_Verify_module_is_removed_from_Featured_when_event_is_finished(Common):
    """
    TR_ID: C11386070
    NAME: Event Hub: Verify module is removed from Featured when event is finished
    DESCRIPTION: This test case verifies module is removed from Event Hub tab when event is finished
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 3. Featured module by Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 4. User is on Homepage > Event Hub tab
    PRECONDITIONS: 5. To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    """
    keep_browser_open = True

    def test_001_find_module_from_preconditions(self):
        """
        DESCRIPTION: Find module from preconditions
        EXPECTED: Module displayed with correct event/outcomes
        """
        pass

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: * Live update with type EVENT is received in WS with attribute 'displayed="N"
        EXPECTED: * Module is removed from Featured tab
        """
        pass
