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
class Test_C64749888_Verify_Greyhounds_EDP_page_Overview(Common):
    """
    TR_ID: C64749888
    NAME: Verify Greyhounds EDP page Overview
    DESCRIPTION: This test case verifies the CMS configurations for surface bet.
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
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

    def test_003_select_event_with_racingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RacingPost available and go to its details page
        EXPECTED: Event details page is opened
        EXPECTED: ** Mobile** and **Desktop**
        """
        pass

    def test_004_verify_event_details_page_overview(self):
        """
        DESCRIPTION: Verify event details page overview
        EXPECTED: overview consists of:
        EXPECTED: *  time of the race
        EXPECTED: *  event name
        EXPECTED: *  distance of the race
        EXPECTED: *  race grade
        EXPECTED: *  racingPost logo
        EXPECTED: *  markets
        """
        pass

    def test_005_verify_race_distance_correctness(self):
        """
        DESCRIPTION: Verify race distance correctness
        EXPECTED: Race distance value corresponds to **distance** attribute from RacingPost microservice response
        """
        pass

    def test_006_verify_race_grade_correctness(self):
        """
        DESCRIPTION: Verify race grade correctness
        EXPECTED: grade value corresponds to **raceType or greade??** attribute from RacingPost microservice response
        """
        pass
