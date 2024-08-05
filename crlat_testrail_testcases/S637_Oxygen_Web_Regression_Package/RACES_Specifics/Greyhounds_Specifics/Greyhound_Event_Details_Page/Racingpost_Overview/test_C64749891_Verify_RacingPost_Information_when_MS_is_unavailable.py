import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C64749891_Verify_RacingPost_Information_when_MS_is_unavailable(Common):
    """
    TR_ID: C64749891
    NAME: Verify RacingPost Information when MS is unavailable
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: Information when MS is unavailable
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

    def test_003_trigger_error_from_racingpost_ms_not_availablenot_responding(self):
        """
        DESCRIPTION: Trigger error from RacingPost MS (not available/not responding)
        EXPECTED: Error is received in response from RacingPost MS
        """
        pass

    def test_004_select_event_with_racingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RacingPost available and go to its details page
        EXPECTED: * Event details page is opened successfully
        EXPECTED: * No error is displayed on Event details page
        """
        pass

    def test_005_verify_event_details_page(self):
        """
        DESCRIPTION: Verify Event details page
        EXPECTED: * Racingpost Overview is not loaded
        EXPECTED: * Markets are displayed according to SS response
        EXPECTED: * Each-way terms are displayed according to SS response (if available)
        """
        pass

    def test_006_go_to_selection_level_and_tap_it(self):
        """
        DESCRIPTION: Go to selection level and tap it
        EXPECTED: * Racingpost Selection Overview is not loaded
        EXPECTED: * Selection name is displayed
        EXPECTED: * Runner number and silk are shown
        EXPECTED: * Odds are shown next to selection name
        """
        pass
