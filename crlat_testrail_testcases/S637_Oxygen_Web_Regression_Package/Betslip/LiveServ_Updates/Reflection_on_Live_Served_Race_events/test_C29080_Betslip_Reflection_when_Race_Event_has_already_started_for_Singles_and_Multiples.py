import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29080_Betslip_Reflection_when_Race_Event_has_already_started_for_Singles_and_Multiples(Common):
    """
    TR_ID: C29080
    NAME: Betslip Reflection when <Race> Event has already started for Singles and Multiples
    DESCRIPTION: This test case verifies Betslip reflection when <Race> Event has already started.
    DESCRIPTION: Need to be split into 2 test cases, also redundant conditions regarding OX 99 (**Before OX99**) should be removed.
    PRECONDITIONS: Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    PRECONDITIONS: For triggering the following situation - **isStarted** **=** **true** for the event :
    PRECONDITIONS: * In TI Tool set **Is** **Off** **:** **YES** on Event level and suspend event
    PRECONDITIONS: * In TI Tool checkbox **Bet** **In** **Play** **List** should be **unchecked** on Event level
    PRECONDITIONS: * In TI Tool **Bet In Running** should be **unchecked** on Market level
    PRECONDITIONS: * Time of event should now not in the future
    """
    keep_browser_open = True

    def test_001_add_race_selection_of_event_which_is_not_yet_startedto_the_betslip(self):
        """
        DESCRIPTION: Add <Race> selection of event which is not yet started to the Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        pass

    def test_002_trigger_for_this_event_the_following_situationisstarted__true_isoff__yesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger for this event the following situation:
        DESCRIPTION: **isStarted = true** ("isOff = Yes")
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Stake' field, 'Odds', 'Estimated returns' and 'Each Way' check box (if present) are disabled and greyed out.
        EXPECTED: 2. Error message 'Event Has Already Started.' is shown on red background below corresponding single
        EXPECTED: 3. Error message 'Please beware that 1 of your selections has been suspended' is shown on yellow background above disabled 'Bet Now' (or 'Log In and Bet') button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: *Selection is suspended
        EXPECTED: *Yellow message: 'Event has already started!" is shown above the selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: *Selection is suspended
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * Message is displayed at the top of the betslip 'Event has already started!" with duration: 5s
        """
        pass

    def test_003_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: No selections are present in the Betslip
        """
        pass

    def test_004_add_a_few_race_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add a few race selections from different events to the Betslip
        EXPECTED: Multiples section is shown on the Betslip
        """
        pass

    def test_005_trigger_isstarted__true_isoff__yes_for_one_of_the_events(self):
        """
        DESCRIPTION: Trigger **isStarted = true** ("isOff = Yes") for one of the events
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Multiples' section is not rebuilt
        EXPECTED: 2. Error message 'Event Has Already Started.' is shown shown on red background below corresponding single
        EXPECTED: 3. 'Stake' field , 'Odds' and 'Estimated returns'  - disabled and greyed out for corresponding single
        EXPECTED: 4. Error message 'Please beware that 1 of your selections has been suspended' is displayed above disabled 'Bet Now' (or 'Log In and Bet') button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: *Selection is suspended
        EXPECTED: *Yellow message: 'Event has already started!" is shown above the selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: *Selection is suspended
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * Message is displayed at the top of the betslip 'Event has already started!" with duration: 5s
        """
        pass

    def test_006_enter_stake_into_multiple(self):
        """
        DESCRIPTION: Enter Stake into Multiple
        EXPECTED: **before OX99**
        EXPECTED: Error message 'Please beware that x of your selections has been suspended. Please remove suspended selections to get new multiple options' is displayed
        EXPECTED: **After OX99:** Message is not changed:
        EXPECTED: Coral:
        EXPECTED: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        pass
