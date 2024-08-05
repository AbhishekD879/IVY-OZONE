import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870404_Verify_user_can_navigate_to_in_play_sports_via_Homepage_and_Inplay_Tab(Common):
    """
    TR_ID: C44870404
    NAME: Verify user can navigate to in-play sports via Homepage and Inplay Tab
    DESCRIPTION: Verify user is able to navigate to all available in-play sports via the homepage and in-play tab sections.
    PRECONDITIONS: User is able to access in-play sports via the homepage and in-play tab sections in both logged out and logged in status
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        self.site.wait_content_state('homepage')

    def test_002_verify_inplay_and_live_stream_section_is_visible_on_homepage_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live(self):
        """
        DESCRIPTION: Verify Inplay and Live Stream section is visible on homepage with a range of sports with correct icons and signposting badge displaying how many events are live.
        EXPECTED: Inplay and Live Stream section is visible on homepage with a range of sports displaying correct icons and signposting badge displaying how many events are live.
        """
        inplay_livestream_section = self.site.home.desktop_modules.inplay_live_stream_module
        self.assertTrue(inplay_livestream_section.is_displayed(), msg=f'"{vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME}" section is not displayed')
        self.assertEqual(inplay_livestream_section.name, vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME,
                         msg=f'Actual title "{inplay_livestream_section.name}" is not as same as Expected title {vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME}')
        self.__class__.sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
        self.assertTrue(self.sports.keys(), msg='"Menu Carousel" of sports is not displayed')
        for sport_name, sport in self.sports.items():
            self.assertTrue(sport_name, msg=f'"{sport_name}" is not displayed')
            self.assertTrue(sport.counter is not None, msg=f'Counter for "{sport_name}" is not displayed')
            self.assertTrue(sport.icon.is_displayed(), msg=f'Icon for "{sport_name}" is not displayed')

    def test_003_verify_navigation_through_each_sport_displayed(self):
        """
        DESCRIPTION: Verify navigation through each sport displayed.
        EXPECTED: User can navigate through each sport successfully.
        """
        for sport_name, sport in list(self.sports.items()):
            sport.click()
            self.assertTrue(wait_for_result(lambda: self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict[sport_name].is_selected(), timeout=10), msg=f'"{sport_name}" page is not displayed')

    def test_004_verify_correct_eventscompetitions_are_displayed_under_respective_sports_tabs_when_navigated(self):
        """
        DESCRIPTION: Verify correct events/competitions are displayed under respective sports tabs when navigated.
        EXPECTED: Correct events/competitions are displayed in respective sports tabs when navigated.
        """
        # Can not be automated

    def test_005_click_on_in_play_via_header_sub_menu_links_displayed_under_the_sports_ribbon(self):
        """
        DESCRIPTION: Click on In-Play via header sub menu links (displayed under the sports ribbon)
        EXPECTED: In-play page displayed with carousel of sports, correct icons and signposting badge displaying how many events are live.
        """
        wait_for_result(lambda: self.site.header, timeout=5)
        self.site.header.sport_menu.items_as_ordered_dict['IN-PLAY'].click()
        self.site.wait_content_state(state_name='InPlay')
        self.__class__.sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(self.sports.keys(), msg='"Menucarousel" is not displayed')

    def test_006_verify_in_play_sports_are_visible_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live(self):
        """
        DESCRIPTION: Verify In-play sports are visible with a range of sports with correct icons and signposting badge displaying how many events are live.
        EXPECTED: In-play sports are visible with a range of sports with correct icons and signposting badge displaying how many events are live.
        """
        for sport_name, sport in self.sports.items():
            if sport_name not in ['WATCH LIVE', 'Watch Live']:
                self.assertTrue(sport_name, msg=f'sport "{sport_name}" is not displayed')
                self.assertTrue(sport.counter is not None, msg=f'Counter for "{sport_name}" is not displayed')
                if sport.icon is not None:
                    self.assertTrue(sport.icon.is_displayed(), msg=f'Icon for "{sport_name}" is not displayed')

    def test_007_verify_navigation_through_each_sport_displayed(self):
        """
        DESCRIPTION: Verify navigation through each sport displayed.
        EXPECTED: User can navigate through each sport successfully.
        """
        sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports_categories, msg='sports categories not displayed')
        for sport_name, sport in list(sports_categories.items()):
            sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            if sport_name not in ['WATCH LIVE', 'Watch Live']:
                sport_tab = sports_categories[sport_name]
                sport_tab.scroll_to()
                sport_tab.perform_click()
                self.assertTrue(wait_for_result(lambda: self.site.inplay.inplay_sport_menu.items_as_ordered_dict[sport_name].is_selected(), timeout=10), msg=f'"{sport_name}" page is not displayed')

    def test_008_verify_correct_eventscompetitions_are_displayed_in_respective_sports(self):
        """
        DESCRIPTION: Verify correct events/competitions are displayed in respective sports.
        EXPECTED: Correct events/competitions are displayed in respective sports.
        """
        # cannot automate

    def test_009_repeat_above_all_steps_with_logged_in(self):
        """
        DESCRIPTION: repeat all the above steps with logged in.
        EXPECTED: repeat all the above steps with logged in.
        """
        self.navigate_to_page('Homepage')
        self.site.login()
        self.device.refresh_page()
        self.test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser()
        self.test_002_verify_inplay_and_live_stream_section_is_visible_on_homepage_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live()
        self.test_003_verify_navigation_through_each_sport_displayed()
        self.test_004_verify_correct_eventscompetitions_are_displayed_under_respective_sports_tabs_when_navigated()
        self.test_005_click_on_in_play_via_header_sub_menu_links_displayed_under_the_sports_ribbon()
        self.test_006_verify_in_play_sports_are_visible_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live()
        self.test_007_verify_navigation_through_each_sport_displayed()
        self.test_008_verify_correct_eventscompetitions_are_displayed_in_respective_sports()
