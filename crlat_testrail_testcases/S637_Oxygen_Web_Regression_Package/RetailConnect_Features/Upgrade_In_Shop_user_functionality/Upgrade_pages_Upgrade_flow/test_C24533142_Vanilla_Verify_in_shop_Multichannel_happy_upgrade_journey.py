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
class Test_C24533142_Vanilla_Verify_in_shop_Multichannel_happy_upgrade_journey(Common):
    """
    TR_ID: C24533142
    NAME: [Vanilla] Verify in-shop > Multichannel happy upgrade journey
    DESCRIPTION: The test case verifies in-shop to multichannel upgrade journey
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade (Coral only)
    PRECONDITIONS: * Load SportBook
    PRECONDITIONS: * Log in with In-Shop user
    PRECONDITIONS: * Open 'Connect' from header ribbon and click Upgrade your Connect account to bet online' - (Coral)
    PRECONDITIONS: or
    PRECONDITIONS: Trigger upgrade flow (e.g. Upgrade pop-up after login, or CTA after adding selection to Quickbet/Betslip) - (Ladbrokes OX 102+)
    PRECONDITIONS: - In-Shop user (card number and pin) are available
    PRECONDITIONS: - In-Shop user is logged in
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
    """
    keep_browser_open = True

    def test_001_trigger_upgrade_flow(self):
        """
        DESCRIPTION: Trigger Upgrade Flow
        EXPECTED: 'initaccountupgrade' page is open with 'UPGRADE NOW' pop-up that contains two buttons:
        EXPECTED: * NO THANKS
        EXPECTED: * UPGRADE
        """
        pass

    def test_002_tap_upgrade_now_upgrade(self):
        """
        DESCRIPTION: Tap 'UPGRADE NOW' ('UPGRADE')
        EXPECTED: '1' page of 'UPGRADE NOW' page is displayed that contains following elements:
        EXPECTED: - 'Country of Residence' and 'Currency' - pre-filled and not editable
        EXPECTED: - 'Email' - pre-filled and editable
        EXPECTED: - 'Username' - pre-filled and not editable
        EXPECTED: - 'Password' - empty and editable
        EXPECTED: - 'CONTINUE' button
        """
        pass

    def test_003_complete_email_and_password_and_tap_continue_button(self):
        """
        DESCRIPTION: Complete 'Email' and 'Password' and tap 'CONTINUE' button
        EXPECTED: '2' page of 'UPGRADE NOW' page is displayed that contains following elements:
        EXPECTED: - Title blocks: MR/Ms. - pre-selected and changeable
        EXPECTED: - First name - pre-filled and editable
        EXPECTED: - Last name - pre-filled and editable
        EXPECTED: - Date of birth - pre-filled and editable
        EXPECTED: - CONTINUE button
        """
        pass

    def test_004_complete_all_required_data_and_tap_continue_button(self):
        """
        DESCRIPTION: Complete all required data and tap 'CONTINUE' button
        EXPECTED: '3' page of 'UPGRADE NOW' page is displayed that contains following elements:
        EXPECTED: - House No, Street name - pre-filled and editable
        EXPECTED: - City - pre-filled and editable
        EXPECTED: - Postcode - pre-filled and editable
        EXPECTED: - Country cod - pre-filled and editable
        EXPECTED: - Mobile number - pre-filled and editable
        EXPECTED: - Email, SMS, Phone call, Post - check boxes
        EXPECTED: - 'CREATE ACCOUNT' button
        """
        pass

    def test_005_tab_create_account_button(self):
        """
        DESCRIPTION: Tab 'CREATE ACCOUNT' button
        EXPECTED: User is logged out with the following message:
        EXPECTED: 'You have upgraded your account. Please use your Username and Password to log in with'.
        """
        pass

    def test_006_log_in_with_username_and_password(self):
        """
        DESCRIPTION: Log in with Username and Password
        EXPECTED: - User is successfully logged in
        EXPECTED: - User business phase status is 'Multi-channel' (Can be checked in local storage > OX.User)
        """
        pass
