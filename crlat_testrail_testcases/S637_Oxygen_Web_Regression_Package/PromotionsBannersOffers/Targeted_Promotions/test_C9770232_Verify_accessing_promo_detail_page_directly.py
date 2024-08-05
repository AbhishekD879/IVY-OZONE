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
class Test_C9770232_Verify_accessing_promo_detail_page_directly(Common):
    """
    TR_ID: C9770232
    NAME: Verify accessing promo detail page directly
    DESCRIPTION: This test case verifies that all promotion details page is shown regardless of Openbet or IMS VIP segmentation when going to the "deep linked URL" of Promo Detail Page directly
    PRECONDITIONS: Create Targeted Promotion with OB Promo ID (use instruction:  [How to setup and use Targeted Promotional with OB Promo ID](https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Targeted+Promotional+with+OB+Promo+ID/))
    PRECONDITIONS: **NOTE**  USER1 is added to the SCV file for 'Invite Only' trigger
    PRECONDITIONS: Login with USER1 and navigate to the Promotion page
    """
    keep_browser_open = True

    def test_001_select_created_promotionverify_that_promotion_detail_page_is_openednote_copy_url_of_the_promotion_details_page_and_save_to_somewhere(self):
        """
        DESCRIPTION: Select created promotion
        DESCRIPTION: Verify that promotion detail page is opened
        DESCRIPTION: NOTE: Copy URL of the Promotion details page and save to somewhere
        EXPECTED: Promotion detail page is opened
        """
        pass

    def test_002_navigate_to_home_page_and_log_outpast_url_of_the_promotion_details_pageverify_that_promotion_detail_page_for_the_promotion_is_opened(self):
        """
        DESCRIPTION: Navigate to Home page and log out
        DESCRIPTION: Past URL of the Promotion details page
        DESCRIPTION: Verify that promotion detail page for the promotion is opened
        EXPECTED: Promotion detail page for the promotion is opened
        """
        pass

    def test_003_navigate_to_home_page_and_log_outlogin_with_a_different_user_for_this_offer_is_unavailablepast_url_of_the_promotion_details_pageverify_that_promotion_detail_page_for_the_promotion_is_opened(self):
        """
        DESCRIPTION: Navigate to Home page and log out
        DESCRIPTION: Login with a different user (for this offer is unavailable)
        DESCRIPTION: Past URL of the Promotion details page
        DESCRIPTION: Verify that promotion detail page for the promotion is opened
        EXPECTED: Promotion detail page for the promotion is opened
        """
        pass
