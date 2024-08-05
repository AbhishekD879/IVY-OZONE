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
class Test_C58413075_NewRelic_tracking_for_STREAM_QUALIFICATION_ERROR(Common):
    """
    TR_ID: C58413075
    NAME: NewRelic tracking for  'STREAM_QUALIFICATION_ERROR'
    DESCRIPTION: This NewRelic tracking for changed ATR/Perform streaming flow when actionName = 'STREAM_QUALIFICATION_ERROR'
    PRECONDITIONS: 1) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related to'STREAM_QUALIFICATION_ERROR' action in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'STREAM_QUALIFICATION_ERROR'
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: For example: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%3D%20%27STREAM_QUALIFICATION_ERROR%27&hello=overview
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    """
    keep_browser_open = True

    def test_001__open_any_horse_racing_event_that_requires_placing_a_bet_in_order_to_watch_the_stream_tap_watch_livelive_stream_button(self):
        """
        DESCRIPTION: * Open any Horse racing event that requires placing a bet in order to watch the stream
        DESCRIPTION: * Tap 'Watch live/Live Stream' button
        EXPECTED: * 'In order to view this event you need..' pop-up/message appears
        EXPECTED: * 'optin' response returns: "Error on passing qualification".
        """
        pass

    def test_002_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * username
        EXPECTED: * eventid
        EXPECTED: * qualificationErrorCode
        EXPECTED: * errorMessageCode (e.g. 'deniedByWatchRules','servicesCrashed')
        """
        pass
