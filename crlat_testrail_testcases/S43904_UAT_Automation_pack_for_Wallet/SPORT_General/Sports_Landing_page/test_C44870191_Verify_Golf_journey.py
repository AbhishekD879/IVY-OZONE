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
class Test_C44870191_Verify_Golf_journey(Common):
    """
    TR_ID: C44870191
    NAME: Verify Golf journey
    DESCRIPTION: 
    PRECONDITIONS: "Site is loaded,
    PRECONDITIONS: User navigates to Sport page page via Homepage -> Carousel Link or Via Homepage -> All Sports (Menu) -> Golf"
    """
    keep_browser_open = True

    def test_001_verify_golf_journey___navigation_from_different_pages_and_display(self):
        """
        DESCRIPTION: Verify Golf journey - navigation from different pages and display
        EXPECTED: User should be able to navigate successfully
        """
        pass

    def test_002_verify_collapseexpandable_accordion(self):
        """
        DESCRIPTION: Verify Collapse/Expandable accordion
        EXPECTED: Collapsible and expandable accordions should be accessible
        """
        pass

    def test_003_verify_display_of_landing_page_and_all_tabs_and_sub_tabs_are_accessible_journey_is_smooth_user_can_navigate_forward_and_backwards_pages_load_and_all_features_including_banners_links_are_displayed(self):
        """
        DESCRIPTION: Verify display of landing page and all tabs and sub tabs are accessible, journey is smooth, user can navigate forward and backwards, pages load and all features including Banners, links, are displayed.
        EXPECTED: Subtabs, landing page and  all other tabs should be accessible
        """
        pass

    def test_004_verify_that_user_is_able_to_switch_between_the_tabs_and_subtabs_and_each_tab_displays_data_grouped_by_type_as_links_or_expandable_areas_as_per_requirements_and_functionality_works_fine_for_each_one_in_play_events_outright_coupons_etc(self):
        """
        DESCRIPTION: Verify that user is able to switch between the tabs and subtabs, and each tab displays data grouped by Type, as links or expandable areas, as per requirements and functionality works fine for each one: In Play, Events, Outright, Coupons, etc.
        EXPECTED: User journey between the tabs and subtabs should be smooth enough
        """
        pass

    def test_005_verify_that_on_edp_user_is_able_to_switch_between_the_markets_and_the_page_is_updated_with_the_correct_specific_market_display_and_respective_data(self):
        """
        DESCRIPTION: Verify that on EDP user is able to switch between the markets, and the page is updated with the correct specific Market display and respective data
        EXPECTED: Successful pages should be loaded
        """
        pass
