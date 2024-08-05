import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1216278_Verify_Timeform_Information_when_MS_is_unavailable(Common):
    """
    TR_ID: C1216278
    NAME: Verify Timeform Information when MS is unavailable
    DESCRIPTION: This test case verifies Timeform Information when Timeform microservice is unavailable
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - TimeForm info will NOT be displayed.
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -----
    PRECONDITIONS: 1) To retrieve data for particular event use the link:
    PRECONDITIONS: https://{endpoint}/api/v1/greyhoundracing/race/{openbetID}/openbet
    PRECONDITIONS: where endpoint can be:
    PRECONDITIONS: * coral-timeform-dev0.symphony-solutions.eu - DEV
    PRECONDITIONS: * coral-timeform-dev1.symphony-solutions.eu  - DEV1(PHOENIX)
    PRECONDITIONS: * coral-timeform-tst2.symphony-solutions.eu - TST2
    PRECONDITIONS: * coral-timeform-stg2.symphony-solutions.eu - STG
    PRECONDITIONS: * coral-timeform.symphony-solutions.eu -PROD
    PRECONDITIONS: 2) To trigger error from Timeform MS - block request URL
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_trigger_error_from_timeform_ms_not_availablenot_responding(self):
        """
        DESCRIPTION: Trigger error from Timeform MS (not available/not responding)
        EXPECTED: Error is received in response from Timeform MS
        """
        pass

    def test_004_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened successfully
        EXPECTED: * No error is displayed on Event details page
        """
        pass

    def test_005_verify_event_details_page(self):
        """
        DESCRIPTION: Verify Event details page
        EXPECTED: * Timeform Overview is not loaded
        EXPECTED: * Markets are displayed according to SS response
        EXPECTED: * Each-way terms are displayed according to SS response (if available)
        """
        pass

    def test_006_go_to_selection_level_and_tap_it(self):
        """
        DESCRIPTION: Go to selection level and tap it
        EXPECTED: * Timeform Selection Overview is not loaded
        EXPECTED: * Selection name is displayed
        EXPECTED: * Runner number and silk are shown
        EXPECTED: * Odds are shown next to selection name
        """
        pass
