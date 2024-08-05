import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C60036255_Verify_USA_panel_inactive_6am_6pmBST(Common):
    """
    TR_ID: C60036255
    NAME: Verify USA panel inactive 6am-6pm(BST)
    DESCRIPTION: Verify that the contry panels ordering should re-initiate at 6.00 am everyday as per OB ranking
    PRECONDITIONS: Note:* USA Panel is inactive from 6 am to 6 pm (UK time zone)
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
        EXPECTED: 3: Country Panel with first race about to start should raise only above NON ACTIVE Country panel.
        """
        pass

    def test_004_verify_every_day_at_600_am_bst_all_the_country_ordering_should_be_re_initiated_to_follow_the_openbet_ordering_for_each_country_including_active_panels(self):
        """
        DESCRIPTION: Verify every day at 6.00 am (BST), all the country ordering should be re-initiated to follow the OpenBet ordering for each country. (including active panels)
        EXPECTED: All the orderings should re-initiate to  OB ranking order for country panels.
        """
        pass

    def test_005_verify_country_panels_orderingexample_in_hr_landing_page_under_meetings_tabracing_events_are_there_for_uk__irish_usa_and_australiafirst_race_in_usa_starts_at_130_pmfirst_race_in_australia_start_at_610_amusa__130_230_330_2210australia___610_700_800(self):
        """
        DESCRIPTION: Verify country panels ordering
        DESCRIPTION: Example: In HR landing page under meetings tab
        DESCRIPTION: Racing events are there for UK & Irish, USA and Australia.
        DESCRIPTION: First race in USA starts at 1.30 pm
        DESCRIPTION: First race in Australia start at 6.10 am
        DESCRIPTION: USA:- 1.30 2.30 3.30 22.10
        DESCRIPTION: Australia :- 6.10 7.00 8.00
        EXPECTED: The country panels ordering in various time frames are
        EXPECTED: Time 12.30 am (BST)
        EXPECTED: 1: UK & Irish displayed at top
        EXPECTED: 2. USA should display below UK & Irish
        EXPECTED: 3: Australia should be displayed below USA
        EXPECTED: At 6.00 (BST) country panels should re-initiate to OB ranking
        EXPECTED: 1. UK & Irish displayed at top
        EXPECTED: 2. USA should display below UK & Irish
        EXPECTED: 4. Australia should be displayed below USA
        EXPECTED: Time 6.00:01 (BST) country panels should raises and moves directly below to 'UK & IRE Races' meeting when first race within any country panel is ACTIVE. (After 6.00.01 BST)
        EXPECTED: 1. UK & Irish displayed at top
        EXPECTED: 2. Australia should be displayed below UK & Irish
        EXPECTED: 3: USA should be displayed below Australia
        """
        pass
