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
class Test_C50111_Verify_Opt_In_button_for_logged_out_User_who_is_NOT_opted_in(Common):
    """
    TR_ID: C50111
    NAME: Verify Opt In button for logged out User who is NOT opted in
    DESCRIPTION: This test cases verifies Opt In button for logged out User who is not already opted in
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+setup+and+use+Promotional+Opt+In+trigger
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

    def test_002_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: User is not logged in
        """
        pass

    def test_003_go_to_promotions_from_sports_ribbon(self):
        """
        DESCRIPTION: Go to 'Promotions' from sports ribbon
        EXPECTED: 'Promotions' landing page is opened
        """
        pass

    def test_004_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        EXPECTED: - Relevant request Opt In ID is NOT sent
        """
        pass

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Log in pop-up appears
        """
        pass

    def test_006_enter_valid_name_and_password(self):
        """
        DESCRIPTION: Enter valid name and password
        EXPECTED: User is logged in on relevant Promotion page
        """
        pass

    def test_007_check_opt_in_button_on_relevant_promotion_page_once_after_logging_in(self):
        """
        DESCRIPTION: Check 'Opt In' button on relevant Promotion page once after logging in
        EXPECTED: - Opt In button appears
        EXPECTED: - Opt In button contains success message
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        pass
