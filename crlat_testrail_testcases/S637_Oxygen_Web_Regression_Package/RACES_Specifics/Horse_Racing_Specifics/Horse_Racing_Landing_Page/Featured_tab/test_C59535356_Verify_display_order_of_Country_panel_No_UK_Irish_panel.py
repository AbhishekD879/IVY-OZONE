import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C59535356_Verify_display_order_of_Country_panel_No_UK_Irish_panel(Common):
    """
    TR_ID: C59535356
    NAME: Verify display order of Country panel- No UK & Irish panel
    DESCRIPTION: Verify that when any Country Panel has ACTIVE race it is displayed at top when there are no UK & Irish Races
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

    def test_003_verify_the_country_panel_display(self):
        """
        DESCRIPTION: Verify the Country Panel display
        EXPECTED: 1: UK & Irish races panel should not be displayed as there are no races
        """
        pass

    def test_004_verify_that_on_page_refresh_international_country_panel_which_has_first_race_in_next_10_minutes_is_displayed_at_top(self):
        """
        DESCRIPTION: Verify that on page refresh International Country panel which has first race in Next 10 minutes is displayed at top
        EXPECTED: On page refresh International Country panel which has first race in Next 10 minutes should be displayed at top
        """
        pass
