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
class Test_C1165690_Verify_Timeform_Selection_Overview(Common):
    """
    TR_ID: C1165690
    NAME: Verify Timeform Selection Overview
    DESCRIPTION: This test case verifies Timeform Selection Overview on Greyhounds event details page
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
    PRECONDITIONS: *  **trainer_full_name** - to check trainer name correctness
    PRECONDITIONS: *  **form** - to check form value correctness
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
        EXPECTED: 
        """
        pass

    def test_003_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        pass

    def test_004_go_to_selection_area(self):
        """
        DESCRIPTION: Go to selection area
        EXPECTED: Selection area consists of:
        EXPECTED: * Runner number
        EXPECTED: * Dogs name
        EXPECTED: * 'Trainer' label and trainer name
        EXPECTED: * 'Form' label and form value
        EXPECTED: * Expandable/collapsible arrow with 'expand' default state
        """
        pass

    def test_005_verify_trainer_name_correctness(self):
        """
        DESCRIPTION: Verify trainer name correctness
        EXPECTED: Trainer name corresponds to **trainer_full_name** attribute from Timeform microservice response
        EXPECTED: **NOTE** meeting name returned in **trainer_full_name** attribute is NOT displayed on FE
        """
        pass

    def test_006_verify_form_value_correctness(self):
        """
        DESCRIPTION: Verify form value correctness
        EXPECTED: Form value corresponds to **form** attribute from Timeform microservice response
        """
        pass

    def test_007_tap_arrow(self):
        """
        DESCRIPTION: Tap arrow
        EXPECTED: * Timeform Selection Summary Information is expanded
        EXPECTED: * Arrow changed its position to 'collapse' state
        """
        pass

    def test_008_tap_arrow_one_more_time(self):
        """
        DESCRIPTION: Tap arrow one more time
        EXPECTED: * Timeform Selection Summary Information is collapsed
        EXPECTED: * Arrow changed its position to 'expand' state
        """
        pass

    def test_009_select_another_market_for_a_particular_event_and_repeat_steps_4_8(self):
        """
        DESCRIPTION: Select another market for a particular event and repeat steps 4-8
        EXPECTED: 
        """
        pass
