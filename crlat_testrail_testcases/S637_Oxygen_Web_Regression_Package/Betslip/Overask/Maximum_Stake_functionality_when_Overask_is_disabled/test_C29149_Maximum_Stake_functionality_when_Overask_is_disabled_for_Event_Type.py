import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29149_Maximum_Stake_functionality_when_Overask_is_disabled_for_Event_Type(Common):
    """
    TR_ID: C29149
    NAME: Maximum Stake functionality when Overask is disabled for Event Type
    DESCRIPTION: This test case verifies Maximum Stake functionality when Overask is disabled for Event type
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-9296 Overask - Display Max Bet message if Overask is disabled for the Customer
    DESCRIPTION: BMA-21529 New betslip - Max bet alert
    PRECONDITIONS: To enable/disable Overask for type event please follow this path:
    PRECONDITIONS: Backoffice tool -> Events hierarchy -> Type -> Bet Intercept -> Check/Uncheck option
    """
    keep_browser_open = True

    def test_001_login_with_user_who_has_enabled_overask_functionality_and_add_selection_for_event_with_disabled_overask_for_its_type(self):
        """
        DESCRIPTION: Login with user who has enabled Overask functionality and add selection for event with disabled Overask for its type
        EXPECTED: 
        """
        pass

    def test_002_enter_stake_value_which_is_higher_than_maximum_allowed_stake_for_this_bet(self):
        """
        DESCRIPTION: Enter Stake value which is higher than maximum allowed Stake for this bet
        EXPECTED: 
        """
        pass

    def test_003_tapclick_on_bet_now_button(self):
        """
        DESCRIPTION: Tap/click on 'Bet now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        pass

    def test_004_add_multiples_to_betslip_for_event_type_with_disabled_overask(self):
        """
        DESCRIPTION: Add Multiples to Betslip for Event type with disabled Overask
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        pass

    def test_006_add_multiples_for_different_event_types_one_of_which_has_enabled_overask_functionality_and_the_second_one___disabled(self):
        """
        DESCRIPTION: Add Multiples for different event types, one of which has enabled overask functionality, and the second one - disabled
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Overask review is started/Max Bet error message is displayed depending on OB response
        EXPECTED: *   OB response is located in PlaceBet call
        """
        pass
