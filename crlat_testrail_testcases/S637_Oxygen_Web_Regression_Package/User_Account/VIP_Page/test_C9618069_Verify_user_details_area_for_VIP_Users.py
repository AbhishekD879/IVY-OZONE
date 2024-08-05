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
class Test_C9618069_Verify_user_details_area_for_VIP_Users(Common):
    """
    TR_ID: C9618069
    NAME: Verify user details area for VIP Users
    DESCRIPTION: This test case verifies VIP user details area on 'My Account' menu
    DESCRIPTION: - To change user's VIP level in IMS: Account Information > Casino VIP level > Click 'Update Info'
    DESCRIPTION: **VIP IMS Level Configuration**
    DESCRIPTION: - **Non-VIP players** = IMS VIP Level 1 - 10
    DESCRIPTION: - **Bronze players** = IMS VIP Level 11
    DESCRIPTION: - **Silver players** = IMS VIP Level 12
    DESCRIPTION: - **Gold players** = IMS VIP Level 13
    DESCRIPTION: - **Platinum players** = IMS VIP Level 14
    DESCRIPTION: - Link to IMS and creds: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. Bronze VIP level user is logged in
    """
    keep_browser_open = True

    def test_001_tap_on_user_balance(self):
        """
        DESCRIPTION: Tap on user 'Balance'
        EXPECTED: 'My Account' menu is slid up
        """
        pass

    def test_002_verify_user_details_area_for_a_bronze_vip_level_user(self):
        """
        DESCRIPTION: Verify user details area for a Bronze VIP level user
        EXPECTED: - Brown avatar icon is displayed
        EXPECTED: - Welcome message: "Hi, [Name of a user]"
        EXPECTED: - 'Bronze VIP' brown badge is displayed
        EXPECTED: - 'Deposit' button
        EXPECTED: - Balance: "<currency symbol> XX.XX"
        EXPECTED: - "HIDE BALANCE" link
        """
        pass

    def test_003_tap_on_bronze_vip_badge(self):
        """
        DESCRIPTION: Tap on 'Bronze VIP' badge
        EXPECTED: User is redirected to to: https://gaming.ladbrokes.com/vip
        """
        pass

    def test_004_log_in_with_silver_vip_level_user(self):
        """
        DESCRIPTION: Log in with Silver VIP level user
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_2___3(self):
        """
        DESCRIPTION: Repeat steps 2 - 3
        EXPECTED: - Grey avatar icon is displayed
        EXPECTED: - Welcome message: "Hi, [Name of a user]"
        EXPECTED: - 'Silver VIP' grey badge is displayed
        EXPECTED: - 'Deposit' button
        EXPECTED: - Balance: "<currency symbol> XX.XX"
        EXPECTED: - "HIDE BALANCE" link
        """
        pass

    def test_006_tap_on_silver_vip_badge(self):
        """
        DESCRIPTION: Tap on 'Silver VIP' badge
        EXPECTED: User is redirected to to: https://gaming.ladbrokes.com/vip
        """
        pass

    def test_007_log_in_with_gold_vip_level_user(self):
        """
        DESCRIPTION: Log in with Gold VIP level user
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2___3(self):
        """
        DESCRIPTION: Repeat steps 2 - 3
        EXPECTED: - Yellow avatar icon is displayed
        EXPECTED: - Welcome message: "Hi, [Name of a user]"
        EXPECTED: - 'Gold VIP' yellow badge is displayed
        EXPECTED: - 'Deposit' button
        EXPECTED: - Balance: "<currency symbol> XX.XX"
        EXPECTED: - "HIDE BALANCE" link
        """
        pass

    def test_009_tap_on_gold_vip_badge(self):
        """
        DESCRIPTION: Tap on 'Gold VIP' badge
        EXPECTED: User is redirected to to: https://gaming.ladbrokes.com/vip
        """
        pass

    def test_010_log_in_with_platinum_vip_level_user(self):
        """
        DESCRIPTION: Log in with Platinum VIP level user
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2___3(self):
        """
        DESCRIPTION: Repeat steps 2 - 3
        EXPECTED: - Grey avatar icon is displayed
        EXPECTED: - Welcome message: "Hi, [Name of a user]"
        EXPECTED: - 'Platinum VIP' yellow badge is displayed
        EXPECTED: - 'Deposit' button
        EXPECTED: - Balance: "<currency symbol> XX.XX"
        EXPECTED: - "HIDE BALANCE" link
        """
        pass

    def test_012_tap_on_platinum_vip_badge(self):
        """
        DESCRIPTION: Tap on 'Platinum VIP' badge
        EXPECTED: User is redirected to to: https://gaming.ladbrokes.com/vip
        """
        pass
