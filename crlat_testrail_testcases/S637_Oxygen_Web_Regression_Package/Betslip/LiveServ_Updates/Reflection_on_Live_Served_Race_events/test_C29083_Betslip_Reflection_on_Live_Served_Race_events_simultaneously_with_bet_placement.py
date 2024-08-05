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
class Test_C29083_Betslip_Reflection_on_Live_Served_Race_events_simultaneously_with_bet_placement(Common):
    """
    TR_ID: C29083
    NAME: Betslip Reflection on Live Served <Race> events simultaneously with bet placement
    DESCRIPTION: This test case verifies Betslip reflection on Live Served <Race> events simultaneously with bet placement
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-7112 Refactoring of bet placement error handling functionality
    PRECONDITIONS: User is logged in with positive balance
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selection to Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_for_selection(self):
        """
        DESCRIPTION: Enter stake value for selection
        EXPECTED: 'Bet now' button becomes enabled
        """
        pass

    def test_003_in_backoffice_tool_suspend_eventmarketoutcome_for_added_selection_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool suspend Event/Market/Outcome for added selection and save changes
        EXPECTED: 
        """
        pass

    def test_004_in_the_same_time_while_changes_in_backoffice_are_not_saved_tap_place_bet_button(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved tap 'Place Bet' button
        EXPECTED: **Before OX99**
        EXPECTED: * Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: * Error message 'Sorry, the Outcome/Market/Event Has Been Suspended' (depends on what comes in response from server) is shown on red background below corresponding single
        EXPECTED: * Response from server is received in ReadBet call
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_005_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: Betslip is cleared
        """
        pass

    def test_006_add_selection_to_betslip_and_add_a_stake_value_where__event_is_not_started_yet__in_ti_backofficebet_in_play_list_should_be_unchecked_on_event_levelbet_in_running_should_be_unchecked_on_market_levelevent_start_time_is_few_minutes_before_now(self):
        """
        DESCRIPTION: Add selection to Betslip and add a Stake value, where
        DESCRIPTION: - event is not started yet
        DESCRIPTION: - in TI backoffice:
        DESCRIPTION: 'Bet In Play List' should be unchecked on event level
        DESCRIPTION: 'Bet in Running' should be unchecked on market level
        DESCRIPTION: Event start time is few minutes before now
        EXPECTED: 
        """
        pass

    def test_007_in_backoffice_tool_start_event_for_added_selection_and_save_changes__set_isoff__yes(self):
        """
        DESCRIPTION: In Backoffice tool start event for added selection and save changes.
        DESCRIPTION: - set 'IsOff' = Yes
        EXPECTED: 
        """
        pass

    def test_008_in_the_same_time_while_changes_in_backoffice_are_not_saved_tap_place_bet_button(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved tap 'Place Bet' button
        EXPECTED: **Before OX99**
        EXPECTED: * Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: * Error message 'The Event is started' (depends on what comes in response from server) is shown in below corresponding single
        EXPECTED: * Response from server is received in ReadBet call
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: *Yellow message: 'Event has already started!" is shown above the selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: Message is displayed at the top of the betslip 'Event has already started!" with duration: 5s
        """
        pass

    def test_009_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: Betslip is cleared
        """
        pass

    def test_010_add_selection_to_betslip_and_add_a_stake_value_for_selection(self):
        """
        DESCRIPTION: Add selection to Betslip and add a Stake value for selection
        EXPECTED: 
        """
        pass

    def test_011_in_backoffice_tool_change_price_for_selection_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool change price for selection and save changes.
        EXPECTED: 
        """
        pass

    def test_012_in_the_same_time_while_changes_in_backoffice_are_not_saved_tap_place_bet_button(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved tap 'Place Bet' button
        EXPECTED: * Stake' field, 'Odds' and 'Estimated returns'  - are active.
        EXPECTED: * New Odds are displayed :
        EXPECTED: - in Red color if Odds decreased
        EXPECTED: - in Green color if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * General Error Message on Yellow background appears above Footer with text:
        EXPECTED: "Please beware that 1 of your selections had a price change"
        EXPECTED: 'Accept & Bet(1)' and is disabled
        EXPECTED: * Response from server is received in ReadBet call
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push
        EXPECTED: * notification box is displayed at the bottom of the betslip
        EXPECTED: * a notification box is displayed at the top of the betslip with animations - this is removed after 5 seconds
        EXPECTED: * the Place bet button text is updated to 'Accept price change'
        """
        pass

    def test_013_clear_betslip(self):
        """
        DESCRIPTION: Clear betslip
        EXPECTED: Betslip is cleared
        """
        pass
