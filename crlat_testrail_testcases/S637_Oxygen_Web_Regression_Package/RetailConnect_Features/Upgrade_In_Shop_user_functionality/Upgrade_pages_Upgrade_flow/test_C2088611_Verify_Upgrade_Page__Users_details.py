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
class Test_C2088611_Verify_Upgrade_Page__Users_details(Common):
    """
    TR_ID: C2088611
    NAME: Verify Upgrade Page - Users details
    DESCRIPTION: This test case verify Upgrade Landing Page
    DESCRIPTION: JIRA ticked:
    DESCRIPTION: HMN-2417 Upgrade Landing Page
    DESCRIPTION: HMN-2651 Web: Amend UI for Upgrade Journey
    DESCRIPTION: HMN-3777 Web: Changes for Upgrade Pages
    PRECONDITIONS: !Please note that for Coral we have 'CONNECT' and for Ladbrokes - 'THE GRID'
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: The way to open upgrade dialog:
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in as an in-shop user
    PRECONDITIONS: OR
    PRECONDITIONS: Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: Open MY ACCOUNT menu
    PRECONDITIONS: Select CONNECT(Coral) / The Grid (Ladbrokes)
    PRECONDITIONS: Select UPGRADE
    PRECONDITIONS: OR
    PRECONDITIONS: Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: a) Select DEPOSIT from header
    PRECONDITIONS: b) Open MY ACCOUNT and select DEPOSIT
    PRECONDITIONS: c) Open MY ACCOUNT, select CASHIER and DEPOSIT
    PRECONDITIONS: d) Open MY ACCOUNT, select CASHIER and WITHDRAW
    PRECONDITIONS: e) Open CONNECT from header and tap "Upgrade your Connect account to bet online" (Coral)
    """
    keep_browser_open = True

    def test_001_click_the_upgrade_button(self):
        """
        DESCRIPTION: Click the **UPGRADE** button
        EXPECTED: * A user is redirected to the 'registration' screen with title **UPGRADE NOW**
        EXPECTED: and 3 steps of registration
        """
        pass

    def test_002_provide_all_necessary_data_on_all_3_steps_password_etc___remember_the_user_name(self):
        """
        DESCRIPTION: Provide all necessary data on all 3 steps (password etc. - REMEMBER THE USER NAME!)
        EXPECTED: * All possible fields are prepopulated with data from the system
        """
        pass

    def test_003_verify_validations_rules_after_tapping_create_account_button(self):
        """
        DESCRIPTION: Verify validations rules after tapping 'Create Account' button
        EXPECTED: * If required fields are not filled or filled incorrectly corresponding error messages are displayed under each field
        EXPECTED: * If there are no errors user is logged out from the app and redirected to the login page with an information about successful upgrade and need for re-login
        """
        pass

    def test_004_log_in_with_connect_card_number_and_pin(self):
        """
        DESCRIPTION: Log in with connect card number and pin
        EXPECTED: User is not able to log in, error message is displayed
        """
        pass

    def test_005_log_in_with_username_and_password_configured_during_upgrade(self):
        """
        DESCRIPTION: Log in with username and password configured during upgrade
        EXPECTED: User is successfully logged in, account is upgraded
        """
        pass
