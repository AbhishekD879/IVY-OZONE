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
class Test_C9726412_Event_Hub_Verify_Surface_Bet_module_ordering_among_other_modules(Common):
    """
    TR_ID: C9726412
    NAME: Event Hub: Verify Surface Bet module ordering among other modules
    DESCRIPTION: Test case verifies possibility to order Surface Bet module among other modules
    PRECONDITIONS: 1. There is at least one Surface Bet added to the Event Hub in CMS.
    PRECONDITIONS: 2. There are other modules active and configured in CMS for this Event Hub
    PRECONDITIONS: 3. Open this Event Hub in Oxygen application.
    PRECONDITIONS: CMS path for the Event Hub: Sport Pages > Event Hub > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_order_of_the_surface_bet_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Surface Bet module is as per order in the CMS
        EXPECTED: The order is as defined in CMS
        """
        pass

    def test_002_change_the_order_in_the_cmsin_the_application__verify_the_order_is_updated_by_live_update(self):
        """
        DESCRIPTION: Change the order in the CMS.
        DESCRIPTION: In the application  verify the order is updated by live update
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
