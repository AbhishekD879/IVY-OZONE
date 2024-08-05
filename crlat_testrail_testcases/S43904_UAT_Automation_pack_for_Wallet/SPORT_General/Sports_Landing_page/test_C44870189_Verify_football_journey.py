import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870189_Verify_football_journey(Common):
    """
    TR_ID: C44870189
    NAME: Verify football journey
    DESCRIPTION: "Site is loaded,
    DESCRIPTION: User navigates to Sport page via Homepage -> Carousel Link or Via Homepage -> All Sports (Menu) -> Football"
    DESCRIPTION: Also user can navigate form A-Z menu.
    PRECONDITIONS: Verify football journey - navigation from different pages and display > User should be able to navigate successfully
    """
    keep_browser_open = True

    def test_001_tapclick_on_football_button_from_the_main_menuorselect_football_from_a_z_menu(self):
        """
        DESCRIPTION: Tap/Click on Football button from the Main Menu
        DESCRIPTION: or
        DESCRIPTION: Select Football from A-Z menu.
        EXPECTED: Football page is loaded.
        EXPECTED: The 'Matches' tab is selected by default
        EXPECTED: The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: All events which are available are displayed for the League
        EXPECTED: Enhanced Multiple events (if available) are displayed on the top of the list and is expanded (**For Mobile/Tablet**) Enhanced Multiple events (if available) are displayed as carousel above tabs (**For Desktop**)
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel (**For Desktop**)
        """
        pass

    def test_002_verify_collapseexpandable_accordion(self):
        """
        DESCRIPTION: Verify Collapse/Expandable accordion
        EXPECTED: Collapsible and expandable accordions should be accessible
        """
        pass

    def test_003_tapclick_on_in_play_tab(self):
        """
        DESCRIPTION: Tap/Click on 'In-Play' tab
        EXPECTED: The 'In-Play' tab is loaded with the 'Live Now'/'Upcoming' sections
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        EXPECTED: 'In-Play' widget is NOT displayed in 3rd column or below main content (**For Desktop**)
        """
        pass

    def test_004_tapclick_on_the_competition_tab_accumulators_outrights__specials(self):
        """
        DESCRIPTION: Tap/Click on the Competition tab/ Accumulators/ Outrights / Specials
        EXPECTED: Event types are displayed.
        """
        pass

    def test_005_verify_display_of_landing_page_and_all_tabs_and_sub_tabs_are_accessible_journey_is_smooth_user_can_navigate_forward_and_backwards_pages_load_and_all_features_including_banners_links_are_displayed(self):
        """
        DESCRIPTION: Verify display of landing page and all tabs and sub tabs are accessible, journey is smooth, user can navigate forward and backwards, pages load and all features including Banners, links, are displayed
        EXPECTED: Subtabs, landing page and  all other tabs should be accessible
        """
        pass

    def test_006_verify_that_user_is_able_to_switch_between_the_tabs_and_subtabs_and_each_tab_displays_data_grouped_by_type_as_links_or_expandable_areas_as_per_requirements_and_functionality_works_fine_for_each_one_in_play_competitions_etc(self):
        """
        DESCRIPTION: Verify that user is able to switch between the tabs and subtabs, and each tab displays data grouped by Type, as links or expandable areas, as per requirements and functionality works fine for each one: In Play, Competitions etc
        EXPECTED: User journey between the tabs and subtabs should be smooth enough
        """
        pass

    def test_007_verify_that_on_edp_user_is_able_to_switch_between_the_markets_and_the_page_is_updated_with_the_correct_specific_market_display_and_respective_data(self):
        """
        DESCRIPTION: Verify that on EDP user is able to switch between the markets, and the page is updated with the correct specific Market display and respective data
        EXPECTED: Successful pages should be loaded
        """
        pass
