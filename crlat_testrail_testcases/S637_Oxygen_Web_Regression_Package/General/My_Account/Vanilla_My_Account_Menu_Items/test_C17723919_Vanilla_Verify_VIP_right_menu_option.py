import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17723919_Vanilla_Verify_VIP_right_menu_option(Common):
    """
    TR_ID: C17723919
    NAME: [Vanilla] Verify VIP right menu option
    DESCRIPTION: This test case is to verify all option menus under VIP right menu option
    PRECONDITIONS: User has a **VIP** account
    PRECONDITIONS: Non-VIP players = VIP Level 1 - 10
    PRECONDITIONS: Bronze players = VIP Level 11
    PRECONDITIONS: Silver players = VIP Level 12
    PRECONDITIONS: Gold players = VIP Level 13
    PRECONDITIONS: Platinum players = VIP Level 14
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env_as_vip_user_11_14(self):
        """
        DESCRIPTION: Log in to test env as VIP user (11-14)
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_vip_menu_option(self):
        """
        DESCRIPTION: Click/tap VIP menu option
        EXPECTED: VIP menu is displayed with the following options:
        EXPECTED: - My VIP
        EXPECTED: - VIP Benefits
        EXPECTED: - Contact us
        """
        pass

    def test_004_clicktap_my_vip_option(self):
        """
        DESCRIPTION: Click/tap My VIP option
        EXPECTED: My VIP page is displayed with the user statistics information
        """
        pass

    def test_005_reopen_right_menu__vip_and_clicktap_vip_benefits_option(self):
        """
        DESCRIPTION: Reopen right menu-> VIP and click/tap VIP Benefits option
        EXPECTED: User is taken to VIP Benefits page
        """
        pass

    def test_006_reopen_right_menu__vip_and_clicktap_contact_us_option(self):
        """
        DESCRIPTION: Reopen right menu-> VIP and click/tap Contact us option
        EXPECTED: User is taken to Contact Us page
        """
        pass
