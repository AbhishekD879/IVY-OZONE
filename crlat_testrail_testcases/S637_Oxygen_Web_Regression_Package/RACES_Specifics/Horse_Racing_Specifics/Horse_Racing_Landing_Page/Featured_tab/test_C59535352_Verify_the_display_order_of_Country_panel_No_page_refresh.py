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
class Test_C59535352_Verify_the_display_order_of_Country_panel_No_page_refresh(Common):
    """
    TR_ID: C59535352
    NAME: Verify the display order of Country panel- No page refresh
    DESCRIPTION: Verify that Country panel does not move up when User does not refresh the page even the panel has first race which is about to start in Next 10 minutes
    PRECONDITIONS: Note:* USA Panel is inactive from 6 am to 6 pm (UK time zone) as per the BMA-56686
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_or_coral_urlmobile_app_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes or Coral URL
        DESCRIPTION: Mobile App: Launch the app
        EXPECTED: User should be able to launch the URL
        EXPECTED: Mobile App: User should be able to launch the app
        """
        pass

    def test_002_click_on_horse_racing_button_from_main_menumobile_click_on_horse_racing_icon_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on 'Horse Racing' button from main menu
        DESCRIPTION: Mobile: Click on Horse racing icon from Sports ribbon
        EXPECTED: 1: User should be navigated to Horse racing landing page
        EXPECTED: 2: Ladbrokes: By default Meetings tab should be displayed
        EXPECTED: Coral: By default Featured tab should be displayed
        EXPECTED: 3: UK & Irish Races should be displayed at the top by default
        """
        pass

    def test_003_verify_the_display_of_country_panels(self):
        """
        DESCRIPTION: Verify the display of Country Panels
        EXPECTED: 1: UK & Irish displayed at top
        EXPECTED: 2: All other Country panels should be displayed below UK & Irish races
        """
        pass

    def test_004_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Do not Refresh the page
        EXPECTED: 
        """
        pass

    def test_005_verify_that_one_country_panel_has_first_race_is_scheduled_in_next_10_minutes_and_no_other_country_has_any_active_racesexample_country_panels_are_displayed_in_below_orderfranceindiaaustralia__australia_has_first_race_to_start_in_next_10_minutes__france_and_india_have_no_active_races(self):
        """
        DESCRIPTION: Verify that one Country panel has first race is scheduled in next 10 minutes and no other Country has any ACTIVE races
        DESCRIPTION: Example: Country panels are displayed in below order
        DESCRIPTION: France
        DESCRIPTION: India
        DESCRIPTION: Australia
        DESCRIPTION: --Australia has first race to start in next 10 minutes
        DESCRIPTION: --France and India have NO ACTIVE races
        EXPECTED: User should be able to see the Country Panel does not move even when the Country panel has ACTIVE race
        EXPECTED: Example
        EXPECTED: User should be displayed the same order even when Australia race is about to begun
        EXPECTED: France
        EXPECTED: India
        EXPECTED: Australia
        EXPECTED: Note: User did not refresh the page
        """
        pass
