import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.promotions_banners_offers
@vtest
class Test_C9765388_Verify_showing_Eligible_Offers_to_the_Customer_upon_Login(Common):
    """
    TR_ID: C9765388
    NAME: Verify showing Eligible Offers to the Customer upon Login
    DESCRIPTION: This test case verifies that Targeted Promos ( Eligible Offers ) is shown for appropriate logged in user
    PRECONDITIONS: 1.  Promotions are created in CMS ( all other promotions that are displayed for all users)
    PRECONDITIONS: 2. Create two Targeted Promotions with OB Promo ID (use instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Targeted+Promotional+with+OB+Promo+ID
    PRECONDITIONS: **NOTE** USER1 is added to the SCV file for 'Invite Only' trigger
    PRECONDITIONS: Login with USER1
    """
    keep_browser_open = True

    def test_001_navigate_to_promotions_pageverify_that_created_targeted_promo_offer_is_shown(self):
        """
        DESCRIPTION: Navigate to Promotions page
        DESCRIPTION: Verify that created targeted promo offer is shown
        EXPECTED: - Created targeted promo offer is shown for User1
        EXPECTED: - All promotions  that are displayed for all users (with OB Promo Id field = empty) are shown
        """
        pass

    def test_002_logged_out_from_the_applicationstay_on_promotions_pageverify_that_created_targeted_promo_offer_is_not_shown(self):
        """
        DESCRIPTION: Logged out from the application
        DESCRIPTION: Stay on Promotions page
        DESCRIPTION: Verify that created targeted promo offer is NOT shown
        EXPECTED: - Created targeted promo offer is NOT shown
        EXPECTED: - All promotions other promotions that are displayed for all users are shown
        """
        pass

    def test_003_login_with_another_userstay_on_promotions_pageverify_that_created_targeted_promo_offer_for_user1_is_not_shown(self):
        """
        DESCRIPTION: Login with another User
        DESCRIPTION: Stay on Promotions page
        DESCRIPTION: Verify that created targeted promo offer for USER1 is NOT shown
        EXPECTED: - Created targeted promo offer for USER1 is NOT shown
        EXPECTED: - All promotions  that are displayed for all users (with OB Promo Id field = empty) are shown
        """
        pass
