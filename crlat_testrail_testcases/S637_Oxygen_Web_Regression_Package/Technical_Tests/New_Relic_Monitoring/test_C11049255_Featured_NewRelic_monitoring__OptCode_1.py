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
class Test_C11049255_Featured_NewRelic_monitoring__OptCode_1(Common):
    """
    TR_ID: C11049255
    NAME: Featured NewRelic monitoring - OptCode -1
    DESCRIPTION: This test case verifies 'buildBet' requests monitoring in NewRelic for BetSlip
    DESCRIPTION: Note:
    DESCRIPTION: Use the next instruction for the simulation situation when BPP(You can use it for featured-sports-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com) is down:
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+simulate+the+situation+when+Site+Serve+is+down
    PRECONDITIONS: 1) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related to Featured MS in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction WHERE appId = '54469560' AND actionName LIKE '%FEATURED%'
    PRECONDITIONS: where
    PRECONDITIONS: app IDs:
    PRECONDITIONS: * 54469068 - dev0
    PRECONDITIONS: * 54469319 - tst2
    PRECONDITIONS: * 54469423 - stg2
    PRECONDITIONS: * 54469529 - HL
    PRECONDITIONS: * 54469560 - PROD
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    """
    keep_browser_open = True

    def test_001_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Featured' tab
        EXPECTED: 'Featured' tab is selected
        """
        pass

    def test_002_open_new_relic_and_run_the_query_from_preconditions(self):
        """
        DESCRIPTION: Open New Relic and run the query from preconditions
        EXPECTED: The next attributes are received in "FEATURED_WS_STRUCTURE_RECEIVED":
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * payloadSize
        """
        pass

    def test_003_trigger_situation_when_featured_is_down(self):
        """
        DESCRIPTION: Trigger situation when featured is down
        EXPECTED: * Warning message 'Server is unavailable at the moment, please try again later.
        EXPECTED: * Button 'Reload' is displayed
        """
        pass

    def test_004_open_new_relic_and_run_the_request_part_1(self):
        """
        DESCRIPTION: Open New Relic and run the request part 1
        EXPECTED: The next attributes are received in
        EXPECTED: FEATURED_WS_CONNECTION_FAILED
        EXPECTED: FEATURED_WS_RECONNECTION_FAILED
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * error
        """
        pass

    def test_005_open_new_relic_and_run_the_request_part_2(self):
        """
        DESCRIPTION: Open New Relic and run the request part 2
        EXPECTED: The next attributes are received in
        EXPECTED: FEATURED_WS_RECONNECTION_ATTEMP
        EXPECTED: FEATURED_WS_CONNECTION_ATTEMP:
        EXPECTED: * attemp
        """
        pass
