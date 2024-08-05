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
class Test_C60094885_Verify_the_display_order_of_Country_panel_OB_ranking_Multiple_Active_panels(Common):
    """
    TR_ID: C60094885
    NAME: Verify the display order of Country panel-OB ranking-Multiple Active panels
    DESCRIPTION: Verify that when two or more country Panels are ACTIVE at same time then Country panels are displayed as per Open Bet ranking.
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

    def test_003_verify_the_country_panels_are_displayed_as_per_open_bet_ranking_when_two_or_more_country_panels_first_races_start_at_same_timeexample_in_hr_landing_page_under_meetings_tabracing_events_are_there_for_uk__irish_france_india_australia_racesfirst_race_in_france_starts_at_5_am_followed_by_few_racesfirst_race_in_india_starts_at_5_amfirst_race_in_australia_starts_at_5_amfrance500_600_700india500_800_900australia500_800(self):
        """
        DESCRIPTION: Verify the country panels are displayed as per Open bet ranking when two or more country panels first races start at same time
        DESCRIPTION: Example: In HR landing page under meetings tab
        DESCRIPTION: Racing events are there for UK & Irish, France, India, Australia races
        DESCRIPTION: First race in France starts at 5 AM followed by few races
        DESCRIPTION: First race in India starts at 5 AM
        DESCRIPTION: First race in Australia starts at 5 AM
        DESCRIPTION: France
        DESCRIPTION: 5:00 6:00 7:00
        DESCRIPTION: India
        DESCRIPTION: 5:00 8:00 9:00
        DESCRIPTION: Australia
        DESCRIPTION: 5:00 8:00
        EXPECTED: 1: UK & Irish displayed at top
        EXPECTED: 2: France should be displayed below UK & Irish
        EXPECTED: 3: India should be displayed below France
        EXPECTED: 4: Australia should be displayed below India
        """
        pass
