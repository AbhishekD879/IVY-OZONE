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
class Test_C28049_Offers_displaying_to_New_or_Existing_or_Both_users(Common):
    """
    TR_ID: C28049
    NAME: Offers displaying to New or Existing or Both users
    DESCRIPTION: This test case verifies Offers displaying to New or Existing or Both users
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True

    def test_001_clear_browser_cookies_and_load_oxygen_applicationdo_not_log_in_to_the_application_and_verify_offers_displaying(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application.
        DESCRIPTION: Do not log in to the application and verify Offers displaying.
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are displayed
        EXPECTED: *   Offers with 'Show for Existing Users' option value are NOT displayed
        """
        pass

    def test_002_log_in_to_the_application_for_the_first_time_using_the_browser_with_cleared_cookiesverify_cookie_creation_in_resources__gt_cookies(self):
        """
        DESCRIPTION: Log in to the application for the first time using the browser with cleared cookies.
        DESCRIPTION: Verify cookie creation in Resources -&gt; Cookies.
        EXPECTED: *   'ExistingUser: True' cookie is added
        """
        pass

    def test_003_verify_offers_displaying_after_cookie_existinguser_true_cookie_was_added(self):
        """
        DESCRIPTION: Verify Offers displaying after cookie 'ExistingUser: True' cookie was added
        EXPECTED: *   Offers with 'Show for Existing Users' option value are displayed
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are NOT displayed
        """
        pass

    def test_004_log_out_from_the_application_the_cookie_is_already_added_to_the_browserverify_offers_displaying_in_the_application(self):
        """
        DESCRIPTION: Log out from the application (the cookie is already added to the browser).
        DESCRIPTION: Verify Offers displaying in the application.
        EXPECTED: *   Offers with 'Show for Existing Users' option value are displayed
        EXPECTED: *   Offers with 'Show for Both' option value are displayed
        EXPECTED: *   Offers with 'Show for New Users' are NOT displayed
        """
        pass
