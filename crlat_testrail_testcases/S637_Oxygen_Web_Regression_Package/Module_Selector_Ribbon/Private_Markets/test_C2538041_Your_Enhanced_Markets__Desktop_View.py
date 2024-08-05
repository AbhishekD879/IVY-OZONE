import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C2538041_Your_Enhanced_Markets__Desktop_View(Common):
    """
    TR_ID: C2538041
    NAME: Your Enhanced Markets - Desktop View
    DESCRIPTION: 
    PRECONDITIONS: User should be eligible for one or more private enhanced market offers
    """
    keep_browser_open = True

    def test_001_login_with_user_eligible_for_one_or_more_private_enhanced_market_offers(self):
        """
        DESCRIPTION: Login with user eligible for one or more private enhanced market offers
        EXPECTED: *  Homepage is opened
        EXPECTED: *  'Your Enhanced Markets' section is present at the top of the page below Hero Header
        """
        pass

    def test_002_log_out_from_app_and_verify_your_enhanced_markets_section(self):
        """
        DESCRIPTION: Log out from app and verify 'Your Enhanced Markets' section
        EXPECTED: * 'Your Enhanced Markets' section is disappeared
        EXPECTED: * 'In-Play & Live Stream' section is displayed at the top
        """
        pass
