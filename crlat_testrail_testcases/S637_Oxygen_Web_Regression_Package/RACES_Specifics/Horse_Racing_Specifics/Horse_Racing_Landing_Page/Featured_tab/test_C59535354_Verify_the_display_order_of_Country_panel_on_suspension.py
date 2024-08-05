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
class Test_C59535354_Verify_the_display_order_of_Country_panel_on_suspension(Common):
    """
    TR_ID: C59535354
    NAME: Verify the display order of Country panel on suspension
    DESCRIPTION: Verify that Country Panel does not move when the first race in that panel is suspended
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

    def test_003_verify_the_country_panels_displayed(self):
        """
        DESCRIPTION: Verify the Country Panels displayed
        EXPECTED: 1: UK & Irish Races should be displayed at the top by default
        EXPECTED: 2: ACTIVE country panel should be displayed below the UK & Irish races
        EXPECTED: 3: Country Panel with first race about to start should raise only above NON ACTIVE Country panel
        """
        pass

    def test_004_in_ti_suspend_the_first_race_which_is_about_to_start_in_next_10_minutes(self):
        """
        DESCRIPTION: In TI Suspend the First race which is about to start in Next 10 minutes
        EXPECTED: Changes made in TI on Race Suspension should be successful
        """
        pass

    def test_005_refresh_page(self):
        """
        DESCRIPTION: Refresh Page
        EXPECTED: 
        """
        pass

    def test_006_verify_that_panel_does_not_move(self):
        """
        DESCRIPTION: Verify that Panel does not move
        EXPECTED: Country Panel with first race suspended should not move
        """
        pass
