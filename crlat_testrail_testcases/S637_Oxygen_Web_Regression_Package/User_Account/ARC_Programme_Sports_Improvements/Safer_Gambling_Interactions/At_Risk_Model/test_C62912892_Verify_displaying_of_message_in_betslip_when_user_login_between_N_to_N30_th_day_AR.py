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
class Test_C62912892_Verify_displaying_of_message_in_betslip_when_user_login_between_N_to_N30_th_day_AR(Common):
    """
    TR_ID: C62912892
    NAME: Verify displaying of message in betslip when user login between N to N+30 th day_AR
    DESCRIPTION: This test cases verifies message display when user login on N to N+30 th day
    PRECONDITIONS: User will not see any Messaging component
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_user_login_on_n_to_nplus30th_day(self):
        """
        DESCRIPTION: User login on N to N+30th day
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
