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
class Test_C59892343_Verify_Push_LiveServe_subscriptions_channels_on_Football_Coupon_details_page(Common):
    """
    TR_ID: C59892343
    NAME: Verify Push LiveServe subscriptions channels on Football Coupon details page
    DESCRIPTION: This test case verifies Push LiveServe subscriptions channels on Football Coupon details page
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: **CMS:** https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: **TI:** https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **How to create a coupon:** https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Find or create two events with two markets for each of them.
    PRECONDITIONS: 2. Create coupon with this two events
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Open Football Lading page
    PRECONDITIONS: **NOTE:** On Football coupon details page all the events should be received in push > Request Payload (from collapsed and expanded accordions)
    """
    keep_browser_open = True

    def test_001_go_to_the_coupon_page_accas(self):
        """
        DESCRIPTION: Go to the Coupon Page (ACCAS)
        EXPECTED: Coupon page is loaded
        """
        pass

    def test_002_open_coupon_details_page_from_preconditions(self):
        """
        DESCRIPTION: Open coupon details page from preconditions
        EXPECTED: Coupon details page is loaded. Events are displayed
        """
        pass

    def test_003_check_push__request_payload(self):
        """
        DESCRIPTION: Check push > Request Payload
        EXPECTED: **sEVENTsEVMKTSEVMKT** (for each market there should be separate **sEVMKTSEVMKT**) is received
        """
        pass

    def test_004_trigger_price_update(self):
        """
        DESCRIPTION: Trigger price update
        EXPECTED: Price update is received on UI
        """
        pass

    def test_005_check_push__request_payload(self):
        """
        DESCRIPTION: Check push > Request Payload
        EXPECTED: **sEVENTsEVMKTSEVMKT** (for each market there should be separate **sEVMKTSEVMKT**) is received
        """
        pass
