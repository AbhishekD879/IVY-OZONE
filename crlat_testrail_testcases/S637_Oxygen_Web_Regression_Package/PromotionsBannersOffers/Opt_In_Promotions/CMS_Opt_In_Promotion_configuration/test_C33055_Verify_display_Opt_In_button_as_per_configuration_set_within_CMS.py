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
class Test_C33055_Verify_display_Opt_In_button_as_per_configuration_set_within_CMS(Common):
    """
    TR_ID: C33055
    NAME: Verify display Opt In button as per configuration set within CMS
    DESCRIPTION: This test case verifies Opt In button must only be displayed as per configurations set within CMS.
    DESCRIPTION: For e.g.: Promotion set for *VIP Levels 1-3 only these customers* will see Opt In button
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Add Opt In to Promotion within CMS, please, see C29336
    PRECONDITIONS: For configuration Opt In offers, please, use the following instruction:
    PRECONDITIONS: NOTE: For caching needs Akamai service is used on TST2/ STG environment, so after saving changes in CMS there clould be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_make_sure_promotion_with_opt_in_button_is_configured_within_cmspromotion_is_available_for_customers_with_vip_level1_2_3(self):
        """
        DESCRIPTION: Make sure Promotion with Opt In button is configured within CMS.
        DESCRIPTION: Promotion is available for customers with VIP Level:
        DESCRIPTION: 1, 2, 3
        EXPECTED: 
        """
        pass

    def test_002_load_oxygen_and_log_in_account_with_suitable_vip_level(self):
        """
        DESCRIPTION: Load Oxygen and log in account with suitable VIP Level
        EXPECTED: User is logged in
        """
        pass

    def test_003_find_a_configured_promotion(self):
        """
        DESCRIPTION: Find a configured Promotion
        EXPECTED: Promotion page is opened
        """
        pass

    def test_004_check_a_opt_in_button(self):
        """
        DESCRIPTION: Check a 'Opt In' button
        EXPECTED: Opt In button is present on front end for Users which have suitable VIP Level
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_006_log_in_next_account_with_unsuitable_vip_levelfor_eg_account_with_vip5(self):
        """
        DESCRIPTION: Log in next account with unsuitable VIP Level
        DESCRIPTION: For e.g.: account with VIP=5
        EXPECTED: User is logged in
        """
        pass

    def test_007_find_a_configured_promotion(self):
        """
        DESCRIPTION: Find a configured Promotion
        EXPECTED: Promotion is not displayed for Users which have unsuitable VIP Level.
        EXPECTED: Opt In button is not available for such customers.
        """
        pass
