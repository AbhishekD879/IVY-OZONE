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
class Test_C62912871_Verify_displaying_of_message_in_bet_receipt_when_user_login_between_N_to_N15th_day_PG(Common):
    """
    TR_ID: C62912871
    NAME: Verify displaying of message in bet receipt when user login between N to N+15th day_PG
    DESCRIPTION: This test cases verifies message display  in bet receipt  when user login on N to N+15 th day
    PRECONDITIONS: User will not see any Messaging component
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_user_login_on_n_to_nplus15th_day(self):
        """
        DESCRIPTION: User login on N to N+15th day
        EXPECTED: Login should be successful
        """
        pass

    def test_003_application_retrieve_the_saved_user_interactions(self):
        """
        DESCRIPTION: Application retrieve the saved user interactions
        EXPECTED: User interactions should be received
        """
        pass

    def test_004_check_the_messaging_component_in_betslip(self):
        """
        DESCRIPTION: Check the messaging component in betslip
        EXPECTED: user will not see any Messaging component
        """
        pass
