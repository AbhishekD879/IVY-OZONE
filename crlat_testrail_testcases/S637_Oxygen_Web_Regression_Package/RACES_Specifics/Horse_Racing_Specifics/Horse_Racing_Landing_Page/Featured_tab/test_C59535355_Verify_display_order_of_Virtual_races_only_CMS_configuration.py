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
class Test_C59535355_Verify_display_order_of_Virtual_races_only_CMS_configuration(Common):
    """
    TR_ID: C59535355
    NAME: Verify display order of Virtual races-only CMS configuration
    DESCRIPTION: Verify that Virtual races panel dos not move when first race in that Panel is about to start in Next 10 minutes
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

    def test_004_refresh_the_page_when_virtual_race_is_less_than_10_mins_to_start(self):
        """
        DESCRIPTION: Refresh the page when virtual race is less than 10 mins to start
        EXPECTED: 
        """
        pass

    def test_005_verify_that_virtual_races_panel_position_doesnt_change(self):
        """
        DESCRIPTION: Verify that Virtual races panel position doesn't change
        EXPECTED: Virtual Races panel should not reposition
        """
        pass
