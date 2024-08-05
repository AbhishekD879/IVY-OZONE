import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870319_Verify_user_can_navigate_to_all_sports_from_A_Z_menu_overlay_available_from_HP_quick_Carousel_Verify_navigation_header_bar_with_back_button_and_click_on_it_to_redirect_to_the_previously_visited_page_(Common):
    """
    TR_ID: C44870319
    NAME: "Verify user can navigate to all sports from A-Z menu overlay available from HP quick Carousel -Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page "
    DESCRIPTION: "Verify user can navigate to all sports from A-Z menu overlay available from HP quick Carousel
    DESCRIPTION: -Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_tapping_on_menu_on_hp_quick_carousel_an_a_z_sports_overlay_opens(self):
        """
        DESCRIPTION: Verify tapping on Menu on HP quick Carousel an A-Z sports overlay opens
        EXPECTED: Menu is tappable and A-Z overlay opened
        """
        pass

    def test_003_verify_user_user_can_navigate_to_football_landing_page_from_all_sports_overlay(self):
        """
        DESCRIPTION: Verify user user can navigate to Football landing page from All sports overlay
        EXPECTED: Football landing page opened
        """
        pass

    def test_004_verify_navigation_header_bar_with__back_button_and_click_on_it_to_redirect_to_the_previously_visited_page(self):
        """
        DESCRIPTION: Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page
        EXPECTED: user redirected to previously visited page.
        """
        pass

    def test_005_repeat_step_3_4_for_all_sports_available_on_a_z_menu(self):
        """
        DESCRIPTION: repeat step #3 #4 for all sports available on A-Z menu
        EXPECTED: 
        """
        pass
