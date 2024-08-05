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
class Test_C50313_Verify_Opt_In_button_after_re_logging_with_the_same_User(Common):
    """
    TR_ID: C50313
    NAME: Verify Opt In button after re-logging with the same User
    DESCRIPTION: This test case verifies Opt In button after relogging with the same User from Promotion page
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

    def test_002_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
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
        EXPECTED: - Opt In button is displayed
        EXPECTED: - 'fired': 'false' is sent in the Request ID response
        """
        pass

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: - Opt In option was successful
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        EXPECTED: - Opt In button contains success message
        """
        pass

    def test_006_complete_the_offer_conditions_after_opted_in(self):
        """
        DESCRIPTION: Complete the Offer conditions after opted in
        EXPECTED: - Offer conditions is completed
        EXPECTED: - User gets reward
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_008_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Promotion page is opened
        EXPECTED: - Opt In button is displayed as per CMS configuration
        EXPECTED: - Relevant request Opt In ID is NOT sent
        """
        pass

    def test_009_tap_on_opt_in_button_and_log_in(self):
        """
        DESCRIPTION: Tap on 'Opt In' button and log in
        EXPECTED: User is logged in on relevant Promotion page
        """
        pass

    def test_010_check_opt_in_button_once_after_logging_in(self):
        """
        DESCRIPTION: Check Opt In button once after logging in
        EXPECTED: - Opt In button appears and contains already opted in message
        EXPECTED: - Opt In button is diseble
        EXPECTED: - 'fired': 'true' is sent in the Request ID response
        """
        pass
