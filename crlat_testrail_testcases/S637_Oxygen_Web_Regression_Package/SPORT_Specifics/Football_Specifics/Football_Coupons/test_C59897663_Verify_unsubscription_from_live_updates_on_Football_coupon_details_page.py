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
class Test_C59897663_Verify_unsubscription_from_live_updates_on_Football_coupon_details_page(Common):
    """
    TR_ID: C59897663
    NAME: Verify unsubscription from live updates on Football coupon details page
    DESCRIPTION: This test case verifies unsubscription from live updates on Football coupon details page after navigation to anywhere else
    PRECONDITIONS: **To see what CMS and TI is in use type "devlog" over opened application or go to URL:** https://your_environment/buildInfo.json
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
        EXPECTED: sEVENTsEVMKTSEVMKT (for each market there should be separate sEVMKTSEVMKT) is received
        """
        pass

    def test_004_navigate_to_any_other_page_and_check_unsubcription(self):
        """
        DESCRIPTION: Navigate to any other page and check unsubcription
        EXPECTED: Previous push is closed with Request Payload: CL0000
        EXPECTED: ![](index.php?/attachments/get/118934724)
        """
        pass

    def test_005_trigger_price_update_for_event_from_coupon_details_page(self):
        """
        DESCRIPTION: Trigger price update for event from coupon details page
        EXPECTED: push > Request Payload > sEVENTsEVMKTSEVMKT (for each market there should be separate sEVMKTSEVMKT) isn't received
        """
        pass
