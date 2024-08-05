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
class Test_C59535350_Verify_UK_IRE_meeting_should_always_be_on_top(Common):
    """
    TR_ID: C59535350
    NAME: Verify UK & IRE meeting should always be on top
    DESCRIPTION: This test case verifies UK & IRELAND Races panel should remain at top all the time irrespective of any international race started
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

    def test_003_verify_that_one_of_the_international_country_panel_is_active_and_first_race_is_scheduled_before_any_uk__irish_first_racesrefresh_the_page_when_the_race_is_about_to_start_in_next_10_minutes(self):
        """
        DESCRIPTION: Verify that one of the International Country Panel is Active and first race is Scheduled before any UK & Irish first races
        DESCRIPTION: Refresh the page when the race is about to start in Next 10 minutes
        EXPECTED: 1: UK & Irish Races should be displayed at the top by default
        EXPECTED: 2: ACTIVE country panel should be displayed below the UK & Irish races
        EXPECTED: Note: Country Panel with first race about to start should raise only above NON ACTIVE Country panel
        """
        pass
