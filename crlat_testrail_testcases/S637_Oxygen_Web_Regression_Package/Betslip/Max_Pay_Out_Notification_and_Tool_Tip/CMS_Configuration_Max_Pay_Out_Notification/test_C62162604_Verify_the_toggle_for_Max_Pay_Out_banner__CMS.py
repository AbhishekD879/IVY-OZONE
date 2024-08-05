import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C62162604_Verify_the_toggle_for_Max_Pay_Out_banner__CMS(Common):
    """
    TR_ID: C62162604
    NAME: Verify the toggle for Max Pay Out banner - CMS
    DESCRIPTION: This test case verifies the Toggle ON/OFF feature for Max PAY Out Banner
    PRECONDITIONS: User should have CMS admin access
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as Admin user
        EXPECTED: Login should be successful
        """
        pass

    def test_002_navigate_to_system_config__structure_maxpayout(self):
        """
        DESCRIPTION: Navigate to System Config -Structure-Maxpayout
        EXPECTED: 
        """
        pass

    def test_003_disable_the_max_pay_out_and_click_on_save_changes(self):
        """
        DESCRIPTION: Disable the Max Pay Out and click on Save changes
        EXPECTED: User should be able to save the changes
        """
        pass

    def test_004_in_fe___ladbrokes__coral___add_selections_to_betslip_quick_betmobile_only_trigger_the_max_pay_out_bannervalidate_the_display_of_max_pay_out_banner(self):
        """
        DESCRIPTION: In FE - Ladbrokes , Coral - Add selections to Betslip, Quick Bet(Mobile Only), Trigger the Max Pay Out banner
        DESCRIPTION: Validate the display of Max Pay Out Banner
        EXPECTED: * User should not be able to view the banner
        """
        pass

    def test_005_enable_the_max_pay_out_and_click_on_save_changes(self):
        """
        DESCRIPTION: Enable the Max Pay Out and click on Save changes
        EXPECTED: User should be able to save the changes
        """
        pass

    def test_006_in_fe___ladbrokes__coral___add_selections_to_betslip_quick_betmobile_only_trigger_the_max_pay_out_bannervalidate_the_display_of_max_pay_out_banner(self):
        """
        DESCRIPTION: In FE - Ladbrokes , Coral - Add selections to Betslip, Quick Bet(Mobile Only), Trigger the Max Pay Out banner
        DESCRIPTION: Validate the display of Max Pay Out Banner
        EXPECTED: * User should be able to view the banner
        """
        pass
