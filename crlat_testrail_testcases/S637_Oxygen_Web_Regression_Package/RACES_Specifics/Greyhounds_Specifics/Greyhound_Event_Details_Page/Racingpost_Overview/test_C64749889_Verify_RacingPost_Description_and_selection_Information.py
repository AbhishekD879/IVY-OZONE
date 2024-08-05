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
class Test_C64749889_Verify_RacingPost_Description_and_selection_Information(Common):
    """
    TR_ID: C64749889
    NAME: Verify RacingPost Description and selection Information
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: Description and selection Information
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
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        pass

    def test_004_go_to_selection_area_and_verify_for_the_description_of_the_event(self):
        """
        DESCRIPTION: Go to selection area and verify for the description of the event
        EXPECTED: event Selection/description area consists of:
        EXPECTED: * Silk with different colors (for different track and dog identification)
        EXPECTED: * Dog Names
        EXPECTED: * Trainer Details
        EXPECTED: * Dog Form for? last 5 races result
        EXPECTED: * Show more button
        EXPECTED: * and Odds.
        """
        pass

    def test_005_verify_trainer_name_correctness(self):
        """
        DESCRIPTION: Verify trainer name correctness
        EXPECTED: Trainer name corresponds to **trainerName** attribute from RacingPost microservice response
        """
        pass

    def test_006_verify_form_value_correctness(self):
        """
        DESCRIPTION: Verify form value correctness
        EXPECTED: Form value corresponds to **last5Runs** attribute from RacingPost microservice response
        """
        pass

    def test_007_verify_user_can_made_selections(self):
        """
        DESCRIPTION: Verify user can made selections
        EXPECTED: User should be able to made selections.
        """
        pass

    def test_008_verify_non_runner_selection_within_racingpost_summary_information(self):
        """
        DESCRIPTION: Verify Non-runner selection within RacingPost Summary Information
        EXPECTED: Non-runner selection is NOT included in RacingPost Summary Information
        """
        pass
