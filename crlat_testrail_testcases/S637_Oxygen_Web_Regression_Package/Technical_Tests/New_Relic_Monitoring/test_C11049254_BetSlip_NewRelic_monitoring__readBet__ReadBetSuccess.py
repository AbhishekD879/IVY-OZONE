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
class Test_C11049254_BetSlip_NewRelic_monitoring__readBet__ReadBetSuccess(Common):
    """
    TR_ID: C11049254
    NAME: BetSlip NewRelic monitoring - readBet - ReadBetSuccess
    DESCRIPTION: This test case verifies 'readBet' requests monitoring in NewRelic for BetSlip when actionName = 'ReadBetSuccess'
    PRECONDITIONS: 1. Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2. Start writing the request to get data related to 'readBet' actions in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'ReadBetSuccess' AND appName = '{ENDPOINT}' AND username = '{username}' LIMIT 100
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: action names:
    PRECONDITIONS: * ReadBetError
    PRECONDITIONS: * ReadBetSuccess
    PRECONDITIONS: 1) Load Oxygen app
    PRECONDITIONS: 2) Log in app
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: Selection is added to the BetSlip
        """
        pass

    def test_002_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: * Bet successfully placed
        EXPECTED: * 'readBet' request is sent to BPP
        """
        pass

    def test_003_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp (should be there by default)
        EXPECTED: * actionName - ReadbetSuccess
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * selection id/s
        EXPECTED: * BetTypes
        EXPECTED: * Bet(response payload)
        EXPECTED: * MarketID
        EXPECTED: * eventID
        """
        pass

    def test_004_trigger_suspension_of_eventmarketoutcome_and_place_bet(self):
        """
        DESCRIPTION: Trigger suspension of event/market/outcome and place bet
        EXPECTED: * 'Stake' field, 'Odds' and 'Estimated returns' - disabled and greyed out.
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown below the corresponding single
        EXPECTED: * Warning message 'Please beware that # of your selections has been suspended' is shown on the * * * yellow background in the bottom of the Betslip
        EXPECTED: * 'readBet' request isn't sent to BPP
        """
        pass

    def test_005_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * selection id/s
        EXPECTED: * ErrorCode SubCode
        EXPECTED: * serviceName
        EXPECTED: * MarketID is empty
        EXPECTED: * eventID is empty
        """
        pass
