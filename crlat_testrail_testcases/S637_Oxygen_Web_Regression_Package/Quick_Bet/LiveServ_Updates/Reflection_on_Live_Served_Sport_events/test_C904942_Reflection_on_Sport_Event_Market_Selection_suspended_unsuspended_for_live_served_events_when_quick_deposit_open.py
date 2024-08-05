import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C904942_Reflection_on_Sport_Event_Market_Selection_suspended_unsuspended_for_live_served_events_when_quick_deposit_open(Common):
    """
    TR_ID: C904942
    NAME: Reflection on <Sport> Event/Market/Selection suspended/unsuspended for live served events when quick deposit open
    DESCRIPTION: This test case verifies Quick Bet-> Quick deposit reflection when <Sport> Event/Market/Selection is Suspended/Unsuspended.
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: - Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: - XXXXXXX - event id
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Sport> Event should be LiveServed:
    PRECONDITIONS: - Event should be **Live (isStarted=true)**
    PRECONDITIONS: - Event should be **in-Pla**y:
    PRECONDITIONS: - drilldown****TagNames=EVFLAG_BL
    PRECONDITIONS: - **isMarketBetInRun=true**
    PRECONDITIONS: - rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** ( **eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: This test case is applied only for **Mobile application**.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_into_app(self):
        """
        DESCRIPTION: Log into app
        EXPECTED: User is logged
        """
        pass

    def test_003_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_004_go_to_the_in_play_tab(self):
        """
        DESCRIPTION: Go to the 'In-Play' tab
        EXPECTED: 'In-Play' page with list of events is opened
        """
        pass

    def test_005_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_006_make_single_selection(self):
        """
        DESCRIPTION: Make single selection
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_007_enter_amount_greater_than_users_balance_into_the_stake_field(self):
        """
        DESCRIPTION: Enter amount greater than user's balance into the stake field
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        pass

    def test_008_click_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Click on 'Make a Deposit' button
        EXPECTED: Quick Deposit window is opened
        """
        pass

    def test_009_suspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_s(self):
        """
        DESCRIPTION: Suspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"S"**
        EXPECTED: 
        """
        pass

    def test_010_check_update_in_quick_deposit(self):
        """
        DESCRIPTION: Check update in Quick Deposit
        EXPECTED: * 'Your Event has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        pass

    def test_011_click_on_the_back_button(self):
        """
        DESCRIPTION: Click on the 'Back' button
        EXPECTED: * 'Your Event has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: - Stake field becomes disabled
        EXPECTED: - 'MAKE A DEPOSIT' and 'Add to Betslip' buttons are disabled
        """
        pass

    def test_012_unsuspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_a(self):
        """
        DESCRIPTION: Unsuspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"A"**
        EXPECTED: - Message that event has been suspended is removed
        EXPECTED: - Stake field becomes enabled
        EXPECTED: - 'MAKE A DEPOSIT' and 'Add to Betslip' buttons are enabled
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' warning message is displayed on yellow background below 'QUICK BET' header on **Coral**
        EXPECTED: * Same message is displayed below the Quick Stake buttons on **Ladbrokes**
        """
        pass

    def test_013_repeat_steps_8_9_for_market_and_selection(self):
        """
        DESCRIPTION: Repeat steps 8-9 for market and selection
        EXPECTED: 
        """
        pass
