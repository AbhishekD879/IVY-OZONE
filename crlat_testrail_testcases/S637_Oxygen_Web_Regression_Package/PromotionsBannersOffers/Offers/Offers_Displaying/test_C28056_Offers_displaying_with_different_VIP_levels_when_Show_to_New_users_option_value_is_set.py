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
class Test_C28056_Offers_displaying_with_different_VIP_levels_when_Show_to_New_users_option_value_is_set(Common):
    """
    TR_ID: C28056
    NAME: Offers displaying with different VIP levels when 'Show to New users' option value is set
    DESCRIPTION: This test case verifies Offers displaying for users with different VIP levels when 'Show to New users' option value is set
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
    PRECONDITIONS: 3) 'Show to New Users' option value is set for Offers
    """
    keep_browser_open = True

    def test_001_clear_all_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear all cookies and load Oxygen application
        EXPECTED: *   'viplevel' cookie is NOT present in browser
        EXPECTED: *   'Existing user:True' cookie is NOT present to browser
        """
        pass

    def test_002_select_offer_with_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select offer with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_003_select_offer_with_include_vip_levels__x_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels'  = 'X' and verify Offer displaying
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_004_log_in_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Log in to application with user for which 'viplevel' = 'X'
        EXPECTED: 
        """
        pass

    def test_005_select_offer_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Offer with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_006_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_007_select_offer_with_include_vip_levels_ltgt_x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' &lt;&gt; 'X' and verify its displaying in application
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_008_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass
