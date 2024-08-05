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
class Test_C2563589_CMS_Verify_enabling_disabling_of_Filter_by_Odds_Card_functionality(Common):
    """
    TR_ID: C2563589
    NAME: [CMS] Verify enabling/disabling of Filter by Odds/Card functionality
    DESCRIPTION: This test case verifies enabling of Filter by Odds/Card functionality.
    PRECONDITIONS: - Filter by Odds/Card feature should be disabled in CMS
    """
    keep_browser_open = True

    def test_001_go_to_cms_and_navigate_to_system_configuration___enable_filter_sort_options_oddscard_featureverify_feature_toggle_is_enabled(self):
        """
        DESCRIPTION: Go to CMS and navigate to system configuration -> Enable Filter Sort Options (Odds/Card) feature
        DESCRIPTION: Verify feature toggle is enabled
        EXPECTED: * Feature toggle is "ON"
        """
        pass

    def test_002_go_to_oxygen_app_navigate_to_horse_racing_and_select_any_available_horse_racing_eventverify_that_filter_by_oddscard_toggle_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app, navigate to Horse racing and select any available Horse racing event
        DESCRIPTION: Verify that Filter by Odds/Card toggle is displayed
        EXPECTED: * Event details page of selected event is displayed
        EXPECTED: * Filter by Odds/Card toggle is displayed
        EXPECTED: * Default toggle value is set to:  'SORT BY: PRICE'
        """
        pass

    def test_003_go_to_greyhounds_and_select_any_available_greyhounds_eventverify_that_filter_by_oddscard_toggle_is_displayed(self):
        """
        DESCRIPTION: Go to Greyhounds and select any available Greyhounds event
        DESCRIPTION: Verify that Filter by Odds/Card toggle is displayed
        EXPECTED: * Event details page of selected Greyhound event is displayed
        EXPECTED: * Filter by Odds/Card should not be displayed
        """
        pass

    def test_004_go_to_cms___disable_filter_by_oddscard_feature___go_to_oxygen_app_and_navigate_to_horse_racing(self):
        """
        DESCRIPTION: Go to CMS -> Disable Filter by Odds/Card feature -> Go to Oxygen app and navigate to Horse racing
        EXPECTED: * Feature toggle is "OFF"
        """
        pass

    def test_005_select_horse_racing_event_from_step_2verify_that_filter_by_oddscard_toggle_is_displayed(self):
        """
        DESCRIPTION: Select Horse racing event from step 2
        DESCRIPTION: Verify that Filter by Odds/Card toggle is displayed
        EXPECTED: * Event details page of selected event is displayed
        EXPECTED: * Filter by Odds/Card should not be displayed
        """
        pass
