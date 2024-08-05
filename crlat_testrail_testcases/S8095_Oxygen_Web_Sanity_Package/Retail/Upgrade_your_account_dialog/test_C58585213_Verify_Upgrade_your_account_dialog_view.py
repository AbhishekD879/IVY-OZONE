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
class Test_C58585213_Verify_Upgrade_your_account_dialog_view(Common):
    """
    TR_ID: C58585213
    NAME: Verify 'Upgrade your account' dialog view
    DESCRIPTION: This test case verifies upgrade dialog (upgrade, no thanks, close) view
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade (Coral only)
    PRECONDITIONS: - In-Shop user (card number and pin) are available
    PRECONDITIONS: ---
    PRECONDITIONS: User type ('In-shop', 'Online', 'Multi-channel') received in https://{env}/en/api/clientconfig/partial?configNames=vnUser&configNames=vnClaims in
    PRECONDITIONS: "http://api.bwin.com/v3/user/accBusinessPhase:" attribute after login and stored in local storage > OX.USER > accountBusinessPhase attribute
    PRECONDITIONS: ![](index.php?/attachments/get/74407650) ![](index.php?/attachments/get/74407651)
    PRECONDITIONS: ---
    PRECONDITIONS: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    PRECONDITIONS: 'Online' - user with username and password.
    PRECONDITIONS: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: ---
    PRECONDITIONS: Contact Venugopal Rao Joshi in order to generate In-Shop users for Ladbrokes brand (currently no known flows to generate In-Shop users for Coral)
    PRECONDITIONS: ---
    PRECONDITIONS: Redirection path: mobileportal/initaccountupgrade?source=guard
    """
    keep_browser_open = True

    def test_001___log_in_as_an_in_shop_user__verify_upgrade_dialog_structure(self):
        """
        DESCRIPTION: - Log in as an in-shop user
        DESCRIPTION: - Verify upgrade dialog structure
        EXPECTED: - User is redirected to Upgrade dialog
        EXPECTED: * Header with text: **UPGRADE NOW**
        EXPECTED: * 'X' button
        EXPECTED: * Upgrade Text, e.g. ***Get £30 in free bets when you upgrade and stake £5 or more online today. You'll receive £20 online and £10 in your local Coral shop.*
        EXPECTED: * **NO THANKS** button
        EXPECTED: * **UPGRADE** button
        """
        pass

    def test_002_login_as_an_in_shop_user_select_no_thanks_on_the_dialog_after_login__select_deposit_from_header_desktop_only__my_account__deposit__my_account__banking__deposit__my_account__banking__withdraw__my_account__banking__my_balance__upgrade(self):
        """
        DESCRIPTION: Login as an in-shop user select NO THANKS on the dialog after login
        DESCRIPTION: - Select DEPOSIT from header (Desktop only)
        DESCRIPTION: - MY ACCOUNT > DEPOSIT
        DESCRIPTION: - MY ACCOUNT > BANKING > DEPOSIT
        DESCRIPTION: - MY ACCOUNT > BANKING > WITHDRAW
        DESCRIPTION: - MY ACCOUNT > BANKING > MY BALANCE > UPGRADE
        EXPECTED: - User is redirected to Upgrade dialog
        EXPECTED: * Header with text: **UPGRADE NOW**
        EXPECTED: * 'X' button
        EXPECTED: * Upgrade Text, e.g. ***Get £30 in free bets when you upgrade and stake £5 or more online today. You'll receive £20 online and £10 in your local Coral shop.*
        EXPECTED: * **NO THANKS** button
        EXPECTED: * **UPGRADE** button
        """
        pass

    def test_003_login_as_an_in_shop_user_select_no_thanks_on_the_dialog_after_login__add_any_selections_to_betslip_and_click_on_upgrade__place_bet__try_to_place_lotto_bet__try_to_place_horse_racing_tote_bet(self):
        """
        DESCRIPTION: Login as an in-shop user select NO THANKS on the dialog after login
        DESCRIPTION: - Add any selection(s) to Betslip and click on 'Upgrade & Place bet'
        DESCRIPTION: - Try to place Lotto bet
        DESCRIPTION: - Try to place Horse Racing Tote bet
        EXPECTED: - User is redirected to Upgrade dialog
        EXPECTED: * Header with text: **UPGRADE NOW**
        EXPECTED: * 'X' button
        EXPECTED: * Upgrade Text, e.g. ***Get £30 in free bets when you upgrade and stake £5 or more online today. You'll receive £20 online and £10 in your local Coral shop.*
        EXPECTED: * **NO THANKS** button
        EXPECTED: * **UPGRADE** button
        """
        pass

    def test_004_corallogin_as_an_in_shop_user_select_no_thanks_on_the_dialog_after_login__my_account__connect__upgrade(self):
        """
        DESCRIPTION: (Coral)
        DESCRIPTION: Login as an in-shop user select NO THANKS on the dialog after login > MY ACCOUNT > CONNECT > UPGRADE
        EXPECTED: - User is redirected to Upgrade dialog
        EXPECTED: * Header with text: **UPGRADE NOW**
        EXPECTED: * 'X' button
        EXPECTED: * Upgrade Text, e.g. ***Get £30 in free bets when you upgrade and stake £5 or more online today. You'll receive £20 online and £10 in your local Coral shop.*
        EXPECTED: * **NO THANKS** button
        EXPECTED: * **UPGRADE** button
        """
        pass
