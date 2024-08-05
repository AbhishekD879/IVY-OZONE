import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29494_Affiliate_Tracking_for_non_income_access_traffic(Common):
    """
    TR_ID: C29494
    NAME: Affiliate Tracking for non-income access traffic
    DESCRIPTION: This Test Case verifies Affiliate Tracking for non-income access traffic
    DESCRIPTION: **Jira Ticket: **BMA-6939 Affiliate Tracking for non-income access traffic (via direct URLs)
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   Cache and cookies are cleared
    PRECONDITIONS: *   Browser console is opened (Resources-> Cookies -> invictus.coral.co.uk)
    PRECONDITIONS: *   UAT is available to check values set in IMS
    PRECONDITIONS: *   Configure link in one of the following formats:
    PRECONDITIONS: 1.  https://invictus.coral.co.uk/#/betslip/add/[event\_id]?id=N&member=[member\_value]&profile=[profile\_value]&creferer=[creferer\_value]
    PRECONDITIONS: 2.  https://invictus.coral.co.uk/#/?id=N?member=[member\_value]&profile=[profile\_value]&creferer=[creferer_value]
    PRECONDITIONS: 3.  https://invictus.coral.co.uk/#/football?id=N?member=[member\_value]&profile=[profile\_value]&creferer=[creferer_value]
    PRECONDITIONS: 4.  https://invictus.coral.co.uk/#/in-play?id=N?member=[member\_value]&profile=[profile\_value]&creferer=[creferer_value]
    """
    keep_browser_open = True

    def test_001_launch_one_of_the_urls_configured_in_preconditions(self):
        """
        DESCRIPTION: Launch one of the URLs configured in Preconditions
        EXPECTED: 
        """
        pass

    def test_002_check_in_cookies_section_if_banner_domaiclick_cookie_was_set(self):
        """
        DESCRIPTION: Check in Cookies section if 'banner_domaiclick' cookie was set
        EXPECTED: The following query string parameters should be taken from URL and be stored in 'banner_domainclick' cookie:
        EXPECTED: *   member;
        EXPECTED: *   profile;
        EXPECTED: *   creferer.
        """
        pass

    def test_003_tap_on_join_button_and_proceed_with_registration_flow(self):
        """
        DESCRIPTION: Tap on 'Join' button and proceed with Registration flow
        EXPECTED: User is successfully registered.
        """
        pass

    def test_004_verify_values_set_in_ims___advertiser___profileid___creferer(self):
        """
        DESCRIPTION: Verify values set  in IMS:
        DESCRIPTION: *   advertiser
        DESCRIPTION: *   profileid
        DESCRIPTION: *   creferer
        EXPECTED: The folowing values are set in IMS:
        EXPECTED: *   advertiser = [member_value];
        EXPECTED: *   profileid = [profile_value];
        EXPECTED: *   creferer = BTAG:[creferer_value].
        """
        pass

    def test_005_launch_any_other_url_from_precondition_with_another_values(self):
        """
        DESCRIPTION: Launch any other URL from Precondition (with another values)
        EXPECTED: 
        """
        pass

    def test_006_check_values_in_cookies_section_which_are_set_in_banner_domainclick_cookie(self):
        """
        DESCRIPTION: Check values in Cookies Section which are set in  'banner_domainclick' cookie
        EXPECTED: Values of 'banner_domainclick' cookie should be replaced with new (taken from the new URL)
        """
        pass

    def test_007_log_out_and_proceed_with_registration_flow_again(self):
        """
        DESCRIPTION: Log Out and proceed with Registration flow again
        EXPECTED: User is succssefully registered.
        """
        pass

    def test_008_verify_values_set_in_ims_for_new_created_user___advertiser___profileid___crefere(self):
        """
        DESCRIPTION: Verify values set in IMS for new created user:
        DESCRIPTION: *   advertiser
        DESCRIPTION: *   profileid
        DESCRIPTION: *   crefere
        EXPECTED: Values should be set in IMS:
        EXPECTED: *   advertiser = [member_value];
        EXPECTED: *   profileid = [profile_value];
        EXPECTED: *   crefere = BTAG:[crefere_value].
        """
        pass
