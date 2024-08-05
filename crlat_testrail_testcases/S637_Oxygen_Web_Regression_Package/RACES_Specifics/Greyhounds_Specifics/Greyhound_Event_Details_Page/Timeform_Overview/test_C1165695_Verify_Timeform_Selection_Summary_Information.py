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
class Test_C1165695_Verify_Timeform_Selection_Summary_Information(Common):
    """
    TR_ID: C1165695
    NAME: Verify Timeform Selection Summary Information
    DESCRIPTION: This test case verifies Timeform Selection Summary Information on Greyhounds event details page
    DESCRIPTION: AUTOTEST [C1959314]
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
    PRECONDITIONS: *  **one_line_comment** - to check Timeform Selection Summary Information correctness
    PRECONDITIONS: *  **star_rating** - to check stars rating correctness
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
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        pass

    def test_004_tap_arrow_within_selection_area(self):
        """
        DESCRIPTION: Tap arrow within selection area
        EXPECTED: Timeform Selection Summary Information is displayed for the particular dog and consists of:
        EXPECTED: * 'Timeform Summary' label and Timeform Selection Summary data
        EXPECTED: * 'Show More' option
        EXPECTED: * 'Rating' label and rating starts
        """
        pass

    def test_005_verify_timeform_selection_summary_information_correctness(self):
        """
        DESCRIPTION: Verify Timeform Selection Summary Information correctness
        EXPECTED: Timeform Selection Summary corresponds to **one_line_comment** attribute from Timeform microservice response for particular dog
        """
        pass

    def test_006_verify_stars_rating_correctness(self):
        """
        DESCRIPTION: Verify stars rating correctness
        EXPECTED: Stars rating corresponds to **star_rating** attribute Timeform microservice response for particular dog
        """
        pass

    def test_007_verify_show_more_option(self):
        """
        DESCRIPTION: Verify 'Show More' option
        EXPECTED: * 'Show More' option is displayed when Timeform Selection Summary Information is more than 100 characters
        EXPECTED: * 'Show More' option becomes 'Show Less' after tapping it
        EXPECTED: * All Timeform Selection Summary is displayed after tapping 'Show More' option
        """
        pass

    def test_008_verify_show_less_option(self):
        """
        DESCRIPTION: Verify 'Show Less' option
        EXPECTED: * 'Show Less' option becomes 'Show More' after tapping it
        EXPECTED: * Part of Timeform Selection Summary is collapsed after tapping 'Show Less' option
        """
        pass
