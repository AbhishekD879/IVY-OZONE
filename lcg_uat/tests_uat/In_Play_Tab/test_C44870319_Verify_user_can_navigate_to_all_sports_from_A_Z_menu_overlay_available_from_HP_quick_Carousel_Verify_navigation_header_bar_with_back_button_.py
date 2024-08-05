import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.p1
@vtest
class Test_C44870319_Verify_user_can_navigate_to_all_sports_from_A_Z_menu_overlay_available_from_HP_quick_Carousel_Verify_navigation_header_bar_with_back_button_and_click_on_it_to_redirect_to_the_previously_visited_page_(Common):
    """
    TR_ID: C44870319
    NAME: "Verify user can navigate to all sports from A-Z menu overlay available from HP quick Carousel -Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page "
    DESCRIPTION: "Verify user can navigate to all sports from A-Z menu overlay available from HP quick Carousel
    DESCRIPTION: -Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page
    """
    keep_browser_open = True
    expected_url = "https://" + tests.HOSTNAME + "/"
    sport_dict = {'Promos': 'Promotions',
                  'Horse Racing International Tote': 'International Tote',
                  'Virtuals': 'Virtual',
                  'TableTennis01': 'Table Tennis',
                  'C. League': 'UEFA CHAMPIONS LEAGUE',
                  'UEFA': 'UEFA CHAMPIONS LEAGUE',
                  'Water Surfing': 'AZ test',
                  'Fencing-QE': 'Questionengine'}

    def test_001_load_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_verify_tapping_on_menu_on_hp_quick_carousel_an_a_z_sports_overlay_opens(self):
        """
        DESCRIPTION: Verify tapping on Menu on HP quick Carousel an A-Z sports overlay opens
        EXPECTED: Menu is tappable and A-Z overlay opened
        """
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.sb.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict.keys()
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
        self.assertTrue(sports, msg='No sports found in "A-Z Sports" section')
        for sport in sports:
            if self.device_type == 'mobile':
                az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            else:
                az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(az_sports, msg='No sports found in "A-Z Sports" section')

            if sport in ['Correct 4', 'Gaming', 'Live Casino', 'Sports Roulette', 'Roulette', 'Slots', 'The Grid',
                         'Racing Super Series', 'Football Super Series', 'Responsible Gambling', 'Instant Spins', 'News & Blogs']:
                # These sports don't have header back button.
                continue
            else:
                az_sports[sport].click()
                sleep(2)
                # redirect to homepage when no events are found for sport
                if self.device.get_current_url() == self.expected_url:
                    if self.device_type == 'mobile':
                        all_items = self.site.home.menu_carousel.items_as_ordered_dict
                        all_items.get(vec.sb.ALL_SPORTS).click()
                        self.site.wait_content_state(state_name='AllSports')
                        sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict.keys()
                    else:
                        sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
                    continue
                actual_header = self.site.sports_page.header_line.page_title.text
                if sport in self.sport_dict.keys():
                    self.assertEqual(self.sport_dict[sport].upper(), actual_header.upper(),
                                     msg=f'sport {sport.upper()} is not available in {actual_header}')
                else:
                    self.assertEqual(sport.upper(), actual_header.upper(),
                                     msg=f'sport {sport.upper()} is not available in {actual_header}')
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    self.assertTrue(self.site.has_back_button,
                                    msg='"back button" is not present in navigated page')
                    self.site.back_button_click()
                else:
                    self.assertTrue(self.site.sports_page.is_back_button_displayed(),
                                    msg='"back button" is not present in navigated page')
                    self.site.sports_page.back_button_click()
                if self.device_type == 'mobile':
                    self.assertTrue(self.site.wait_content_state(state_name='AllSports'),
                                    msg=' "ALLSports page" is not displayed')
                else:
                    self.assertTrue(self.site.wait_content_state('homepage'), msg=' "HomePage" is not displayed')

    def test_003_verify_user_user_can_navigate_to_football_landing_page_from_all_sports_overlay(self):
        """
        DESCRIPTION: Verify user user can navigate to Football landing page from All sports overlay
        EXPECTED: Football landing page opened
        """
        # this step is already covered in step2

    def test_004_verify_navigation_header_bar_with__back_button_and_click_on_it_to_redirect_to_the_previously_visited_page(
            self):
        """
        DESCRIPTION: Verify navigation header bar with '<' back button and click on it to redirect to the previously visited page
        EXPECTED: user redirected to previously visited page.
        """
        # this step is already covered in step2

    def test_005_repeat_step_3_4_for_all_sports_available_on_a_z_menu(self):
        """
        DESCRIPTION: repeat step #3 #4 for all sports available on A-Z menu
        """
        # this step is already covered in step2
