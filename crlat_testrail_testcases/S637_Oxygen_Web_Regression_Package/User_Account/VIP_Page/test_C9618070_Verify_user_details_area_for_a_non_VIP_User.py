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
class Test_C9618070_Verify_user_details_area_for_a_non_VIP_User(Common):
    """
    TR_ID: C9618070
    NAME: Verify user details area for a non VIP User
    DESCRIPTION: This test case verifies non VIP user details area on 'My Account' menu
    DESCRIPTION: - To change user's VIP level in IMS: Account Information > Casino VIP level > Click 'Update Info'
    DESCRIPTION: - Non-VIP players = IMS VIP Level 1 - 10coral2
    DESCRIPTION: - Link to IMS and creds: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. Non VIP user is logged in
    """
    keep_browser_open = True

    def test_001_tap_on_user_balance(self):
        """
        DESCRIPTION: Tap on user 'Balance'
        EXPECTED: 'My Account' menu is slid up
        """
        pass

    def test_002_verify_user_details_area_for_a_non_vip_user(self):
        """
        DESCRIPTION: Verify user details area for a non VIP user
        EXPECTED: - Black avatar icon is displayed
        EXPECTED: - Welcome message: "Hi, [Name of a user]"
        EXPECTED: - 'Deposit' button
        EXPECTED: - Balance: "<currency symbol> XX.XX"
        EXPECTED: - "HIDE BALANCE" link
        """
        pass
