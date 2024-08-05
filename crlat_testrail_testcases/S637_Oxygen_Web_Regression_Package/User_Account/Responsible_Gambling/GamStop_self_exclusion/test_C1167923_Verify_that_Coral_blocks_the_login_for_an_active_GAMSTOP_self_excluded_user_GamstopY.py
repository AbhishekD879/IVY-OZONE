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
class Test_C1167923_Verify_that_Coral_blocks_the_login_for_an_active_GAMSTOP_self_excluded_user_GamstopY(Common):
    """
    TR_ID: C1167923
    NAME: Verify that Coral blocks the login for an active GAMSTOP self excluded user (Gamstop=Y)
    DESCRIPTION: This test case verifies blocking Player Login on Coral, if Player has an Active self-exclusion period in Gamstop Database [i.e. Blocking login and Setting External self-exclusion for a Player in IMS-Coral].
    DESCRIPTION: The Gamstop IMS feature can be tested on TST2 / STG /Prod IMS pointing environments.
    PRECONDITIONS: -The scenario describes a user attempting to log in on Coral as an active GAMSTOP self excluded user. Choose 'Gamstop status=Y' column users from the herein attached spreadsheet.
    PRECONDITIONS: -Tst2/STG/Prod Gamstop test users data: see attached file
    PRECONDITIONS: -Tst2/STG/Prod IMS editing permissions credentials are needed to run this case.
    PRECONDITIONS: NOTE:
    PRECONDITIONS: This test case can be run via a workaround mocking the actual journey, as advised by Lavinia/Liam:
    PRECONDITIONS: - Register a standard EXTERNAL Coral user in Tst2/STG/HL/Prod ,to simulate an existing user. This user should not be internal! Do not use test@playtech.com as email , but a standard email domain for example user 123@yahoo.com).
    PRECONDITIONS: - Go to IMS and modify the account details (player info) in order to MATCH the Gamstop user data from the attached spreadsheet (Choose 'Gamstop status=Y' column users ).
    PRECONDITIONS: - After updating and saving the new details in IMS, log on Oxygen app with your modified Coral user: IMS makes a call to Gamstop with current data and gets a Gamstop='Y' response back.
    PRECONDITIONS: NOTE: **The user picked from xls. must not already exist in the coral IMS. Please check IMS : search by the email address of picked user, and modify to random data the info of any found account's info  previously existing user account's info (name, surname, DOB, email, postcode) to something else so that the Gamstop data set can be reused**
    PRECONDITIONS: The users test data spreadsheet has been provided by Gamstop for testing purposes in Tst2/STG/Prod pointing environments, and the info in columns (name, surname, dob, email, postcode) has to match exactly when updating the account details in IMS.
    PRECONDITIONS: Once details are modified, attempt to log in with your modified info username on Oxygen.
    PRECONDITIONS: In case more test users with 'GamStop' = 'Y' response are needed, please contact Lavinia Popovici/Liam Church.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_tap_log_in_button(self):
        """
        DESCRIPTION: Load Oxygen and tap Log in button.
        EXPECTED: Log In overlay is shown.
        """
        pass

    def test_002_log_in_with_credentials_of_user_modified_in_preconditions(self):
        """
        DESCRIPTION: Log in with credentials of user modified in preconditions.
        EXPECTED: * Error message is displayed
        EXPECTED: * Text of error message corresponds to value set to 'message' field from 'playerActionShowMessage' in login response (check OpenAPI websocket)
        """
        pass

    def test_003_in_ims_backoffice_search_for_username_from_preconditions_and_check_account_status(self):
        """
        DESCRIPTION: In IMS backoffice search for username from preconditions and check account status
        EXPECTED: Account status should be 'Frozen' (automatic freeze via ASE rules happens in IMS, based on the Gamstop=Y response received in Step 2).
        """
        pass
