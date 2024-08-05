import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C60094852_Verify_display_of_Day_selector_tabs_Races_available_after_Day_3(Common):
    """
    TR_ID: C60094852
    NAME: Verify display of Day selector tabs-Races available after Day 3
    DESCRIPTION: Verify that Day name is displayed when there are no races scheduled for Today and Tomorrow
    PRECONDITIONS: 1: Login to TI and Schedule race for Day 3 or more but not greater than 7 days
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_url_or_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL or App
        EXPECTED: User should be able to launch the app
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_verify_the_display_of_meetings_in_hr_landing_pag(self):
        """
        DESCRIPTION: Verify the display of meetings in HR landing pag
        EXPECTED: 1: Meetings tab should be selected by default
        EXPECTED: For Coral: Featured tab should be selected by default
        EXPECTED: 2: UK & Irish races should be displayed at by default
        """
        pass

    def test_004_verify_the_day_selector_tabs_displayed_in_the_country_pane(self):
        """
        DESCRIPTION: Verify the Day selector tabs displayed in the Country Pane
        EXPECTED: 1: Day name should be displayed
        EXPECTED: ( If races are scheduled for 7 days later or more Race will not be displayed)
        """
        pass
