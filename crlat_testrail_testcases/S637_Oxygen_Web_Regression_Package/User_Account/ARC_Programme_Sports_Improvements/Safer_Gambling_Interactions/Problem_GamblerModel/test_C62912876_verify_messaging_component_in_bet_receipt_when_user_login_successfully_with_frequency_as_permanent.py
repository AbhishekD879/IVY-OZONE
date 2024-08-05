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
class Test_C62912876_verify_messaging_component_in_bet_receipt_when_user_login_successfully_with_frequency_as_permanent(Common):
    """
    TR_ID: C62912876
    NAME: verify messaging component in bet receipt when user login successfully with frequency as permanent
    DESCRIPTION: This test case verifies messaging component in  bet receipt with frequency as permanent
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
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_005_check_the_messaging_in__bet_receipt(self):
        """
        DESCRIPTION: Check the Messaging in  bet receipt
        EXPECTED: User view a messaging component after bet placement as per CMS config
        """
        pass

    def test_006_user_click_on_minimize_for_message_component(self):
        """
        DESCRIPTION: User click on Minimize for message component
        EXPECTED: Message component is minimized,Application save the interaction successfully and should display next login
        """
        pass
