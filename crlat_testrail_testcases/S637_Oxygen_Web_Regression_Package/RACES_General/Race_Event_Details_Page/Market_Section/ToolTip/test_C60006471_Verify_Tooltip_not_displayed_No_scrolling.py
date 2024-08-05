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
class Test_C60006471_Verify_Tooltip_not_displayed_No_scrolling(Common):
    """
    TR_ID: C60006471
    NAME: Verify Tooltip not displayed: No scrolling
    DESCRIPTION: Verify that Tooltip is displayed only when all markets are visible in tool bar (No Scrolling needed)
    PRECONDITIONS: 1: Tooltip should be enabled in CMS
    PRECONDITIONS: 2: HR/GH events without any additional markets should be available
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

    def test_003_click_on_any_horse_racing_event_where_all_markets_are_displayed_in_the_tool_bar_no_scrolling_needed(self):
        """
        DESCRIPTION: Click on any horse racing event where all markets are displayed in the Tool bar (No Scrolling needed)
        EXPECTED: User should be navigated to event details page (race card)
        """
        pass

    def test_004_validate_that_no_tooltip_displayed(self):
        """
        DESCRIPTION: Validate that no Tooltip displayed
        EXPECTED: User should not be displayed any tooltip
        """
        pass

    def test_005_repeat_step_2_to_step_4_and_validate_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat Step 2 to Step 4 and Validate for Grey Hound racing
        EXPECTED: User should not be displayed any tooltip
        """
        pass
