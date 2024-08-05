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
class Test_C59535353_Verify_the_display_order_of_country_panel_Only_first_race(Common):
    """
    TR_ID: C59535353
    NAME: Verify the display order of country panel- Only first race
    DESCRIPTION: Verify that Country panel only moves for the First races and not for all the races
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

    def test_003_verify_that_on_page_refresh_if_any_country_panel_has_active_races_in_next_10_minutes_it_moves_above_non_active_country_panelexamplefrance730_800_900_920india800_830australia910_930(self):
        """
        DESCRIPTION: Verify that on page refresh if any Country panel has ACTIVE races in next 10 minutes it moves above NON ACTIVE Country panel
        DESCRIPTION: Example:
        DESCRIPTION: France
        DESCRIPTION: 7:30 8:00 9:00 9:20
        DESCRIPTION: India
        DESCRIPTION: 8:00 8:30
        DESCRIPTION: Australia
        DESCRIPTION: 9:10 9:30
        EXPECTED: On Page refresh at 9:00
        EXPECTED: 1: UK & Irish displayed at top
        EXPECTED: 2: Australia displayed below France
        EXPECTED: 3: India displayed below Australia
        EXPECTED: As below,
        EXPECTED: France
        EXPECTED: 7:30 8:00 9:00 9:15
        EXPECTED: Australia
        EXPECTED: 9:10 9:30
        EXPECTED: India
        EXPECTED: 8:00 8:30
        """
        pass

    def test_004_at_920_refresh_page(self):
        """
        DESCRIPTION: At 9:20 refresh page
        EXPECTED: Country panels should be displayed as
        EXPECTED: France
        EXPECTED: 7:30 8:00 9:00 9:15
        EXPECTED: Australia
        EXPECTED: 9:10 *9:30*
        EXPECTED: India
        EXPECTED: 8:00 8:30
        EXPECTED: *Australia races should not move above France*
        """
        pass
