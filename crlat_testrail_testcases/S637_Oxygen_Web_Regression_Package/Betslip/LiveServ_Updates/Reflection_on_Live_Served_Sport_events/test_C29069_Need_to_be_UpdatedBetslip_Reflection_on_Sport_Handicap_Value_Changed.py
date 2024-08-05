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
class Test_C29069_Need_to_be_UpdatedBetslip_Reflection_on_Sport_Handicap_Value_Changed(Common):
    """
    TR_ID: C29069
    NAME: [Need to be Updated]Betslip Reflection on <Sport> Handicap Value Changed
    DESCRIPTION: This test case verifies Betslip reflection on <Sport> Handicap value Changed
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-9274 Change Handicap alert logic in Betslip
    DESCRIPTION: *   BMA-12031 Handicap - live serv integration
    DESCRIPTION: *   BMA-12039 Handicap - Client error handling
    DESCRIPTION: **STEP 11** hard to understand - need to update ( ** Message is displayed after closing and opening again betslip)
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Sport> Event should be LiveServed:
    PRECONDITIONS: *   Event should be **Live (isStarted=true)**
    PRECONDITIONS: *   Event should be **in-Pla**y:
    PRECONDITIONS: *   **drilldown****TagNames=EVFLAG_BL**
    PRECONDITIONS: *   **isMarketBetInRun=true**
    PRECONDITIONS: *   **rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"**
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    """
    keep_browser_open = True

    def test_001_login_into_the_oxygen_application(self):
        """
        DESCRIPTION: Login into the Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_go_to_thelive_in_playevent(self):
        """
        DESCRIPTION: Go to the **LIVE, In-Play **event
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_add_selection_that_contains_handicap_value_to_betslip(self):
        """
        DESCRIPTION: Add selection that contains Handicap value to Betslip
        EXPECTED: *   Betslip counter is increased
        EXPECTED: *   Selection is added
        """
        pass

    def test_006_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_007_trigger_the_following_situation_for_this_eventchangerawhandicapvalueon_market_leveland_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Handicap value is changed
        """
        pass

    def test_008_verify_error_message_handicap_value_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Handicap value and 'Bet now' button
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background below the corresponding selection
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: - Notification message is displayed above selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass

    def test_009_enter_value_in_stake_field_for_bet_and_tapclick_place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for bet and tap/click 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        pass

    def test_010_repeat_steps_2_9_but_make_few_selections(self):
        """
        DESCRIPTION: Repeat steps #2-9 but make few selections
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background for all bets
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: 3. 'Bet Now' button should remain active
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: - Notification message is displayed above the selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass

    def test_011_close_betslip_and_open_again_verify_error_message_about_price_changed(self):
        """
        DESCRIPTION: Close Betslip and open again, verify error message about price changed
        EXPECTED: Error message is NOT present
        """
        pass
