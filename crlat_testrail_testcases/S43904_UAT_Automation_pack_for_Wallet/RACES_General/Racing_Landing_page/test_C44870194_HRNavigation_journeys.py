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
class Test_C44870194_HRNavigation_journeys(Common):
    """
    TR_ID: C44870194
    NAME: HRNavigation journeys
    DESCRIPTION: "HR Navigation journeys: Home page, Highlights tab or Next Races Tab -> Tap on ""View All Horse Racing Betting"" - will lead to landing page
    DESCRIPTION: Home page, carousel link or Tab bar - App Sports (Menu) -> Tap on HR will lead to landing page
    DESCRIPTION: User is able to navigate smooth forward and backwards between the tabs and toward EDP, page is loading fine, all elements are properly displayed and is Sorted by Odds/Racecard( Filters DropDown)
    DESCRIPTION: Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the tace status and add selections to bet slip as per requirements/GDs
    DESCRIPTION: Also verify below,
    DESCRIPTION: Verify below sections on the HR
    DESCRIPTION: UK & IRE (events with typeFlagCodes 'UK' or 'IE')
    DESCRIPTION: International (events with typeFlagCodes 'INT')
    DESCRIPTION: Virtual (events with typeFlagCodes 'VR')
    DESCRIPTION: Specials Tab
    DESCRIPTION: Next Events module
    DESCRIPTION: Tomorrow Tab"
    PRECONDITIONS: Roxanne app / site is is loaded,
    PRECONDITIONS: User is on Home Page
    """
    keep_browser_open = True

    def test_001_for_desktop_only__scroll_down_on_home_page_to_next_races_and_click_on_view_all_horse_racing_events(self):
        """
        DESCRIPTION: For Desktop only : Scroll down on home page to 'NEXT RACES' and click on 'VIEW ALL HORSE RACING EVENTS'
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        pass

    def test_002_for_desktop_only___tap_on_horse_racing_from1_header_menu2_a_z_sports(self):
        """
        DESCRIPTION: For Desktop only :  Tap on Horse Racing from
        DESCRIPTION: 1. Header menu
        DESCRIPTION: 2. A-Z Sports
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        pass

    def test_003_for_mobile__tablet_only__tap_on_horses_from1_sports_carousal2_all_sports__horses3_any_quick_link_if_configured_on_home_page_eg__todays_racing(self):
        """
        DESCRIPTION: For Mobile / Tablet only : Tap on Horses from
        DESCRIPTION: 1. Sports carousal
        DESCRIPTION: 2. All Sports > Horses
        DESCRIPTION: 3. Any Quick Link if configured on Home Page eg : 'Today's Racing'
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        pass

    def test_004_verify_various_tabs_on_hr_landing_page1_meetings2_next_races3_futures4_specials(self):
        """
        DESCRIPTION: Verify various tabs on HR Landing Page
        DESCRIPTION: 1. Meetings
        DESCRIPTION: 2. Next Races
        DESCRIPTION: 3. Futures
        DESCRIPTION: 4. Specials
        EXPECTED: User should be able to move forward and backward between the tabs smoothly. all the elements of the tab should properly displayed.
        """
        pass

    def test_005_verify_meetings_tab(self):
        """
        DESCRIPTION: Verify Meetings tab
        EXPECTED: Meetings tab should display all the meetings grouped under
        EXPECTED: 1. Offers and Featured Races ( If any available)
        EXPECTED: 2. UK & IRE (events with typeFlagCodes 'UK' or 'IRE')
        EXPECTED: 3. International (events with typeFlagCodes 'INT')
        EXPECTED: 4. Virtual (events with typeFlagCodes 'VR')
        EXPECTED: User should be able to expand / collapse the grouping accordions.
        """
        pass

    def test_006_click_on_any_meeting(self):
        """
        DESCRIPTION: Click on any meeting
        EXPECTED: User is landed on the respecting Meeting(Event) Landing Page.
        EXPECTED: Should be able to scroll across the Meeting carousal.
        EXPECTED: User should be able to see the race Status
        EXPECTED: User should be able to add selections to bet slip if the race is not suspended.
        EXPECTED: User should be able to change the display Sort order : Price / Racecard (for Win/Each Way )
        """
        pass

    def test_007_while_on_hr_landing_page_tap_on_next_races(self):
        """
        DESCRIPTION: While on HR Landing page, tap on 'NEXT RACES'
        EXPECTED: All the next races that are about to start should load in order of start time, earliest being on the top.
        EXPECTED: Each event displays the first 3 entries with an option to view the full racecard by clicking on 'MORE'
        """
        pass

    def test_008_while_on_hr_landing_page_verify_future_tab(self):
        """
        DESCRIPTION: While on HR landing page, Verify Future tab
        EXPECTED: User should be able to see the information related to Future events
        """
        pass

    def test_009_while_on_hr_landing_page_verify_specials_tab(self):
        """
        DESCRIPTION: While on HR landing page, Verify Specials Tab
        EXPECTED: User should see the information related to Special HR events
        """
        pass
