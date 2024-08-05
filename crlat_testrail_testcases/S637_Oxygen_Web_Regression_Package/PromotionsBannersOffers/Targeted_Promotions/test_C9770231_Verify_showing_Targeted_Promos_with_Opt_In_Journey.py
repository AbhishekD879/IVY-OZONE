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
class Test_C9770231_Verify_showing_Targeted_Promos_with_Opt_In_Journey(Common):
    """
    TR_ID: C9770231
    NAME: Verify showing Targeted Promos with Opt In Journey
    DESCRIPTION: This test case verifies showing Targeted Promos with Opt In Journey
    PRECONDITIONS: Use Instructions to create Promotion:
    PRECONDITIONS: [How to setup and use Promotional Opt In trigger](https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Promotional+Opt+In+trigger/)
    PRECONDITIONS: [How to setup and use Targeted Promotional with OB Promo ID](https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Targeted+Promotional+with+OB+Promo+ID/)
    PRECONDITIONS: [TC: Verify Opt In BMA button when creating Promotions](https://ladbrokescoral.testrail.com/index.php?/cases/view/29336/)
    PRECONDITIONS: Create a promotion with OB Promo ID and with Opt In Request ID (The one offer should be created with appropriate triggers)
    PRECONDITIONS: NOTE: USER1 is added to the SCV file for 'Invite Only' trigger
    """
    keep_browser_open = True

    def test_001_navigate_to_promotion_pageverify_that_created_in_preconditions_offer_is_not_shownkeep_in_mind_that_this_is_targeted_promo_with_opt_it_button(self):
        """
        DESCRIPTION: Navigate To Promotion Page
        DESCRIPTION: Verify that created in preconditions offer is NOT shown
        DESCRIPTION: (keep in mind that this is targeted promo with opt-it button)
        EXPECTED: Created in preconditions offer is NOT shown
        """
        pass

    def test_002_login_with_user1verify_that_created_in_preconditions_offer_is_shown_in_promotions_page(self):
        """
        DESCRIPTION: Login with User1.
        DESCRIPTION: Verify that created in preconditions offer is shown in Promotions page
        EXPECTED: Created in preconditions offer is shown
        """
        pass

    def test_003_open_promotion_details_page(self):
        """
        DESCRIPTION: open Promotion details page
        EXPECTED: Opt In button is displayed on the page
        """
        pass

    def test_004_tap_on_opt_in_buttonverify_that__trigger_request_with_trigger_id_is_sent(self):
        """
        DESCRIPTION: Tap on Opt In button
        DESCRIPTION: Verify that  'trigger' request with 'trigger_id' is sent
        EXPECTED: - Opt In button contains success message
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        pass
