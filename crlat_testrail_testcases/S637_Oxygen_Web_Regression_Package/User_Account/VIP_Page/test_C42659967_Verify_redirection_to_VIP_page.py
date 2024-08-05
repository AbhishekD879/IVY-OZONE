import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C42659967_Verify_redirection_to_VIP_page(Common):
    """
    TR_ID: C42659967
    NAME: Verify redirection to VIP page
    DESCRIPTION: This test case verifies valid redirection for VIP users when clicking on "Silver-up" button
    PRECONDITIONS: - User has a VIP level
    PRECONDITIONS: - User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account(self):
        """
        DESCRIPTION: Navigate to My Account
        EXPECTED: My Account page is opened
        """
        pass

    def test_002_click_on_silver_up_vip_button(self):
        """
        DESCRIPTION: Click on "Silver-up" (VIP) button
        EXPECTED: User is redirected to https://<env>/en/vip/new-benefits
        EXPECTED: (e.g https://casino.ladbrokes.com/en/vip/new-benefits PROD)
        """
        pass
