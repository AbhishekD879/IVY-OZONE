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
class Test_C1158561_Verify_Timeform_Overview(Common):
    """
    TR_ID: C1158561
    NAME: Verify Timeform Overview
    DESCRIPTION: This test case verifies Timeform Overview on Greyhounds event details page
    DESCRIPTION: AUTOTEST: [C1937686]
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
    PRECONDITIONS: To retrieve data for particular event use the link:
    PRECONDITIONS: https://{endpoint}/api/v1/greyhoundracing/race/{openbetID}/openbet
    PRECONDITIONS: where endpoint can be:
    PRECONDITIONS: * coral-timeform-dev0.symphony-solutions.eu - DEV
    PRECONDITIONS: * coral-timeform-dev1.symphony-solutions.eu  - DEV1(PHOENIX)
    PRECONDITIONS: * coral-timeform-tst2.symphony-solutions.eu - TST2
    PRECONDITIONS: * coral-timeform-stg2.symphony-solutions.eu - STG
    PRECONDITIONS: * coral-timeform.symphony-solutions.eu -PROD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *  **race_distance** - to check race distance correctness
    PRECONDITIONS: *  **race_grade_name** - to check race grade correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
    PRECONDITIONS: * **verdict** - to check Timeform summary correctness
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

    def test_003_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_timeform_overview(self):
        """
        DESCRIPTION: Verify Timeform overview
        EXPECTED: ** Mobile**
        EXPECTED: Timeform overview consists of:
        EXPECTED: * 'Distance' label and race distance value
        EXPECTED: * 'Race Grade' label and race grade value
        EXPECTED: * Timeform logo
        EXPECTED: * 'TFPick' label and name of dog
        EXPECTED: * Timeform summary and 'Show More' option (if available)
        EXPECTED: **Desktop**
        EXPECTED: Timeform Overview consists of:
        EXPECTED: 'Distance' label and race distance value
        EXPECTED: 'Race Grade' label and race-grade value
        """
        pass

    def test_005_verify_race_distance_correctness(self):
        """
        DESCRIPTION: Verify race distance correctness
        EXPECTED: * Race distance value corresponds to **race_distance** attribute from Timeform microservice response
        EXPECTED: * Race distance is shown in the next format:
        EXPECTED: race_distance value + 'M' character
        """
        pass

    def test_006_verify_race_grade_correctness(self):
        """
        DESCRIPTION: Verify race grade correctness
        EXPECTED: Race grade value corresponds to **race_grade_name** attribute from Timeform microservice response
        """
        pass

    def test_007_verify_name_of_dog_correctness_displayed_next_to_tfpick_label(self):
        """
        DESCRIPTION: Verify name of dog correctness displayed next to 'TFPick' label
        EXPECTED: Name of dog corresponds to **position_prediction** attribute from Timeform microservice response
        """
        pass

    def test_008_verify_timeform_summary_correctness(self):
        """
        DESCRIPTION: Verify Timeform summary correctness
        EXPECTED: Timeform summary corresponds to **verdict** attribute from Timeform microservice response
        """
        pass

    def test_009_verify_show_more_option(self):
        """
        DESCRIPTION: Verify 'Show More' option
        EXPECTED: * 'Show More' option becomes 'Show Less' after tapping it
        EXPECTED: * 3 dogs with Timeform Summary Information are displayed after tapping 'Show More' option
        """
        pass

    def test_010_verify_show_less_option(self):
        """
        DESCRIPTION: Verify 'Show Less' option
        EXPECTED: * 3 dogs with Timeform Summary Information are collapsed after tapping 'Show Less' option
        EXPECTED: * 'Show Less' option becomes 'Show More' after tapping it
        """
        pass
