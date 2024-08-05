import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11470025_BetSlip_NewRelic_monitoring__buildBet_when_actionName_BuildBetSuccess(Common):
    """
    TR_ID: C11470025
    NAME: BetSlip NewRelic monitoring - buildBet when actionName = 'BuildBetSuccess'
    DESCRIPTION: This test case verifies 'buildBet' requests monitoring in NewRelic for BetSlip when actionName = 'BuildBetSuccess'
    PRECONDITIONS: 1) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related to 'buildBet' actions in 'NRQL' field
    PRECONDITIONS: See example of the query:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'BuildBetSuccess' AND appName = 'CR-SPT-OXYGEN-MBFE-DEV0' AND username = 'natarey' LIMIT 100
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: serviceName:
    PRECONDITIONS: buildBetLogged - single and multiples bets for Logged in user
    PRECONDITIONS: buildBet - single and multiples bets for Logged out user
    PRECONDITIONS: buildComplexLegs - forecast/tricast
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: * Selection is added to the BetSlip
        EXPECTED: * 'buildBet' request is sent to BPP
        """
        pass

    def test_002_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * selection id/s
        EXPECTED: * betType
        EXPECTED: * serviceName
        """
        pass

    def test_003_trigger_suspension_of_eventmarketoutcome_and_refresh_the_page(self):
        """
        DESCRIPTION: Trigger suspension of event/market/outcome and refresh the page
        EXPECTED: * 'Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown below the corresponding single
        EXPECTED: * Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: * Updated 'buildBet' request is sent to BPP
        """
        pass

    def test_004_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * selection id/s
        EXPECTED: * ErrorCode SubCode
        EXPECTED: * serviceName
        """
        pass

    def test_005_add_at_least_two_selections_to_the_betslip_from_the_same_horse_racing_event_for_triggering_forecasttricast(self):
        """
        DESCRIPTION: Add at least two selections to the BetSlip from the same Horse Racing event for triggering forecast/tricast
        EXPECTED: * Selections are added to the BetSlip
        EXPECTED: * 'buildBet' request is sent to BPP
        EXPECTED: * 'forecast/tricast' section appears on the BetSlip
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_007_log_out_the_app(self):
        """
        DESCRIPTION: Log out the app
        EXPECTED: User is successfully logged out
        """
        pass

    def test_008_repeat_steps_1_6(self):
        """
        DESCRIPTION: Repeat steps 1-6
        EXPECTED: 
        """
        pass
