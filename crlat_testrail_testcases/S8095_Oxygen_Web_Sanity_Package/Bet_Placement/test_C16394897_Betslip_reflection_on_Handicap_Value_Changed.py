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
class Test_C16394897_Betslip_reflection_on_Handicap_Value_Changed(Common):
    """
    TR_ID: C16394897
    NAME: Betslip reflection on Handicap Value Changed
    DESCRIPTION: This test case verifies Betslip reflection on <Sport> Handicap value Changed
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Sport> Event should be LiveServed:
    PRECONDITIONS: Event should be **Live (isStarted=true)**
    PRECONDITIONS: Event should be **in-Pla**y:
    PRECONDITIONS: drilldown****TagNames=EVFLAG_BL
    PRECONDITIONS: isMarketBetInRun=true
    PRECONDITIONS: rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    """
    keep_browser_open = True

    def test_001_login_into_the_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Login into the application
        DESCRIPTION: Add selection that contains Handicap value to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip counter is increased
        EXPECTED: Selection is added
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventchange_rawhandicapvalue_on_market_leveland_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Handicap value is changed
        """
        pass

    def test_003_verify_changes_in_betslip(self):
        """
        DESCRIPTION: Verify changes in Betslip
        EXPECTED: **Before OX 99**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background below the corresponding selection
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: **After OX 99**
        EXPECTED: - Notification message is displayed above selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass

    def test_004_enter_value_in_stake_field_for_bet_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for bet and tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        pass

    def test_005_repeat_steps_2_4_but_make_few_selections(self):
        """
        DESCRIPTION: Repeat steps #2-4 but make few selections
        EXPECTED: **Before OX 99**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background for all bets
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: 3. 'Bet Now' button should remain active
        EXPECTED: **After OX 99**
        EXPECTED: - Notification message is displayed above the selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass
