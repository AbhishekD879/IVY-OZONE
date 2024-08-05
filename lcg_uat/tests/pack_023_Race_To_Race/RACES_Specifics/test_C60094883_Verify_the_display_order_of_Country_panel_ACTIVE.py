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
class Test_C60094883_Verify_the_display_order_of_Country_panel_ACTIVE(Common):
    """
    TR_ID: C60094883
    NAME: Verify the display order of Country panel- ACTIVE
    DESCRIPTION: Verify that country panel raises and moves directly below to 'UK & IRE Races' meeting when first race within any country panel is ACTIVE
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

    def test_004_verify_the_country_panel_movedexample_in_hr_landing_page_under_meetings_tabracing_events_are_there_for_uk__irish_france_india_australia_racesfirst_race_in_france_starts_at_5_am_followed_by_few_racesfirst_race_in_india_starts_at_7_amfirst_race_in_australia_starts_at_6_amfirst_race_in_chile_starts_at_10_amfrance500_600_700india700__800__900australia600__800chile1000(self):
        """
        DESCRIPTION: Verify the country panel moved
        DESCRIPTION: Example: In HR landing page under meetings tab
        DESCRIPTION: Racing events are there for UK & Irish, France, India, Australia races
        DESCRIPTION: First race in France starts at 5 AM followed by few races
        DESCRIPTION: First race in India starts at 7 AM
        DESCRIPTION: First race in Australia starts at 6 AM
        DESCRIPTION: First race in Chile starts at 10 AM
        DESCRIPTION: France
        DESCRIPTION: 5:00 6:00 7:00
        DESCRIPTION: India
        DESCRIPTION: 7:00  8:00  9:00
        DESCRIPTION: Australia
        DESCRIPTION: 6:00  8:00
        DESCRIPTION: Chile
        DESCRIPTION: 10:00
        EXPECTED: 1: UK & Irish displayed at top
        EXPECTED: 2: France should be displayed below UK & Irish
        EXPECTED: 3: Australia should be displayed below France
        EXPECTED: 4: India should be displayed below Australia
        EXPECTED: 5: Chile should be displayed below India
        """
        pass

    def test_005_result_the_above_france_india_australia_races_once_they_are_race_offrefresh_the_fe_page_and_verify_the_display_of_meetings(self):
        """
        DESCRIPTION: Result the above France, India, Australia races once they are RACE OFF
        DESCRIPTION: Refresh the FE page and Verify the display of meetings
        EXPECTED: 1: UK & Irish races should be displayed at top
        EXPECTED: 2: Chile races should be displayed below UK & Irish
        EXPECTED: 3: France should be displayed below Chile
        EXPECTED: 4: India should be displayed below France
        EXPECTED: 5: Australia should be displayed below India
        EXPECTED: Once the panels are not active they should be displayed as per OB ranking
        """
        pass

    def test_006_when_the_country_panels_are_displayed_as_belowcurrent_time_640india630_race_off_730_800france700(self):
        """
        DESCRIPTION: When the Country panels are displayed as below
        DESCRIPTION: Current Time 6:40
        DESCRIPTION: India
        DESCRIPTION: 6:30 (Race OFF) 7:30 8:00
        DESCRIPTION: France
        DESCRIPTION: 7:00
        EXPECTED: India
        EXPECTED: 6:30 (Race OFF) 7:30 8:00
        EXPECTED: France
        EXPECTED: 7:00
        """
        pass

    def test_007_refresh_the_fe_at_650(self):
        """
        DESCRIPTION: Refresh the FE at 6:50
        EXPECTED: 1: France Panel will be moved above India
        EXPECTED: 2: France first race is about to start in Next 10 minutes and France OB rank is higher than India
        EXPECTED: France
        EXPECTED: 7:00
        EXPECTED: India
        EXPECTED: 6:30 (Race OFF) 7:30 8:00
        """
        pass
