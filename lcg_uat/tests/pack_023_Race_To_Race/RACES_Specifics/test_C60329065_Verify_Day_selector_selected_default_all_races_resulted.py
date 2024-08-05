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
class Test_C60329065_Verify_Day_selector_selected_default_all_races_resulted(Common):
    """
    TR_ID: C60329065
    NAME: Verify Day selector selected default- all races resulted
    DESCRIPTION: Verify that when all the races Under Today tab are resulted in any country panel on page refresh 'Tomorrow' or the next Day selector tab is selected by default
    PRECONDITIONS: 1: All the races scheduled for Today in a Country panel should be resulted
    PRECONDITIONS: 2: Two or More Day selector tabs should be available in that Country Panel
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
        EXPECTED: 1: Today tab should be selected by default
        EXPECTED: (All Races for Today are not yet resulted)
        """
        pass

    def test_005_verify_the_day_selector_tab_displayed_in_the_country_panel_when_all_races_under_today_tab_are_resulted(self):
        """
        DESCRIPTION: Verify the Day Selector tab displayed in the Country panel when all races under Today tab are resulted
        EXPECTED: *Without Page Refresh
        EXPECTED: 1: Today tab is selected by default when all the races are resulted
        EXPECTED: *Page Refresh
        EXPECTED: 1; Tomorrow or the Next Day selector tab should be selected by default
        EXPECTED: 2: User should be able to switch between the today and current day selector tab
        """
        pass
