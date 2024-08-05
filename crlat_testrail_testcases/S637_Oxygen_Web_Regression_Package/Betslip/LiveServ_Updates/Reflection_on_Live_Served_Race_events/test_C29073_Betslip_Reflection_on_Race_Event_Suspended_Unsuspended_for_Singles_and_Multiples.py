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
class Test_C29073_Betslip_Reflection_on_Race_Event_Suspended_Unsuspended_for_Singles_and_Multiples(Common):
    """
    TR_ID: C29073
    NAME: Betslip Reflection on <Race> Event Suspended/Unsuspended for Singles and Multiples
    DESCRIPTION: This test case verifies Betslip reflection when <Race> event is Suspended/Unsuspended for Singles and Multiples.
    DESCRIPTION: AUTOTEST: [C2292354]
    DESCRIPTION: AUTOTEST: [C2292364]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_single_race_selection(self):
        """
        DESCRIPTION: Make single Race selection
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        pass

    def test_003_trigger_the_following_situation_for_this_eventeventstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: 1.  'Stake' field, 'Odds' and 'Estimated returns', 'Each Way' check box (if present) are disabled and greyed out.
        EXPECTED: 2.  Error message 'Sorry, the event has been suspended' is shown on red background below corresponding single
        EXPECTED: 3. Error message 'Please beware that x of your selections has been suspended' is shown on yellow background above disabled 'Bet Now' (or 'Log In and Bet') button
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

    def test_004_from_ox_99_for_ladbrokeswait_5_secverify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip[ is removed
        EXPECTED: Message 'Some of your selections have been suspended' is removed from the top of the Betslip
        """
        pass

    def test_005_trigger_the_following_situation_for_this_eventeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Stake' field, 'Odds', 'Estimated returns' and 'Each Way' check box (if present)- enabled and are not greyed out.
        EXPECTED: 2. Error message 'Sorry, the event has been suspended' disappears below corresponding single
        EXPECTED: 3. Error message 'Please beware that x of your selections has been suspended' disappears above disabled 'Bet Now' (or 'Log In and Bet') button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out if stake was entered before
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: *  All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        pass

    def test_006_na_for_ox99bin_icon_was_removed_in_ox99tap_bin_icon_to_remove_bet_from_betslip(self):
        """
        DESCRIPTION: **N/A for OX99**(Bin icon was removed in OX99)
        DESCRIPTION: Tap 'Bin' icon to remove Bet from Betslip
        EXPECTED: Bet is removed from Betslip successfully
        """
        pass

    def test_007_from_ox99tap_x_button(self):
        """
        DESCRIPTION: **From OX99**
        DESCRIPTION: Tap 'X' button
        EXPECTED: Bet is removed from Betslip successfully
        """
        pass

    def test_008_add_a_few_selectionsfrom_different_events(self):
        """
        DESCRIPTION: Add a few selections from different events
        EXPECTED: 'Singles' and 'Multiples' sections are shown in the bet slip
        """
        pass

    def test_009_trigger_the_following_situation_for_one_of_eventseventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for one of events:
        DESCRIPTION: **eventStatusCode="S"**
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Multiples' section is not rebuilt, it still contain selection from Suspended event
        EXPECTED: 2. Error message 'Sorry, the event has been suspended' is shown on red background below suspended single
        EXPECTED: 3. 'Stake' field , 'Odds', 'Estimated returns' and 'Each Way' check box (if present) are disabled and greyed out for suspended single
        EXPECTED: 4. Error message 'Please beware that x of your selections has been suspended.' is shown on yellow background above disabled 'Bet Now'  (or 'Log In and Bet') button
        EXPECTED: 5. No error message is displayed for active events
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_010_enter_stake_into_multiple(self):
        """
        DESCRIPTION: Enter Stake into Multiple
        EXPECTED: **Before OX99**
        EXPECTED: Error message 'Please beware that x of your selections has been suspended. Please remove suspended selections to get new multiple options' is displayed
        EXPECTED: **After OX99:** Message is not changed:
        EXPECTED: Coral:
        EXPECTED: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        pass

    def test_011_trigger_the_following_situation_for_suspended_eventeventstatuscodea(self):
        """
        DESCRIPTION: Trigger the following situation for suspended event:
        DESCRIPTION: **eventStatusCode="A"**
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Stake' field , 'Odds', 'Estimated returns' and 'Each Way' check box (if present) are enabled and not greyed out
        EXPECTED: 2. Error message 'Sorry, the event has been suspended' disappears below the single
        EXPECTED: 3. Error message 'Please beware that x of your selections has been suspended. Please remove suspended selections to get new multiple options' disappears above disabled 'Bet Now' (or 'Log In and Bet') button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: *  All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        pass
