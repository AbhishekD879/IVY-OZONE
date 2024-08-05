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
class Test_C60006473_Verify_display_of_Tooltip_only_once_for_a_device(Common):
    """
    TR_ID: C60006473
    NAME: Verify display of Tooltip: only once for a device
    DESCRIPTION: Verify that ToolTip is displayed only once for a device
    PRECONDITIONS: 1: Tooltip should be enabled in CMS
    PRECONDITIONS: 2: HR/GH events should be available with additional markets that needs scrolling
    PRECONDITIONS: 3: Tooltip for the device is not shown previously
    """
    keep_browser_open = True

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        pass

    def test_003_click_on_any_horse_racing_event_that_has_additional_markets_that_needs_scrolling(self):
        """
        DESCRIPTION: Click on any horse racing event that has additional markets that needs scrolling
        EXPECTED: User should be navigated to event details page (race card)
        """
        pass

    def test_004_validate_that_there_are_more_markets_for_you_to_view_below_tooltip_is_displayed(self):
        """
        DESCRIPTION: Validate that "There are more markets for you to view below" Tooltip is displayed
        EXPECTED: User should be able to see the Tooltip "There are more markets for you to view below" which is displayed is same as that is Configured in CMS
        """
        pass

    def test_005_click_anywhere_on_screen_and_validate_that_tooltip_is_closed(self):
        """
        DESCRIPTION: Click anywhere on screen and Validate that Tooltip is closed
        EXPECTED: Tooltip should be closed
        """
        pass

    def test_006_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back button
        EXPECTED: User should be navigated back to racing landing page
        """
        pass

    def test_007_navigate_back_to_the_same_event_and_validate_tooltip_display(self):
        """
        DESCRIPTION: Navigate back to the same event and validate Tooltip display
        EXPECTED: 1: User should be navigated to Event details page
        EXPECTED: 2: User should not be displayed any tooltip
        """
        pass

    def test_008_repeat_the_same_by_logging_out_or_re_launching_the_app(self):
        """
        DESCRIPTION: Repeat the same by logging out or re-launching the App
        EXPECTED: 1: No Tooltip should be displayed
        """
        pass
