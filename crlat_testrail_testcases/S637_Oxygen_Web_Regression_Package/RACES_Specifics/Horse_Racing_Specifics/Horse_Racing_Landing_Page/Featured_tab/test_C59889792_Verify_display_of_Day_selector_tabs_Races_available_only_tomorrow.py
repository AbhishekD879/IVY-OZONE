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
class Test_C59889792_Verify_display_of_Day_selector_tabs_Races_available_only_tomorrow(Common):
    """
    TR_ID: C59889792
    NAME: Verify display of Day selector tabs-Races available only tomorrow
    DESCRIPTION: Verify that only Tomorrow tab is displayed when there are no races scheduled for Today or any day later than tomorrow
    PRECONDITIONS: 1: Login to TI and schedule races for only Tomorrow
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

    def test_003_verify_the_display_of_meetings_in_hr_landing_page(self):
        """
        DESCRIPTION: Verify the display of meetings in HR landing page
        EXPECTED: 1: Meetings tab should be selected by default
        EXPECTED: For Coral: Featured tab should be selected by default
        EXPECTED: 2: UK & Irish races should be displayed at by default
        """
        pass

    def test_004_verify_the_day_selector_tabs_displayed_in_the_country_panel(self):
        """
        DESCRIPTION: Verify the Day selector tabs displayed in the Country Panel
        EXPECTED: 1: Only Tomorrow tab should be displayed
        """
        pass
