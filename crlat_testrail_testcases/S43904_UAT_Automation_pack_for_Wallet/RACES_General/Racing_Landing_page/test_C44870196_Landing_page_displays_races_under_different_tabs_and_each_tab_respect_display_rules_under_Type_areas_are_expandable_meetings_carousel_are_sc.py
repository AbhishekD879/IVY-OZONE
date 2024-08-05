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
class Test_C44870196_Landing_page_displays_races_under_different_tabs_and_each_tab_respect_display_rules_under_Type_areas_are_expandable_meetings_carousel_are_scrollable_and_user_can_see_the_race_status_and_add_selections_to_bet_slip_as_per_requirements_GDs_Verify_Co(Common):
    """
    TR_ID: C44870196
    NAME: Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the race status and add selections to bet slip as per requirements/GDs-Verify Co
    DESCRIPTION: "Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the race status and add selections to bet slip as per requirements/GDs
    DESCRIPTION: -Verify Collapse/Expandable accordion
    DESCRIPTION: User is able to switch between the tabs or navigate back. to race landing page
    DESCRIPTION: Verify that the data is correct and completely displayed.
    DESCRIPTION: Verify the Components of the race card
    DESCRIPTION: -Each slide/event/card in the carousel will have below components
    DESCRIPTION: -Header with the Name, Time and More link navigating the user to the specific race card.
    DESCRIPTION: -E/W terms
    DESCRIPTION: -Display all selections with the silks and details same as production
    DESCRIPTION: -Display runners in chronological order
    DESCRIPTION: -Display unnamed favourite
    DESCRIPTION: -Watch Icon when the stream is available."
    PRECONDITIONS: App/Site is loaded
    PRECONDITIONS: User is on the Horse racing page
    """
    keep_browser_open = True

    def test_001_verify_racing_landing_pages_display_different_tabshr_featuredfuture_specials_yourcall_etcgr_today_tomorrow_futureby_meeting_and_by_time(self):
        """
        DESCRIPTION: Verify Racing Landing pages display different tabs
        DESCRIPTION: HR: FEATURED,FUTURE, SPECIALS, YOURCALL etc
        DESCRIPTION: GR: TODAY TOMORROW FUTURE/BY MEETING AND BY TIME
        EXPECTED: User should be able to see these tabs.
        EXPECTED: HR: FEATURED, FUTURE, SPECIALS, YOURCALL etc
        EXPECTED: GR: TODAY TOMORROW FUTURE/BY MEETING AND BY TIME
        """
        pass

    def test_002_click_and_verify_all_accordions_are_expandablecollapsible(self):
        """
        DESCRIPTION: Click and Verify all accordions are Expandable/Collapsible.
        EXPECTED: User should be able Expand/Collapse accordions by clicking on them.
        """
        pass

    def test_003_verify_the_components_of_the_race_card(self):
        """
        DESCRIPTION: Verify the Components of the race card
        EXPECTED: User should be able to see
        EXPECTED: Each slide/event/card in the carousel will have below components
        EXPECTED: -Header with the Name, Time and More link navigating the user to the specific race card.
        EXPECTED: -E/W terms displayed
        EXPECTED: -Display all selections with the silks and details same as production
        EXPECTED: -Display runners in chronological order by taking sort order as racecard
        EXPECTED: -Display Unnamed Favourite & Unnamed 2nd Favourite
        EXPECTED: -LIVE STREAM when the stream is available.
        """
        pass
