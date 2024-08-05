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
class Test_C58413076_NewRelic_tracking_for_STREAM_TOKENISATION_ERROR(Common):
    """
    TR_ID: C58413076
    NAME: NewRelic tracking for  'STREAM_TOKENISATION_ERROR'
    DESCRIPTION: This NewRelic tracking for changed ATR/Perform streaming flow when actionName = 'STREAM_TOKENISATION_ERROR'
    PRECONDITIONS: 1) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related STREAM_TOKENISATION_ERROR' action in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'STREAM_TOKENISATION_ERROR'
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: For example: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%3D%20%27STREAM_TOKENISATION_ERROR%27&hello=overview
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    PRECONDITIONS: 5) In CMS: /system-configuration/structure/performGroup: change Field Value e.g. 'mobilePartnerId' to invalid depending which platform you are testing now on
    """
    keep_browser_open = True

    def test_001__open_any_horse_racing_event_that_has_perform_stream_available_tap_watch_livelive_stream_button(self):
        """
        DESCRIPTION: * Open any Horse racing event that has Perform stream available
        DESCRIPTION: * Tap 'Watch live/Live Stream' button
        EXPECTED: * 'The Stream for this event is not currently available' pop-up/message appears
        EXPECTED: * 'secure.mobile.ladbrokes.performgroup.com response does not return "success" or fails
        EXPECTED: ![](index.php?/attachments/get/101287939)
        """
        pass

    def test_002_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * username
        EXPECTED: * eventId
        EXPECTED: * performEventId
        EXPECTED: * response
        """
        pass
