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
class Test_C50047_Verify_display_Opt_In_button_on_relevant_Promotions_page(Common):
    """
    TR_ID: C50047
    NAME: Verify display Opt In button on relevant Promotion's page
    DESCRIPTION: This test case verifies display Opt In button on relevant Promotion's page for logged out User
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Promotional+Opt+In+trigger
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True

    def test_001_make_sure_promotion_with_opt_in_is_configured_in_cms(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In is configured in CMS
        EXPECTED: 
        """
        pass

    def test_002_open_promotions_page(self):
        """
        DESCRIPTION: Open 'Promotions' page
        EXPECTED: 'Promotions' landing page is opened
        """
        pass

    def test_003_check_promotions_landing_page(self):
        """
        DESCRIPTION: Check 'Promotions' landing page
        EXPECTED: Opt In button is NOT displayed on 'Promotions' landing page
        """
        pass

    def test_004_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: Promotion page is opened
        """
        pass

    def test_005_check_a_promotion_page(self):
        """
        DESCRIPTION: Check a Promotion page
        EXPECTED: Opt In button is displayed on relevant Promotion page
        """
        pass

    def test_006_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: 
        """
        pass
