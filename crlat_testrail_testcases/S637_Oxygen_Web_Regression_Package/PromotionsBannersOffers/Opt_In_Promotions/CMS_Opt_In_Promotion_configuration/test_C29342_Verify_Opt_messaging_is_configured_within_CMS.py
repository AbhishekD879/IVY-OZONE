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
class Test_C29342_Verify_Opt_messaging_is_configured_within_CMS(Common):
    """
    TR_ID: C29342
    NAME: Verify Opt messaging is configured within CMS
    DESCRIPTION: This test case verifies ability to configure Opt In messaging with CMS System configuration
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14801: CMS: Opt In Promotion Config & Success/ Error message
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    PRECONDITIONS: NOTE: For caching needs Akamai service is used on TST2/ STG environment, so after saving changes in CMS there clould be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_system_configuration_page(self):
        """
        DESCRIPTION: Go to 'System configuration' page
        EXPECTED: System configuration page is opened
        """
        pass

    def test_003_find_a_optinmessaging_tab(self):
        """
        DESCRIPTION: Find a 'OPTINMESSAGING' tab
        EXPECTED: 'OPTINMESSAGING' tab is present
        """
        pass

    def test_004_check_options_in_the_optinmessaging(self):
        """
        DESCRIPTION: Check options in the 'OPTINMESSAGING'
        EXPECTED: - 'successMessage' option is present
        EXPECTED: - 'alreadyOptedInMessage' option is present
        EXPECTED: - 'errorMessage' option is present
        """
        pass

    def test_005_enter_relevant_messages_into_relevant_fields(self):
        """
        DESCRIPTION: Enter relevant messages into relevant fields
        EXPECTED: - Some success message is entered into 'successMessage' field
        EXPECTED: - Some error message is entered into 'errorMessage' field
        EXPECTED: - Some already opted in message is entered into 'alreadyOptedInMessage' field
        """
        pass

    def test_006_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: Changes are saved successfuly
        """
        pass

    def test_007_make_sure_promotions_with_opt_in_buttons_is_configured_within_cms(self):
        """
        DESCRIPTION: Make sure Promotion(s) with Opt In button(s) is configured within CMS
        EXPECTED: 
        """
        pass

    def test_008_load_oxygen_and_log_in_account(self):
        """
        DESCRIPTION: Load Oxygen and log in account
        EXPECTED: User is logged in
        """
        pass

    def test_009_find_and_open_configured_promotions(self):
        """
        DESCRIPTION: Find and open configured Promotion(s)
        EXPECTED: Promotion page with Opt In button is opened
        """
        pass

    def test_010_trigger_opt_in_option_is_successful(self):
        """
        DESCRIPTION: Trigger Opt In option is successful
        EXPECTED: 
        """
        pass

    def test_011_check_a_successful_message(self):
        """
        DESCRIPTION: Check a successful message
        EXPECTED: Success message as per configuration within CMS is displayed
        """
        pass

    def test_012_navigate_from_promotion_page_and_re_visit_the_same_promotion_again(self):
        """
        DESCRIPTION: Navigate from Promotion page and re-visit the same Promotion again
        EXPECTED: 
        """
        pass

    def test_013_check_already_opted_in_message_on_opt_in_button(self):
        """
        DESCRIPTION: Check already opted in message on Opt In button
        EXPECTED: Already opted in message as per configuration within CMS is dispalyed
        """
        pass

    def test_014_trigger_opt_in_option_is_unsuccessful(self):
        """
        DESCRIPTION: Trigger Opt In option is unsuccessful
        EXPECTED: 
        """
        pass

    def test_015_check_an_error_message(self):
        """
        DESCRIPTION: Check an error message
        EXPECTED: Error message as per configuration within CMS is displayed
        """
        pass
