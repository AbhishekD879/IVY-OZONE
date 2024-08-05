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
class Test_C1167924_Verify_that_Coral_allows_login_for_a_user_with_expired_GAMSTOP_self_exclusion_GamstopP(Common):
    """
    TR_ID: C1167924
    NAME: Verify that Coral allows login for a user with expired GAMSTOP self exclusion (Gamstop=P)
    DESCRIPTION: This test case verifies that when GAMSTOP Self Exclusion has expired and has been lifted from a user's account, he can log back in on Coral.
    DESCRIPTION: The Gamstop IMS feature can be tested on TST2 / STG /Prod IMS pointing environments.
    PRECONDITIONS: -Since the Gamstop SE has to be on status expired, a user with 'P' (previous) Gamstop status is needed (see spreadsheet).
    PRECONDITIONS: -Tst2/STG/Prod Gamstop test users data: see attached file
    PRECONDITIONS: -Tst2/STG/Prod IMS editing permissions credentials are needed to run this case.
    PRECONDITIONS: The scenario comes down to verifying that a Coral user with 'P' (previous) Gamstop status, and active status in IMS can log in on Coral without issues.
    PRECONDITIONS: NOTE:
    PRECONDITIONS: This test case can be run via a workaround mocking the actual journey, as advised by Lavinia/Liam:
    PRECONDITIONS: - Register a standard EXTERNAL Coral user in Tst2/STG/HL/Prod , to simulate an existing user. This user should not be internal! Do not use test@playtech.com as email , but a standard email domain for example user 123@yahoo.com).
    PRECONDITIONS: - Go to IMS and modify this new account's details (player info section) in order to MATCH the Gamstop user data from the attached spreadsheet (Choose 'Gamstop status=P' column users ).
    PRECONDITIONS: - After updating and saving the new details in IMS, log on Oxygen app with your modified Coral user: IMS makes a call to Gamstop with current data and gets a Gamstop='P' response back, and allows the player to log in on Oxygen.
    PRECONDITIONS: NOTE: **The user picked from xls. must not already exist in the coral IMS. Please check IMS : search by the email address of picked user, and modify to random data the info of any found account's info (name, surname, DOB, email, postcode) to something else, so that the Gamstop data set can be reused**
    PRECONDITIONS: The users test data spreadsheet has been provided by Gamstop for testing purposes in Tst2/STG/Prod pointing environments, and the info in columns (name, surname, dob, email, postcode) has to match exactly when updating the account details in IMS.
    PRECONDITIONS: Once details are modified, attempt to log in with your modified info username on Oxygen.
    PRECONDITIONS: In case more test users with 'GamStop' = 'P' response are needed, please contact Lavinia Popovici/Liam Church.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_tap_log_in_button(self):
        """
        DESCRIPTION: Load Oxygen and tap Log in button
        EXPECTED: Log In overlay is shown.
        """
        pass

    def test_002_log_in_with_credentials_of_username_taken_from_preconditions(self):
        """
        DESCRIPTION: Log in with credentials of username taken from preconditions
        EXPECTED: Log in is successful and no error message is shown.
        """
        pass

    def test_003_in_ims_backoffice_search_for_username_from_preconditions(self):
        """
        DESCRIPTION: In IMS backoffice search for username from preconditions
        EXPECTED: Username is found and account details are displayed.
        """
        pass

    def test_004_on_the_user_account_in_ims_go_to_fraud_section_from_account_top_tabs_and_check_for_gamstop_status_marked_in_the_logs_at_previous_login(self):
        """
        DESCRIPTION: On the user account in IMS, go to 'Fraud' section from account top tabs and check for Gamstop status marked in the logs at previous login
        EXPECTED: GAMSTOP - P Response on Login (ON_LOGIN) should be marked as per previous login.
        """
        pass
