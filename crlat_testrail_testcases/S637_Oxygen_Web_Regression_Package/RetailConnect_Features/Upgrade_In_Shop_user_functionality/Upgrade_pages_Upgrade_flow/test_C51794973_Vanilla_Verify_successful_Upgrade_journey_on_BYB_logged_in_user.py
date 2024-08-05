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
class Test_C51794973_Vanilla_Verify_successful_Upgrade_journey_on_BYB_logged_in_user(Common):
    """
    TR_ID: C51794973
    NAME: [Vanilla] Verify successful Upgrade journey on BYB (logged in user)
    DESCRIPTION: This test case verifies successful Upgrade journey when the logged in In-Shop user attempts to place a BYB
    PRECONDITIONS: - In-Shop user (card number and pin) are available
    PRECONDITIONS: - In-Shop user is logged in
    PRECONDITIONS: - BYB events are present (Bet Builder for Ladbrokes)
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

    def test_001_navigate_to_byb_bet_builder_event__add_selections_and_try_to_place_bet(self):
        """
        DESCRIPTION: Navigate to BYB (Bet Builder) event / add selections and try to place bet
        EXPECTED: Upgrade pop-up/journey is triggered
        """
        pass

    def test_002_click_on_upgrade_button(self):
        """
        DESCRIPTION: Click on 'Upgrade' button
        EXPECTED: User is redirected to Upgrade journey
        """
        pass

    def test_003_follow_upgrade_journey_fill_in_all_required_fields_and_complete_steps_and_click_create_account_buttonuse_email___usernameinternalgvccom_template(self):
        """
        DESCRIPTION: Follow Upgrade journey (fill in all required fields and complete steps) and click 'CREATE ACCOUNT' button
        DESCRIPTION: (use Email - *username*@internalgvc.com template)
        EXPECTED: User is logged out with the following message:
        EXPECTED: 'You have upgraded your account. Please use your Username and Password to log in with'.
        """
        pass

    def test_004_log_in_with_username_and_password_perform_funds_deposit_if_needed_and_place_byb_bet(self):
        """
        DESCRIPTION: Log in with Username and Password (perform funds deposit if needed) and place BYB bet
        EXPECTED: - User successfully logged in (Funds deposit done, if needed)
        EXPECTED: - BYB (Bet Builder) bet with added selections from step #1 is NOT saved, user should add new selections
        """
        pass

    def test_005_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_006_login_with_upgraded_user_and_navigate_to_byb_bet_builder_event__add_selections_and_try_to_place_bet(self):
        """
        DESCRIPTION: Login with upgraded user and navigate to BYB (Bet Builder) event / add selections and try to place bet
        EXPECTED: - Upgrade journey is NOT started
        EXPECTED: - User is able to BYB bet
        """
        pass
