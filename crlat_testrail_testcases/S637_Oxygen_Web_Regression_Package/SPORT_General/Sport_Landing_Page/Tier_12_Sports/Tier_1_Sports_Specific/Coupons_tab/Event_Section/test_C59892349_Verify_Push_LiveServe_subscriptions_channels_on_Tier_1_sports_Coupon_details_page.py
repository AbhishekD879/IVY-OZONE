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
class Test_C59892349_Verify_Push_LiveServe_subscriptions_channels_on_Tier_1_sports_Coupon_details_page(Common):
    """
    TR_ID: C59892349
    NAME: Verify Push LiveServe subscriptions channels on Tier 1 sports Coupon details page
    DESCRIPTION: This test case verifies push LiveServe subscriptions channels on Tier 1 sports Coupon details page (Basketball, Tennis)
    DESCRIPTION: (there is separate test case for Footbal - https://ladbrokescoral.testrail.com/index.php?/cases/view/59892343)
    PRECONDITIONS: **To see what CMS and TI is in use type "devlog" over opened application or go to URL:** https://your_environment/buildInfo.json
    PRECONDITIONS: **CMS:** https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: **TI:** https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **How to create a coupon:** https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Find or create two events with two markets for each of them.
    PRECONDITIONS: 2. Create coupon with this two events
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Open Basketball/Tennis Lading page
    PRECONDITIONS: **NOTE:** On Basketball/Tennis coupon details page only events from expaned module should be received in push > Request Payload
    """
    keep_browser_open = True

    def test_001_go_to_the_coupon_page_accas(self):
        """
        DESCRIPTION: Go to the Coupon Page (ACCAS)
        EXPECTED: Coupon page is loaded
        """
        pass

    def test_002_expand_one_accordion(self):
        """
        DESCRIPTION: Expand one accordion
        EXPECTED: Accourdion is expanded. Events are displayed
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
