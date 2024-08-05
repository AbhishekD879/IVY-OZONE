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
class Test_C16394909_From_OX99_Betslip_Reflection_on_Sport_Handicap_Value_Changed_simultaneously_with_price_changed(Common):
    """
    TR_ID: C16394909
    NAME: [From OX99] Betslip Reflection on <Sport> Handicap Value Changed simultaneously with price changed
    DESCRIPTION: his test case verifies Betslip reflection on <Sport> Handicap value Changed simultaneously with price changed
    PRECONDITIONS: To get SiteServer info about event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Sport> Event should be LiveServed:
    PRECONDITIONS: Event should be LIVE ( isStarted=true )
    PRECONDITIONS: Event should be IN-PLAY:
    PRECONDITIONS: drilldown TagNames=EVFLAG_BL
    PRECONDITIONS: isMarketBetInRun=true
    PRECONDITIONS: rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: Event, Market, Outcome should be:
    PRECONDITIONS: Active ( eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A" )
    PRECONDITIONS: Odds format is Fractional
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Login into Oxygen application
        DESCRIPTION: Add selection that contains Handicap value to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip counter is increased
        EXPECTED: Selection is added
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventchange_on_market_level_handicapvalue_and_price_for_added_selection_and_save_changesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change on market level: HandicapValue and price for added selection and save changes
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: - Notification message is displayed above selection: "Handicap changed from x to x"
        EXPECTED: - info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: - Only Ladbrokes: info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: - Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        pass

    def test_003_provide_same_verification_but_add_few_selections_to_betslip(self):
        """
        DESCRIPTION: Provide same verification but add few selections to Betslip
        EXPECTED: Results are the same
        """
        pass
