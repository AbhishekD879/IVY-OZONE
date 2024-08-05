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
class Test_C2604120_Upgrade_of_In_Shop_user(Common):
    """
    TR_ID: C2604120
    NAME: Upgrade of In-Shop user
    DESCRIPTION: This test case verifies upgrade process for an in-shop user
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=756674&group_order=asc
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: **The ways to open Connect Feature list: (Coral Only)**
    PRECONDITIONS: * Homepage -> header ribbon -> CONNECT
    PRECONDITIONS: * Homepage -> header ribbon -> ALL SPORTS -> CONNECT section
    PRECONDITIONS: * Right Hand Menu -> CONNECT section
    PRECONDITIONS: Contact GVC (Venugopal Rao Joshi / Abhinav Goel) and/or Souparna Datta + Oksana Tkach in order to generate In-Shop users
    """
    keep_browser_open = True

    def test_001_log_in_as_an_in_shop_user(self):
        """
        DESCRIPTION: Log in as an in-shop user
        EXPECTED: A user is logged successfully
        """
        pass

    def test_002___trigger_upgrade_flow_by_adding_sections_to_betslip_and_clicking_upgrade_button__on_upgrade_popup_confirm_upgrade(self):
        """
        DESCRIPTION: - Trigger upgrade flow by adding section(s) to Betslip and clicking Upgrade button
        DESCRIPTION: - On upgrade popup confirm Upgrade
        EXPECTED: User is redirected to Upgrade flow 1st page
        EXPECTED: !IMPORTANT: remember username + password
        """
        pass

    def test_003_fill_all_required_fields_correctly_on_all_3_steps_and_tap_the_confirm_button(self):
        """
        DESCRIPTION: Fill all required fields correctly on all 3 steps and tap the Confirm button
        EXPECTED: - Successful message dialog is shown
        EXPECTED: - User is logged out
        """
        pass

    def test_004_log_in_to_the_application_with_new_username(self):
        """
        DESCRIPTION: Log in to the application with new username
        EXPECTED: - User is logged in
        EXPECTED: - In App Local Storage > OX.User > accountBusinessPhase: "multi-channel"
        """
        pass

    def test_005_add_payment_method_and_make_deposit(self):
        """
        DESCRIPTION: Add payment method and make deposit
        EXPECTED: Users balance is updated
        """
        pass

    def test_006_navigate_back_to_app_and_verify_betslip_content(self):
        """
        DESCRIPTION: Navigate back to app and verify Betslip content
        EXPECTED: - Betslip contains previously added selections
        EXPECTED: - 'PLACE BET' button is displayed
        """
        pass

    def test_007_enter_stake_and_place_bet(self):
        """
        DESCRIPTION: Enter stake and place bet
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt is displayed
        """
        pass
