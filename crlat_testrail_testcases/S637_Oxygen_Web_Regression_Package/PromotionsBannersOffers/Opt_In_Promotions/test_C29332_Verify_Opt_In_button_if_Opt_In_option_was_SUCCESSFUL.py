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
class Test_C29332_Verify_Opt_In_button_if_Opt_In_option_was_SUCCESSFUL(Common):
    """
    TR_ID: C29332
    NAME: Verify Opt In button if Opt In option was SUCCESSFUL
    DESCRIPTION: This test case verifies Opt In button if Opt In option was successful
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14803: Opt In Promotion Functionality
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    PRECONDITIONS: * Make sure Promotion with Opt In is configured in CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Navigate to Promotions page
    """
    keep_browser_open = True

    def test_001_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Opt In button is displayed on relevant Promotion page
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        pass

    def test_002_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option was successful
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        pass

    def test_003_check_opt_in_button_after_successful_opt_in_option(self):
        """
        DESCRIPTION: Check 'Opt In' button after successful Opt In option
        EXPECTED: The text which is contained within Opt In button is changed
        EXPECTED: This message is configurable within CMS.
        EXPECTED: For e.g.: 'Thanks, you are now opted in'
        """
        pass

    def test_004_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: - Opt In button is not clickable.
        EXPECTED: - Actions are not triggered.
        """
        pass

    def test_005_check_whether_user_is_eligible_to_receive_bonus_for_the_relevant_promotion(self):
        """
        DESCRIPTION: Check whether User is eligible to receive bonus for the relevant promotion
        EXPECTED: User is eligible to receive bonus for relevant promotion once promotion criteria is met
        """
        pass
