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
class Test_C64749893_Verify_RacingPost_widget_data_correctness(Common):
    """
    TR_ID: C64749893
    NAME: Verify RacingPost widget data correctness
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: widget data correctness
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_001_load_oxygen_appgo_to_the_greyhounds_landing_pageselect_event_with_racingpost_available_and_go_to_its_details_pageverify_racingpost_widgetverify_racingpost_widget_data_correctness(self):
        """
        DESCRIPTION: Load Oxygen app
        DESCRIPTION: Go to the Greyhounds landing page
        DESCRIPTION: Select event with RacingPost available and go to its details page
        DESCRIPTION: Verify RacingPost widget
        DESCRIPTION: Verify RacingPost widget data correctness.
        EXPECTED: Homepage is loaded
        EXPECTED: Greyhounds landing page is opened
        EXPECTED: * Event details page is opened
        EXPECTED: * RacingPost widget is located in Main Column under selections list
        EXPECTED: RacingPost consists of racing post image (as per the Zeplin links) based on the previous performance of the dogs (ratings).
        EXPECTED: * the value after racingpost widget should be same as postpick attribute from API response in network tab.
        """
        pass
