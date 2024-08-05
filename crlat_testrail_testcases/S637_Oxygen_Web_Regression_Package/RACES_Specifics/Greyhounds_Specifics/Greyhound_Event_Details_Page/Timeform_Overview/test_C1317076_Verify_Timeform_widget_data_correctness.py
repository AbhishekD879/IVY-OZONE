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
class Test_C1317076_Verify_Timeform_widget_data_correctness(Common):
    """
    TR_ID: C1317076
    NAME: Verify Timeform widget data correctness
    DESCRIPTION: This test case verifies Timeform widget data correctness on Greyhounds Event Details page
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
    PRECONDITIONS: *  **trainerFullName** - to check trainer name correctness
    PRECONDITIONS: *  **starRating** - to check stars rating correctness
    PRECONDITIONS: *  **greyHoundFullName** - to check name of dog correctness
    PRECONDITIONS: *  **positionPrediction** - to check position prediction of dogs
    PRECONDITIONS: *  **verdict** - to check Timeform summary correctness
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_in_desktop_mode_with_resolution_of_970px(self):
        """
        DESCRIPTION: Load Oxygen app in Desktop mode with resolution of 970px
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
        EXPECTED: * Timeform widget is located under selections list
        EXPECTED: * Timeform is expanded by default
        """
        pass

    def test_004_verify_name_of_dog_correctness_displayed_next_to_tfpick_label(self):
        """
        DESCRIPTION: Verify name of dog correctness displayed next to 'TFPick' label
        EXPECTED: Name of dog corresponds to **greyHoundFullName** attribute from Timeform microservice response
        """
        pass

    def test_005_verify_timeform_summary_correctness(self):
        """
        DESCRIPTION: Verify Timeform summary correctness
        EXPECTED: Timeform summary corresponds to **verdict** attribute from Timeform microservice response
        """
        pass

    def test_006_verify_3_dogs_ordering(self):
        """
        DESCRIPTION: Verify 3 dogs ordering
        EXPECTED: 3 dogs are ordered according to **positionPrediction** and **starRating** attributes from Timeform microservice response (from the highest to the lowest)
        """
        pass

    def test_007_verify_name_of_dog_correctness(self):
        """
        DESCRIPTION: Verify name of dog correctness
        EXPECTED: Name of dog corresponds to **positionPrediction** attribute from Timeform microservice response
        """
        pass

    def test_008_verify_name_of_trainer_correctness(self):
        """
        DESCRIPTION: Verify name of trainer correctness
        EXPECTED: Name of trainer corresponds to **trainerFullName** attribute Timeform microservice response
        EXPECTED: **NOTE** meeting name returned in **trainerFullName** attribute is NOT displayed on FE
        """
        pass

    def test_009_verify_stars_rating_correctness(self):
        """
        DESCRIPTION: Verify stars rating correctness
        EXPECTED: Stars rating  corresponds to **starRating** attribute Timeform microservice response
        """
        pass

    def test_010_verify_non_runner_selection_within_timeform_summary_information(self):
        """
        DESCRIPTION: Verify Non-runner selection within Timeform Summary Information
        EXPECTED: Non-runner selection is NOT included in Timeform Summary Information
        """
        pass

    def test_011_change_resolution_from_970px_to_1025px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 970px to 1025px and repeat steps #4-10
        EXPECTED: 
        """
        pass

    def test_012_change_resolution_from_1025px_to_1280px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 1025px to 1280px and repeat steps #4-10
        EXPECTED: 
        """
        pass

    def test_013_change_resolution_from_1280px_to_1600px_and_repeat_steps_4_10(self):
        """
        DESCRIPTION: Change resolution from 1280px to 1600px and repeat steps #4-10
        EXPECTED: 
        """
        pass
