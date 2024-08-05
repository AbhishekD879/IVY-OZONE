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
class Test_C62912898_Verify_displaying_of_message_in_betreceipt_when_user_login_between_N_to_N30_th_day(Common):
    """
    TR_ID: C62912898
    NAME: Verify displaying of message in betreceipt  when user login between N to N+30 th day
    DESCRIPTION: This test cases verifies message display  in bet receipt  when user login on N to N+30 th day
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

    def test_004_go_to_any_sport_add_multiple_selection_to_betslip_and_place_and_doubletripleacca_etc_and_tab_on_place_bet_button(self):
        """
        DESCRIPTION: Go to any sport Add multiple selection to betslip and place and double/triple/Acca etc and tab on place bet button
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_005_check_the_messaging_component_in_betreceipt(self):
        """
        DESCRIPTION: Check the messaging component in betreceipt
        EXPECTED: user will not see any Messaging component
        """
        pass
