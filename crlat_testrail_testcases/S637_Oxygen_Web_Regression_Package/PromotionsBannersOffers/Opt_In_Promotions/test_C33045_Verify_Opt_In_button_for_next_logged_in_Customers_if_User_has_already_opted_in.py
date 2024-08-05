import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C33045_Verify_Opt_In_button_for_next_logged_in_Customers_if_User_has_already_opted_in(Common):
    """
    TR_ID: C33045
    NAME: Verify Opt In button for next logged in Customers if User has already opted in
    DESCRIPTION: This test case verifies Opt In button for next logged in Customers if User has already opted in
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14803: Opt In Promotion Functionality
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True

    def test_001_make_sure_promotion_with_opt_in_button_is_configured_in_cms(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In button is configured in CMS
        EXPECTED: 
        """
        pass

    def test_002_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_003_go_to_promotions_page(self):
        """
        DESCRIPTION: Go to 'Promotions' page
        EXPECTED: 'Promotions' page with configured Promotion is opened
        """
        pass

    def test_004_find_a_configured_promotion_with_opt_in_button(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In button
        EXPECTED: Opt in button is available on Promotion page
        """
        pass

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option is successful.
        EXPECTED: Success message is contained on Opt In.
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_007_find_a_configured_promotion_with_opt_in_button(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In button
        EXPECTED: Opt In button is not displayed
        """
        pass

    def test_008_log_in_next_account(self):
        """
        DESCRIPTION: Log in next account
        EXPECTED: User is logged in
        """
        pass

    def test_009_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: 
        """
        pass
