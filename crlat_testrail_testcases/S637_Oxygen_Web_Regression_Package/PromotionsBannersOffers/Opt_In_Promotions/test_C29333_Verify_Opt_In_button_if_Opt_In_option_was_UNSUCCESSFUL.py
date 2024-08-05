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
class Test_C29333_Verify_Opt_In_button_if_Opt_In_option_was_UNSUCCESSFUL(Common):
    """
    TR_ID: C29333
    NAME: Verify Opt In button if Opt In option was UNSUCCESSFUL
    DESCRIPTION: This test case verifies Opt In button and error message if Opt In option was UNSUCCESSFUL
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14803: Opt In Promotion Functionality
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    """
    keep_browser_open = True

    def test_001_make_seru_promotion_with_opt_in_is_configured_in_cms(self):
        """
        DESCRIPTION: Make seru Promotion with Opt In is configured in CMS
        EXPECTED: 
        """
        pass

    def test_002_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_003_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_004_go_to_promotions(self):
        """
        DESCRIPTION: Go to 'Promotions'
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_005_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: Opt In button is displayed on relevant Promotion page
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        pass

    def test_006_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option was unsuccessful:
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'false' is sent in the 'trigger' response
        """
        pass

    def test_007_check_opt_in_button_after_unsuccessful_opt_in_option(self):
        """
        DESCRIPTION: Check Opt In button after unsuccessful Opt In option
        EXPECTED: Relevant error message appears above Opt In button
        """
        pass

    def test_008_check_the_error_message_formatting(self):
        """
        DESCRIPTION: Check the error message formatting
        EXPECTED: - Error message appears as tooltip
        EXPECTED: - Error message has yellow background
        EXPECTED: - Bubble message appears on the left side above button
        EXPECTED: - Text of message is configured within CMS
        """
        pass
