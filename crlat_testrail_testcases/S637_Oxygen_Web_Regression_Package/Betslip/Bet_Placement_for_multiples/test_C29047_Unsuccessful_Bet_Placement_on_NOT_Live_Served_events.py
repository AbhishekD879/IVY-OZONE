import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29047_Unsuccessful_Bet_Placement_on_NOT_Live_Served_events(Common):
    """
    TR_ID: C29047
    NAME: Unsuccessful Bet Placement on NOT Live Served events
    DESCRIPTION: This test case verifies Bet Placement on NOT Live Served events
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    DESCRIPTION: 1. To get SiteServer info about event use the following url:
    DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    DESCRIPTION: where:
    DESCRIPTION: *   Z.ZZ - current supported version of OpenBet SiteServer
    DESCRIPTION: *   XXXXXXX - event id
    DESCRIPTION: *   LL - language (e.g. en, ukr)
    DESCRIPTION: 2. <Sport> Event is NOT LiveServed when:
    DESCRIPTION: *   Event should be not be started **(isStarted=false)**
    DESCRIPTION: *   Event should **NOT **have attribute **isMarketBetInRun=true**
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: NOTE: contact UAT team for all configurations on stg env
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_open_invictus_app(self):
        """
        DESCRIPTION: Open Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_sport_icon_on_sport_menu_ribbon(self):
        """
        DESCRIPTION: Tap on <Sport> icon on Sport Menu Ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_add_few_selections_from_different_not_live_served_events_to_the_betslip(self):
        """
        DESCRIPTION: Add few selections from different NOT Live Served events to the Betslip
        EXPECTED: *   Betslip counter is increased
        EXPECTED: *   Selections are added
        """
        pass

    def test_004_go_to_the_betslip_multiples_section(self):
        """
        DESCRIPTION: Go to the Betslip >'Multiples' section
        EXPECTED: Multiple bet built from added selections is displayed
        """
        pass

    def test_005_add_stake_to_one_of_the_added_selections(self):
        """
        DESCRIPTION: Add Stake to one of the added selections
        EXPECTED: 
        """
        pass

    def test_006_trigger_suspension_of_eventmarketoutcome_for_this_selection_where_stake_was_added(self):
        """
        DESCRIPTION: Trigger suspension of Event/Market/Outcome for this selection where Stake was added
        EXPECTED: Event/Market/Outcome becomes unsuspended
        """
        pass

    def test_007_navigate_to_betsliptap_on_bet_now_button(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: **Before OX99**
        EXPECTED: *   'Multiples' section is not rebuilt
        EXPECTED: *   Error message 'Sorry, the outcome/market/event has been suspended' is shown below corresponding single
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended' is shown above 'Bet Now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: NOTE, the text of error message may vary. It depends on what comes from the server
        EXPECTED: **After OX99**From OX99
        EXPECTED: *   'Multiples' section is not rebuilt
        EXPECTED: *   Bet is NOT placed
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_008_try_to_edit_stake_for_selection_from_step_5(self):
        """
        DESCRIPTION: Try to edit stake for selection from step #5
        EXPECTED: Stake cannot be edited, box is inactive
        """
        pass

    def test_009_enter_stake_for_any_multiple_selection(self):
        """
        DESCRIPTION: Enter Stake for any Multiple selection
        EXPECTED: **Before OX99**
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options' is shown above 'Bet Now' button
        EXPECTED: * 'Bet Now' button remains disabled
        EXPECTED: **After OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        """
        pass

    def test_010_remove_entered_stake_from_multiple_selection_from_step_8(self):
        """
        DESCRIPTION: Remove entered Stake from Multiple selection from step #8
        EXPECTED: **BEfore OX99**
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended' is shown above 'Bet Now' button
        EXPECTED: * 'Bet Now' button remains disabled
        EXPECTED: **After OX99**
        EXPECTED: * 'Place Bet' button remains disabled
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        """
        pass

    def test_011_trigger_unsuspension_of_suspended_eventmarketoutcome__refresh_the_page_and_reopen_betslip(self):
        """
        DESCRIPTION: Trigger unsuspension of suspended Event/Market/Outcome > Refresh the page and reopen Betslip
        EXPECTED: *   Multiple bets are rebuilt
        EXPECTED: *   Error messagees are NO MORE shown above 'Bet Now' button (**From OX99** 'Place Bet' button)
        """
        pass

    def test_012_trigger_starting_of_event_for_one_of_added_selections(self):
        """
        DESCRIPTION: Trigger starting of Event for one of added selections
        EXPECTED: Event becomes started
        """
        pass

    def test_013_enter_stake_for_selection_from_step_11(self):
        """
        DESCRIPTION: Enter stake for selection from step #11
        EXPECTED: Entered stake is shown
        """
        pass

    def test_014_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: Before OX99**
        EXPECTED: *   'Multiples' section is not rebuilt
        EXPECTED: *   Error message 'Event has already started' is shown above corresponding single
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended' is shown above 'Bet Now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: **after OX99**
        EXPECTED: *   'Multiples' section is not rebuilt
        EXPECTED: *   Bet is NOT placed
        EXPECTED: **Coral:**
        EXPECTED: *   Yellow message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Blue message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_015_enter_stake_for_any_multiple_selection(self):
        """
        DESCRIPTION: Enter Stake for any Multiple selection
        EXPECTED: **Before OX99**
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options' is shown above 'Bet Now' button
        EXPECTED: * 'Bet Now' button remains disabled
        EXPECTED: **After OX99**
        EXPECTED: * 'Place Bet' button remains disabled
        EXPECTED: **Coral:**
        EXPECTED: *   Yellow message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'\
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Blue message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        pass

    def test_016_remove_enterd_stake_from_multiple_selection_from_step_14(self):
        """
        DESCRIPTION: Remove enterd Stake from Multiple selection from step #14
        EXPECTED: *   Error message 'Please beware that # of your selections has been suspended' is shown above 'Bet Now' button
        EXPECTED: * 'Bet Now' button remains disabled
        EXPECTED: **After OX99**
        EXPECTED: * 'Place Bet' button remains disabled
        EXPECTED: **Coral:**
        EXPECTED: *   Yellow message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Blue message 'Event has already started' is shown above corresponding single
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        """
        pass

    def test_017_manually_delete_selection_from_started_event_via_bin_button_from_ox99_via_x_button(self):
        """
        DESCRIPTION: Manually delete selection from started event via 'Bin' button (**From OX99** via 'X' button)
        EXPECTED: *   Removed selection is no more shown within 'Singles'
        EXPECTED: *   Multiples are rebuilt with remained active selections
        """
        pass
