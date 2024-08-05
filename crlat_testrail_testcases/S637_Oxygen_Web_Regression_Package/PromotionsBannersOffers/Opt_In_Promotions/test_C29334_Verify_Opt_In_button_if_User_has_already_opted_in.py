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
class Test_C29334_Verify_Opt_In_button_if_User_has_already_opted_in(Common):
    """
    TR_ID: C29334
    NAME: Verify Opt In button if User has already opted in
    DESCRIPTION: This test case verifies Opt In button if User revisits a Promotion page and has already opted in
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14803: Opt In Promotion Functionality
    PRECONDITIONS: There is Promotion(s) with Opt In.
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    PRECONDITIONS: * Make sure Promotion with Opt In is configured in CMS
    PRECONDITIONS: * User is logged in
    """
    keep_browser_open = True

    def test_001_go_to_promotions_page(self):
        """
        DESCRIPTION: Go to 'Promotions' page
        EXPECTED: 'Promotions' page with configured Promotion is opened
        """
        pass

    def test_002_find_a_configured_promotion_with_opt_in(self):
        """
        DESCRIPTION: Find a configured Promotion with Opt In
        EXPECTED: - Opt In button is displayed on relevent Promotion page
        EXPECTED: - Request ID with username and token is sent in the devtool-> Network
        EXPECTED: - 'fired': 'false' in sent in the Request ID response
        """
        pass

    def test_003_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on 'Opt In' button
        EXPECTED: Opt In option was successful
        EXPECTED: - 'trigger' request with 'trigger_id' is sent
        EXPECTED: - 'fired': 'true' is sent in the 'trigger' response
        """
        pass

    def test_004_navigate_from_promotion_page(self):
        """
        DESCRIPTION: Navigate from Promotion page
        EXPECTED: 
        """
        pass

    def test_005_revisit_the_same_configured_promotion(self):
        """
        DESCRIPTION: Revisit the same configured Promotion
        EXPECTED: Opt In button is dispalyed on relevant Promotion page
        EXPECTED: - 'fired': 'true' is sent in the Request ID response
        """
        pass

    def test_006_make_sure_there_is_no_buttons_blink_once_promotion_page_is_opened(self):
        """
        DESCRIPTION: Make sure there is no button's blink once Promotion page is opened
        EXPECTED: Opt In button can appears spinner of loading.
        EXPECTED: There is no blink of previous message once Promotion page is opened.
        """
        pass

    def test_007_check_the_opt_in_button(self):
        """
        DESCRIPTION: Check the Opt In button
        EXPECTED: - Opt In button contains the message 'You're already opted in'.
        EXPECTED: - This message is configurable within CMS.
        EXPECTED: - Opt In button contains the icon.
        """
        pass

    def test_008_click_on_opt_in_button_again(self):
        """
        DESCRIPTION: Click on Opt In button again
        EXPECTED: - Opt In button is not clickable.
        EXPECTED: - Actions are not triggered.
        """
        pass
