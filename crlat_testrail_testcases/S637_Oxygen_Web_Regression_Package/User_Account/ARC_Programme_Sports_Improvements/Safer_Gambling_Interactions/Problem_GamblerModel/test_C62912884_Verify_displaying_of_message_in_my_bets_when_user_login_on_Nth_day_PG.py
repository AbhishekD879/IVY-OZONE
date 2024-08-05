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
class Test_C62912884_Verify_displaying_of_message_in_my_bets_when_user_login_on_Nth_day_PG(Common):
    """
    TR_ID: C62912884
    NAME: Verify displaying of message in my bets when user login on Nth day_PG
    DESCRIPTION: This test case verifies messaging component in  my bets with frequency as permanent
    PRECONDITIONS: .User Risk level and
    PRECONDITIONS: Frequency should be set in CMS
    PRECONDITIONS: .Message component should be as per CMS
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_user_login_to_application_with_frequency_set_as_permanent(self):
        """
        DESCRIPTION: User login to application with frequency set as permanent
        EXPECTED: Login should be successful
        """
        pass

    def test_003_go_to_any_sport_and_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any sport and add single selection to betslip
        EXPECTED: Selection is displayed and  added to betslip
        """
        pass

    def test_004_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button
        EXPECTED: .Bet is placed successfully
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_005_navigate_to_my_bets_open_bets_check_the_messaging_in__bet_receipt(self):
        """
        DESCRIPTION: Navigate to my bets-open bets check the Messaging in  bet receipt
        EXPECTED: User view a messaging component after bet placement as per CMS config
        """
        pass

    def test_006_user_click_on_minimize_for_message_component(self):
        """
        DESCRIPTION: User click on Minimize for message component
        EXPECTED: Message component is minimized,Application save the interaction successfully and should display next login
        """
        pass
