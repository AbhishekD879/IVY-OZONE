import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15478409_Verify_Silks_are_loaded_from_Aggregation_MS(Common):
    """
    TR_ID: C15478409
    NAME: Verify Silks are loaded from Aggregation MS
    DESCRIPTION: This test case verifies that Silks are loaded from Aggregation MS (which uses DF API) and return Silk via ID from silks sprite
    PRECONDITIONS: - Horse Racing Event is mapped with DF API data
    PRECONDITIONS: - List of Aggregation MS {envs.}: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    PRECONDITIONS: https://{env.}/silks/racingpost/17058,243739,266307,61763,...
    PRECONDITIONS: - Silk ID is received in response from https://ld-{env.}.api.datafabric.{env.}.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/{event id}/content?locale=en-GB&api-key={api key}
    PRECONDITIONS: in horses.silk: "{silk id}.png" attribute
    """
    keep_browser_open = True

    def test_001_navigate_to_hr_edp_from_precondition(self):
        """
        DESCRIPTION: Navigate to HR EDP from precondition
        EXPECTED: - Event details page is opened
        EXPECTED: - 'Win or E/W' tab is opened by default
        """
        pass

    def test_002_in_browser_devtools_check_how_silks_are_loadedeg_call_to_aggregation_ms_httpsaggregation_dev0coralsportsdevcloudladbrokescoralcomsilksracingpost123203144359184671b187111218882221353238386249844252924(self):
        """
        DESCRIPTION: In browser DevTools check how silks are loaded
        DESCRIPTION: (e.g. call to Aggregation MS: https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost/123203,144359,184671b,187111,218882,221353,238386,249844,252924)
        EXPECTED: - Silks should be loaded from Aggregation MS by silksIDs
        EXPECTED: (e.g. silk Id of specific horse received in https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/502368/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b corresponds to same silk id from Aggregation MS)
        """
        pass
