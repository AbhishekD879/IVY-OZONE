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
class Test_C1167922_Verify_that_Coral_blocks_the_registration_for_an_active_GAMSTOP_self_excluded_user_GamstopY(Common):
    """
    TR_ID: C1167922
    NAME: Verify that Coral blocks the registration for an active GAMSTOP self excluded user (Gamstop=Y)
    DESCRIPTION: This test case verifies canceling Player Registration on Coral if Player has an Active Self-exclusion period in Gamstop Database.
    DESCRIPTION: The Gamstop IMS feature can be tested on TST2 / STG /Prod IMS pointing environments.
    PRECONDITIONS: - The scenario describes a user that attempts to register on Coral although he is an active GAMSTOP self excluded user.
    PRECONDITIONS: - Test Data: TST2/STG/HL/Prod Gamstop test users data: see attached file . Choose 'Gamstop status=Y' column users from the herein attached spreadsheet.
    PRECONDITIONS: NOTE: **The user picked from xls. must not already exist in the coral IMS. Please check IMS : search by the email address of picked user, and modify to random data any found account's info (name, surname, DOB, email, postcode)  so that the Gamstop data set can be reused**
    PRECONDITIONS: NOTE: this GamStop excluded external users test data xls.  has been provided by Gamstop for testing purposes in Tst2/STG/Prod pointing environments only, and the test data in columns (name, surname, dob, email, postcode) has to match exactly when registering on coral registration form.
    PRECONDITIONS: Other fields such as street name, city etc can be of any accepted value on the registration form.
    PRECONDITIONS: -TST2/STG/Prod IMS edit credentials are needed to run this case.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_tap_join_now_to_register(self):
        """
        DESCRIPTION: Load Oxygen and tap Join Now to register
        EXPECTED: The registration form opens on Step 1
        """
        pass

    def test_002_input_fields_with_test_user_data_from_preconditions(self):
        """
        DESCRIPTION: Input fields with test user data from Preconditions
        EXPECTED: --
        """
        pass

    def test_003_on_last_step_of_registration_tap_confirm_registration(self):
        """
        DESCRIPTION: On last step of registration tap 'Confirm Registration'
        EXPECTED: * Error message is displayed
        EXPECTED: * Text of error message corresponds to value set to 'message' field from 'showMessageNotificationInfo' in response with id: 33006 (check OpenAPI websocket)
        """
        pass

    def test_004_in_ims_backoffice_search_for_newly_created_username_to_make_sure_registration_did_not_finalize(self):
        """
        DESCRIPTION: In IMS backoffice search for newly created username to make sure registration did not finalize.
        EXPECTED: The username does not exist.
        """
        pass
