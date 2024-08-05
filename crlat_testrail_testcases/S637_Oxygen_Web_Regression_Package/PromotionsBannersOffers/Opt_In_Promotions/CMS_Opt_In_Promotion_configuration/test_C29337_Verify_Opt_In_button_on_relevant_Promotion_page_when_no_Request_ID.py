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
class Test_C29337_Verify_Opt_In_button_on_relevant_Promotion_page_when_no_Request_ID(Common):
    """
    TR_ID: C29337
    NAME: Verify Opt In button on relevant Promotion page when no Request ID
    DESCRIPTION: This test case verifies Opt In button on relevant Promotion page when no Request ID is entered and Opt In button is inputted into description
    DESCRIPTION: JIRA Ticket:
    DESCRIPTION: BMA-14801: CMS: Opt In Promotion Config & Success/ Error Message
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please,  see C29336
    PRECONDITIONS: NOTE: For caching needs Akamai service is used on TST2/ STG environment, so after saving changes in CMS there clould be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_make_sure_promotion_with_added_opt_in_button_and_without_request_id_is_configured_within_cms(self):
        """
        DESCRIPTION: Make sure Promotion with added Opt In button and without Request ID is configured within CMS
        EXPECTED: 
        """
        pass

    def test_002_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_003_find_a_promotion_is_configured_within_cms(self):
        """
        DESCRIPTION: Find a Promotion is configured within CMS
        EXPECTED: Promotion page is opened
        """
        pass

    def test_004_check_an_opt_in_button(self):
        """
        DESCRIPTION: Check an 'Opt In' button
        EXPECTED: 'Opt In' button is not displayed on relevant Promotion page
        """
        pass
