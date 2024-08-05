import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2604117_Coral_Only_In_Shop_users_features(Common):
    """
    TR_ID: C2604117
    NAME: [Coral Only] In-Shop users features
    DESCRIPTION: Test case verifies features that are available for in-shop user only, and disabling features that should not be available
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: * 'Upgrade your account' text is CMS configurable via Static block 'Connect Upgrade Dialog'
    PRECONDITIONS: * Connect features list is CMS configurable via Menu -> Connect Menu
    PRECONDITIONS: * Make sure connect features are turned on in CMS (System configuration -> Connect)
    PRECONDITIONS: 1. Clean LocalStorage and Cookies
    PRECONDITIONS: 2. Load Sportbook App
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_log_in_with_in_shop_user_using_connect_card_number_and_pin(self):
        """
        DESCRIPTION: Log in with In-Shop user using Connect Card number and PIN
        EXPECTED: * User is logged in successfully
        EXPECTED: * 'Upgrade your account' dialog is shown
        EXPECTED: * User can close it by tapping 'X' button or by 'No Thanks' link
        """
        pass

    def test_002_verify_upgrade_button(self):
        """
        DESCRIPTION: Verify 'Upgrade' button
        EXPECTED: * Button redirects to Upgrade page
        """
        pass

    def test_003_verify_connect_section_in_a_z_menu(self):
        """
        DESCRIPTION: Verify 'Connect' section in A-Z menu
        EXPECTED: * Connect section is placed at the bottom
        EXPECTED: * Connect section items correspond to CMS configuration
        """
        pass

    def test_004_verify_connect_section_in_rhm(self):
        """
        DESCRIPTION: Verify 'Connect' section in RHM
        EXPECTED: * Connect section items correspond to CMS configuration
        """
        pass

    def test_005_verify_features_designed_for_online_betting_are_not_available_fro_in_shop_user_open_rhm_tap_following_menu_items_one_by_one_deposit_withdraw_cancel_withdraw_my_accountfor_desktop_tap_my_account__tap_following_menu_items_one_by_one_my_freebets_and_bonuses_deposit_withdraw_cancel_withdraw_add_new_payment_type_voucher_code_transaction_history_gaming_history_limits_change_passwordresponsible_gambling(self):
        """
        DESCRIPTION: Verify features designed for online betting are not available fro in-shop user:
        DESCRIPTION: * Open RHM
        DESCRIPTION: * Tap following menu items (one by one): DEPOSIT, WITHDRAW, CANCEL WITHDRAW, MY ACCOUNT
        DESCRIPTION: For Desktop:
        DESCRIPTION: * Tap MY ACCOUNT
        DESCRIPTION: * * Tap following menu items (one by one): My FreeBets and bonuses; Deposit; Withdraw; Cancel Withdraw; Add new payment type; voucher code; transaction history; Gaming history; Limits; change password;Responsible Gambling
        EXPECTED: * After tapping each item 'Upgrade your account' dialog is shown
        EXPECTED: * User can close it or navigate to Upgrade page by tapping 'Upgrade' button
        """
        pass

    def test_006_open_my_bets___tap_deposit_link_at_the_top_right_corner(self):
        """
        DESCRIPTION: Open My Bets -> tap 'Deposit' link at the top right corner
        EXPECTED: * 'Upgrade your account' dialog is shown
        EXPECTED: * User can close it or navigate to Upgrade page by tapping 'Upgrade' button
        """
        pass

    def test_007__add_selection_to_betslip_open_betslip_tap_deposit_link_at_the_top_right_corner(self):
        """
        DESCRIPTION: * Add selection to Betslip
        DESCRIPTION: * Open Betslip
        DESCRIPTION: * Tap 'Deposit' link at the top right corner
        EXPECTED: * (There is no QuickBet functionality for In-Shop user)
        EXPECTED: * 'Upgrade your account' dialog is shown
        EXPECTED: * User can close it or navigate to Upgrade page by tapping 'Upgrade' button
        """
        pass

    def test_008_get_back_to_betslip(self):
        """
        DESCRIPTION: Get back to Betslip
        EXPECTED: * 'Upgrade your account & bet now' button is at the bottom
        EXPECTED: * Button is active
        EXPECTED: * It redirects user to Upgrade page
        """
        pass

    def test_009_verify_use_connect_online_feature_is_available_for_in_shop_user_only(self):
        """
        DESCRIPTION: Verify 'Use Connect online' feature is available for In-Shop user only
        EXPECTED: * When In-Shop user is logged in there is 'Use Connect online' item in:
        EXPECTED: * A-Z menu -> Connect
        EXPECTED: * RHM -> Connect
        EXPECTED: * Connect landing page
        """
        pass

    def test_010__log_out_log_in_with_online_user(self):
        """
        DESCRIPTION: * Log out
        DESCRIPTION: * Log in with online user
        EXPECTED: 'Use Connect online' item is absent in:
        EXPECTED: * A-Z menu -> Connect
        EXPECTED: * RHM -> Connect
        EXPECTED: * Connect landing page
        """
        pass
