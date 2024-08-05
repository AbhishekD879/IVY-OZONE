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
class Test_C1159079_Verify_Timeform_Summary_Information(Common):
    """
    TR_ID: C1159079
    NAME: Verify Timeform Summary Information
    DESCRIPTION: This test case verifies Timeform Summary Information on Greyhounds event details page
    DESCRIPTION: AUTOTEST [C1965336]
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
    PRECONDITIONS: *  **trainer_full_name** - to check trainer name correctness
    PRECONDITIONS: *  **star_rating** - to check stars rating correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
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
        EXPECTED: * Timeform overview is displayed above markets
        EXPECTED: * 'Show more' link is available
        """
        pass

    def test_004_tap_show_more_link(self):
        """
        DESCRIPTION: Tap 'Show more' link
        EXPECTED: Timeform Summary Information is displayed for 3 dogs and consists of the next data for each dog:
        EXPECTED: * Dog image
        EXPECTED: * Name of dog
        EXPECTED: * 'Trainer' label and name of trainer
        EXPECTED: * 'Rating' label and Stars rating
        """
        pass

    def test_005_verify_3_dogs_ordering(self):
        """
        DESCRIPTION: Verify 3 dogs ordering
        EXPECTED: 3 dogs are ordered according to **position_prediction** and **star_rating** attributes from Timeform microservice response (from the highest to the lowest)
        """
        pass

    def test_006_verify_name_of_dog_correctness(self):
        """
        DESCRIPTION: Verify name of dog correctness
        EXPECTED: Name of dog corresponds to **position_prediction** attribute from Timeform microservice response
        """
        pass

    def test_007_verify_name_of_trainer_correctness(self):
        """
        DESCRIPTION: Verify name of trainer correctness
        EXPECTED: Name of trainer corresponds to **trainer_full_name** attribute Timeform microservice response
        EXPECTED: **NOTE** meeting name returned in **trainer_full_name** attribute is NOT displayed on FE
        """
        pass

    def test_008_verify_stars_rating_correctness(self):
        """
        DESCRIPTION: Verify stars rating correctness
        EXPECTED: Stars rating  corresponds to **star_rating** attribute Timeform microservice response
        """
        pass

    def test_009_verify_non_runner_selection_within_timeform_summary(self):
        """
        DESCRIPTION: Verify Non runner selection within Timeform Summary
        EXPECTED: Non-runner selection is NOT included in Timeform Summary
        """
        pass
