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
class Test_C29072_Betslip_Reflection_on_Live_Served_Sport_events_simultaneously_with_bet_placement(Common):
    """
    TR_ID: C29072
    NAME: Betslip Reflection on Live Served <Sport> events simultaneously with bet placement
    DESCRIPTION: This test case verifies Betslip reflection on Live Served <Sport> events simultaneously with bet placement
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
        DESCRIPTION: Enter stake value for selection.
        EXPECTED: 
        """
        pass

    def test_003_in_backoffice_tool_suspend_eventmarketoutcome_for_added_selection_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool suspend Event/Market/Outcome for added selection and save changes.
        EXPECTED: 
        """
        pass

    def test_004_in_the_same_time_while_changes_in_backoffice_are_not_saved__enter_stake_value_for_an_added_selection_tap_bet_now_buttonfor_better_results_use_live_event_with_bir_delay_in_10_sec_it_will_give_you_chance_to_suspend_the_eventselectionoutcome_whilst_it_is_in_the_process_of_placing_the_bet_place_bet__when_it_will_be_under_bir_delay__suspend_neede_stuff(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved > enter Stake value for an added selection> tap 'Bet Now' button
        DESCRIPTION: (For better results use Live event with BIR delay in 10 sec. It will give you chance to suspend the event/selection/outcome whilst it is in the process of placing the bet. Place bet > when it will be under BIR delay > suspend neede stuff)
        EXPECTED: **Before OX99**
        EXPECTED: 1. Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: 2. Error message 'Sorry, the outcome/market/event has been suspended'  (depends on what comes in response from server) is shown below corresponding single
        EXPECTED: 3. Response from server is received in ReadBet call
        EXPECTED: 4. Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background above 'Bet Now' button
        EXPECTED: 5. In case of available multiples with entered stake, warning message is: 'Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options' is shown on the yellow background above 'Bet Now' button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_005_clear_betslip_and_add_new_selection_horses_or_greyhounds_where__event_is_not_started_yet__in_ti_backofficebet_in_play_list_should_be_unchecked_on_event_levelbet_in_running_should_be_unchecked_on_market_levelevent_start_time_is_few_minutes_before_now(self):
        """
        DESCRIPTION: Clear betslip and add new selection (Horses or Greyhounds) where:
        DESCRIPTION: - event is not started yet
        DESCRIPTION: - in TI backoffice:
        DESCRIPTION: 'Bet In Play List' should be unchecked on event level
        DESCRIPTION: 'Bet in Running' should be unchecked on market level
        DESCRIPTION: Event start time is few minutes before now
        EXPECTED: 
        """
        pass

    def test_006_in_backoffice_tool_start_event_for_added_selection_and_save_changes__set_isoff__yes(self):
        """
        DESCRIPTION: In Backoffice tool start event for added selection and save changes:
        DESCRIPTION: - set 'IsOff' = Yes
        EXPECTED: 
        """
        pass

    def test_007_in_the_same_time_while_changes_in_backoffice_are_not_saved__enter_stake_value_for_an_added_selection_tap_bet_now_button(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved > enter Stake value for an added selection> tap 'Bet Now' button
        EXPECTED: 1. Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: 2. Error message 'Event has already started!' is shown below corresponding single
        EXPECTED: 3. Response from server is received in ReadBet call
        EXPECTED: 4. Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background above 'Bet Now' button
        EXPECTED: 5. In case of available multiples with entered stake, warning message is: 'Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options' is shown on the yellow background above 'Bet Now' button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/39908)
        """
        pass

    def test_008_clear_betslip_and_add_new_selection(self):
        """
        DESCRIPTION: Clear betslip and add new selection
        EXPECTED: 
        """
        pass

    def test_009_in_backoffice_tool_change_price_for_selection_and_save_changes(self):
        """
        DESCRIPTION: In Backoffice tool change price for selection and save changes.
        EXPECTED: 
        """
        pass

    def test_010_in_the_same_time_while_changes_in_backoffice_are_not_saved__enter_stake_value_for_an_added_selection_tap_bet_now_button(self):
        """
        DESCRIPTION: In the same time while changes in backoffice are not saved > enter Stake value for an added selection> tap 'Bet Now' button
        EXPECTED: 1. Previous odds become crossed out, up/down arrows showing if odds went up or down and current odds are displayed. Arrows and current price are indicated by arrow direction and color format. If odds went up - green, if odds went down - red
        EXPECTED: 2. Notification banner appears above Betslip footer section on the yellow background: "Please beware that <number of bets with changed price> of your selections had a price change."
        EXPECTED: 3. 'Bet Now' button is  changed to 'Accept & Bet (<number of selections with price change>)'
        EXPECTED: 4. 'Clear Betslip' and 'Accept & Bet (<number of selections with price change>)' buttons are enabled
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: *the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'etslip with animations - this is removed after 5 seconds
        EXPECTED: the Place bet button text is updated to 'Accept price change'
        """
        pass

    def test_011_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_1_10_for_multiples(self):
        """
        DESCRIPTION: Repeat steps 1-10 for multiples
        EXPECTED: **Before OX99**
        EXPECTED: Results are the same
        EXPECTED: **From OX99:**
        EXPECTED: Results are the same only messages is different:
        EXPECTED: Coral:
        EXPECTED: Message is displayed at the bottom of the betslip: 'Please beware **some** of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * Message is displayed at the bottom of the betslip: ' **Some** of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip ' **Some** of your selections have been suspended' with duration: 5s
        """
        pass
