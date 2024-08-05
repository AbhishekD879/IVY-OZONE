import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C50361102_Verify_that_Sport_Categories_menu_is_visible_after_navigation_from_In_Play_page_tab_with_Virtual_Scroll(Common):
    """
    TR_ID: C50361102
    NAME: Verify that Sport Categories menu is visible after navigation from In-Play page/tab with Virtual Scroll
    DESCRIPTION: This test case verifies that Sport Categories menu is visible and displays correct data after navigation from In-Play page/tab with Virtual Scroll
    PRECONDITIONS: * VirtualScroll is enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: * There are few In-Play events for any sport
    PRECONDITIONS: * There are few In-Play Watch Live events for any sport
    """
    keep_browser_open = True

    def test_001_navigate_to_in_play_tab_on_homepage(self):
        """
        DESCRIPTION: Navigate to In-Play tab on Homepage
        EXPECTED: In-Play tab is displayed with current live events
        """
        pass

    def test_002_scroll_down_until_accordion_of_expanded_sport_from_preconditions__became_sticky(self):
        """
        DESCRIPTION: Scroll down until accordion of expanded sport from preconditions  became sticky
        EXPECTED: Sport name panel became sticky
        EXPECTED: ![](index.php?/attachments/get/63272532)
        """
        pass

    def test_003_navigate_to_featured_homepage_tab_by_clicking_on_logo_in_the_header_or_button_on_the_footer(self):
        """
        DESCRIPTION: Navigate to Featured homepage tab by clicking on logo in the header or button on the footer
        EXPECTED: Sport Categories menu is visible with sports buttons without any scrolling
        """
        pass

    def test_004__navigate_to_in_play_page__watch_live_tab_scroll_down_until_some_sport_accordion_became_sticky_and_navigate_to_featured_homepage_tab(self):
        """
        DESCRIPTION: * Navigate to In-Play page > 'Watch live' tab
        DESCRIPTION: * Scroll down until some sport accordion became sticky and navigate to Featured homepage tab
        EXPECTED: Sport Categories menu is visible with sports buttons without any scrolling
        """
        pass

    def test_005_repeat_steps_few_times_as_this_incident_didnt_have_a_constant_reproducing(self):
        """
        DESCRIPTION: Repeat steps few times as this incident didn't have a constant reproducing
        EXPECTED: Sport Categories menu is visible with sports buttons without any scrolling
        """
        pass
