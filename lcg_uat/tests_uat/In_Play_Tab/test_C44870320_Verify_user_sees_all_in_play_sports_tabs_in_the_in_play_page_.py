import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.p1
@vtest
class Test_C44870320_Verify_user_sees_all_in_play_sports_tabs_in_the_in_play_page_(Common):
    """
    TR_ID: C44870320
    NAME: "Verify user sees all in-play sports tabs in the in-play page.  "
    DESCRIPTION: This test case verify inplay sports available in In-Play tab
    PRECONDITIONS: sport should be in in-play to appear in In-Play tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("HomePage")

    def test_002_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' Landing Page is opened
        EXPECTED: Sports Menu Ribbon is shown with Categories where In-Play events are available
        EXPECTED: First <Sport> tab is opened by default
        EXPECTED: Two filter switchers are visible: 'Live Now' and 'Upcoming'
        """
        if self.device_type == 'mobile':
            in_play = vec.SB.IN_PLAY if self.brand == 'ladbrokes' else vec.siteserve.IN_PLAY_TAB
            self.site.home.menu_carousel.click_item(in_play)
            self.site.wait_content_state(state_name='in-play')
            live_now = self.site.inplay.tab_content.live_now
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(live_now.is_displayed(), msg=f'"{vec.inplay.LIVE_NOW_SWITCHER}"is not visible')
            self.assertTrue(upcoming.is_displayed(), msg=f'"{vec.inplay.UPCOMING_SWITCHER}"is not visible')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='"menu items" are not found')
            in_play_tab = menu_items[vec.siteserve.IN_PLAY_TAB]
            in_play_tab.click()
            self.site.wait_content_state(state_name='in-play')
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [vec.Inplay.LIVE_NOW_SWITCHER, vec.Inplay.UPCOMING_SWITCHER]
            self.assertEqual(sections, expected_sections, msg=f'Actual sections:"{sections}"are not same as Expected sections:"{expected_sections}"')
        self.__class__.sports_categories = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())
        self.assertTrue(self.sports_categories, msg='"sports Categories" are not displayed')
        first_sport = self.sports_categories[1]
        self.assertTrue(first_sport.is_selected(), msg=f'"{first_sport.name}" tab is not opened by default')

    def test_003_for_mobiletabletverify_sport_tabs_filteringfor_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_filtering(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Verify Sport tabs filtering
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play & Live Stream' section on Homepage and verify Sport tabs filtering
        EXPECTED: Each sport tab is tappable
        EXPECTED: -If there are any live events available for the particular sport then, number of Live events is displayed on sport icon (example: 3,2 etc)
        EXPECTED: -sports ribbon is scrollable from right to left
        EXPECTED: -Selected sport is highlighted
        """
        if self.device_type == 'mobile':
            length_of_sports_ribbon = len(self.sports_categories)
            sports = self.sports_categories[1:]
            minimum_sports = 6
        else:
            self.navigate_to_page("HomePage")
            sports = list(self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict.values())
            length_of_sports_ribbon = len(sports)
            minimum_sports = 8
        for sport in range(length_of_sports_ribbon - 1):
            if self.device_type == 'mobile':
                sports = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())[1:]
            else:
                sports = list(self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict.values())
            sports[sport].click()
            self.assertTrue(sports[sport].is_selected(), msg=f'"{sports[sport].name}" is not tapapable')
            if self.brand != 'ladbrokes' and self.device_type != 'mobile':
                self.assertTrue(sports[sport].counter is not None, msg=f'"Count label" for "{sports[sport].name}" is not displayed')
            if length_of_sports_ribbon > minimum_sports and sport == length_of_sports_ribbon - 1:
                self.assertTrue(sports[sport].is_selected(), msg='"sports ribbon" is not scrollable from right to left')
            self.assertTrue(sports[sport].is_selected(), msg=f'"{sports[sport].name}" is not highlighted')
