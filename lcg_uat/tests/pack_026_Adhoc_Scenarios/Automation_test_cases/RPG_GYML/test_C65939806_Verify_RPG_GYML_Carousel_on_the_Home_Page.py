import pytest
import tests
import requests
import json
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.adhoc_suite
@pytest.mark.rpg_gyml
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.login
@vtest
# This TestCase Covers C65939807, C65939808, C65939809, C65939810
class Test_C65939806_Verify_RPG_GYML_Carousel_on_the_Home_Page(Common):
    """
    TR_ID: C65939806
    NAME: Verify RPG/GYML Carousel on the Home Page.
    DESCRIPTION: This testcase verifies RPG/GYML carousel
    DESCRIPTION: on the Homepage for logged in user.
    PRECONDITIONS: 1. Login to CMS.
    PRECONDITIONS: 2. Navigate to Hompage-> Module Order-> 'Recently Played Games Module'.
    PRECONDITIONS: 3. 'Recently Played Games' checkbox(for enable/disable) the feature.
    PRECONDITIONS: Note: To view the RPG/GYML module in home page user must play atleast one game.
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.gaming_url_mismatch:
            cls.cms_config.update_recently_played_games(seeMoreLink=cls.cms_gaming_url)

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Recently Played games widget is created and configured in CMS > Sports Pages > Homepage > Recently Played Games;
        DESCRIPTION: 2. Recently Played games widget is active in CMS;
        """
        rpg_cms_module = self.cms_config.get_sport_module(sport_id=0, module_type='RECENTLY_PLAYED_GAMES')[0]
        if rpg_cms_module.get('disabled'):
            rpg_cms_module = self.cms_config.update_recently_played_games(disabled=False)

        self.__class__.expected_rpg_title = rpg_cms_module.get('rpgConfig').get('title').upper()

        # below three variables are for the validation and configuration of See More Link in CMS
        self.__class__.cms_gaming_url = rpg_cms_module['rpgConfig']['seeMoreLink']
        self.__class__.expected_gaming_url = tests.settings.gaming_url
        self.__class__.gaming_url_mismatch = self.cms_gaming_url != self.expected_gaming_url

        if self.gaming_url_mismatch:
            self.cms_config.update_recently_played_games(seeMoreLink=self.expected_gaming_url)

        self.__class__.games_amount = rpg_cms_module['rpgConfig']['gamesAmount']

        username = tests.settings.recently_played_games_user
        self.site.login(username=username)
        self.site.wait_content_state('HomePage')

        # with the help of belwo request, We will get the list of games that the current user has played, i.e. Receltly Played Games.
        rpg_url = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames'
        rpg_headers = {
            "Content-Type": "application/json"
        }
        rpg_payload = {
            "accountName": f"ld_{username}" if self.brand == 'ladbrokes' else f"cl_{username}",
            "productId": "CASINO",
            "brandId": "LADBROKEUK" if self.brand == 'ladbrokes' else "CORAL",
            "feId": "ld" if self.brand == 'ladbrokes' else "cl",
            "channelId": "AW",
            "lang": "en_US",
            "noofgames": 10,
            "lobbyType": "instantCasino",
            "reqSource": "LCG_SPORTS"
        }
        # Convert the data to JSON format
        rpg_json_payload = json.dumps(rpg_payload)

        # Make the POST request
        rpg_response = requests.post(rpg_url, headers=rpg_headers, data=rpg_json_payload)

        # Check the response status code and print the response content
        if rpg_response.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            rpg_response_dict = json.loads(rpg_response.content)
            self.__class__.user_played_games_list = [item["displayname"].upper() for item in rpg_response_dict["games"]]
            self.assertTrue(self.user_played_games_list,
                            msg=f'game is not available in response: {self.user_played_games_list}')
        else:
            raise Exception(f'current url: {rpg_url} is sending status code: {rpg_response.status_code}')


        # with the help of below request, We will get the list of games that the user might like, i.e. Games You Might Like (GYML).
        gyml_url = "https://scmedia.itsfogo.com/$-$/aecf2c358b6d45cd8b191dd0590d06bf.json"
        gyml_headers = {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
        }

        # Make the GET request
        gyml_response = requests.get(url=gyml_url, headers=gyml_headers)

        # Check the response status code and print the response content
        if gyml_response.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            gyml_response_dict = json.loads(gyml_response.content)
            self.__class__.games_you_might_like_data = [item['name'].upper() for item in gyml_response_dict['gamelist']]
            self.assertTrue(self.games_you_might_like_data,
                            msg=f'game is not available in response: {self.games_you_might_like_data}')
        else:
            raise Exception(f'current url: {gyml_url} is sending status code: {gyml_response.status_code}')

    def test_001_launch_the_application_amp_navigate_to_homepage(self):
        """
        DESCRIPTION: Launch the application &amp; Navigate to Homepage.
        EXPECTED: User should be able to launch the app should be see the Homepage is loaded successfully.
        """
        # covered in preconditions
        pass

    def test_002_log_into_the_application_with_the_user_who_visited_casinoand_played_atleast_one_game_recently(self):
        """
        DESCRIPTION: Log into the application with the user who visited casino
        DESCRIPTION: and played atleast one game recently.
        EXPECTED: User is logged in &amp; user is able to see RPG/GYML Module
        """
        # covered in preconditions
        pass

    def test_003_verify_the_recently_played_gamesgames_you_might_like_module_is_displayed_in_carousel_form(self):
        """
        DESCRIPTION: Verify the Recently Played Games/Games You Might Like module is displayed in carousel form.
        EXPECTED: User should be able to see module displays in Carousel form which consists of the games that user recently played &amp; Other Games that user may like.
        """
        is_recently_played_games_displayed = wait_for_result(lambda: self.site.recently_played_games.is_displayed())
        self.assertTrue(is_recently_played_games_displayed,
                        msg='Recently Played Games Widget is not displayed!')
        self.assertEqual(self.site.recently_played_games.rpg_title.upper(), self.expected_rpg_title,
                         msg=f'Recently Played Games not as expected title{self.expected_rpg_title}')

    def test_004_verify_the_scrolling_of_rpggyml_carousel(self):
        """
        DESCRIPTION: Verify the scrolling of RPG/GYML carousel.
        EXPECTED: User should be able to smooth scroll in the carousel.
        """
        games = self.site.recently_played_games.items_as_ordered_dict
        self.assertTrue(games, msg='No games found in RPG module!')

        # getting all the titles of games in RPG module
        self.__class__.games_titles_frontend = [item.strip().upper() for item in self.site.recently_played_games.get_all_game_titles]

        # verifying if the first game is visible or not by default
        first_game_name, first_game = list(games.items())[0]
        self.assertEqual(first_game.title.upper(), self.games_titles_frontend[0], msg=f'even after scrolling to the first game: {first_game.title}, it is not displaying as expected: {self.games_titles_frontend[0]}')

        # scrolling to the last element and verifying if the last game is visible or not
        last_game_name, last_game = list(games.items())[-1]
        last_game.scroll_to_we()
        self.assertEqual(last_game.title.upper(), self.games_titles_frontend[-1], msg='even after scrolling to the last game, it is not displaying as expected')

    def test_005_validate_the_count_of_games_in_the_carousel(self):
        """
        DESCRIPTION: Validate the count of games in the Carousel
        EXPECTED: User should be able to see the total number of games is matched with 'Games Count' which is configued in the CMS
        EXPECTED: Note:
        EXPECTED: * If Game count is set as 10
        EXPECTED: 10 games are displayed in the carousel
        EXPECTED: If user played 4 casino games recently then the above 10 games are aligned in the form of 4 recently played games followed by other games that user may like
        EXPECTED: *If Game count is set as 5
        EXPECTED: 5 games are displayed in the carousel
        EXPECTED: If user played 5 casino games recently then the above 5 games are aligned only with 5 recently played games
        """
        # In the RPG(Recently Played Games) Module, both "Recently Played Games"(RPG) and "Games You Might Like"(GYML) data together are displayed.
        # The data we get from CMS for "games amount" is only specific to RPG.
        # In some cases, the user might have played only a limited number of games in casino.
        # but the "games amount" set in CMS can be higher, so we are using less than or equal assertion.
        self.assertLessEqual(len(self.user_played_games_list), self.games_amount, msg=f"number of visible recently played games in FE is not equal to configured amount that is {self.games_amount}")

    def test_006_verify_the_game_name_in_the_carousel(self):
        """
        DESCRIPTION: Verify the game name in the carousel
        EXPECTED: * If game name has one line of characters then the label/game name is displayed within one line under the image of game
        EXPECTED: *  If game name has two lines of characters then the label/game name is displayed within two lines under the image of game
        EXPECTED: * If game name exceeds two lines of characters then the label/game name is displayed within two lines under the image of game even though the game name is more than two lines
        EXPECTED: And ellipses comes into the picture means three dots are shown at the end of second line
        """
        for user_played_game in self.user_played_games_list:
            self.assertIn(user_played_game, self.games_titles_frontend,
                          msg=f'the user has already played the game {user_played_game}, but not displaying in FE')
            self.games_titles_frontend.remove(user_played_game)

        for game in self.games_titles_frontend:
            self.assertIn(game, self.games_you_might_like_data,
                          msg='games you might like data not matching from response and FE')

    def test_007_click_on_any_of_the_thumbnail_image(self):
        """
        DESCRIPTION: Click on any of the thumbnail image.
        EXPECTED: User should be able to navigate to the specific
        EXPECTED: gaming page.
        """
        games = self.site.recently_played_games.items_as_ordered_dict
        self.assertTrue(games, msg='No games found in RPG module!')

        first_game_name, first_game = list(games.items())[0]
        expected_url_part = f'gameVariantName={first_game_name}'
        first_game.click()
        result = wait_for_result(lambda: expected_url_part in self.device.get_current_url(),
                                 name='Game to open')
        self.assertTrue(result,
                        msg=f'User is redirected to the wrong page: "{expected_url_part}"'
                            f' not found in URL: "{self.device.get_current_url()}"')

        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('HomePage')

    def test_008_navigate_to_hompage_gt_module_order_gt_recently_played_games_module__gt_disable_the_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Navigate to Hompage-&gt; Module Order-&gt; 'Recently Played Games Module' -&gt;
         Disable the Active checkbox and save changes
        EXPECTED: Changes are saved successfully
        """
        self.cms_config.update_recently_played_games(disabled=True)

    def test_009_navigate_to_homepage_amp_refresh_the_page(self):
        """
        DESCRIPTION: Navigate to Homepage &amp; refresh the page
        EXPECTED: Homepage is loaded successfully
        EXPECTED: And RPG/GYML module is not displayed
        """
        recently_played_games_module = wait_for_cms_reflection(lambda: self.site.recently_played_games.is_displayed(),
                                                               timeout=3, ref=self, haul=3, expected_result=False)
        self.assertFalse(recently_played_games_module,
                         msg="recentely played games is still displaying even after disabling it in CMS")

    def test_010_navigate_to_hompage_gt_module_order_gt_recently_playedgames_module__gt_enable_the_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Navigate to Hompage-&gt; Module Order-&gt; 'Recently Played
        DESCRIPTION: Games Module' -&gt; Enable the Active checkbox and save changes
        EXPECTED: Changes are saved successfully
        """
        self.cms_config.update_recently_played_games(disabled=False)

    def test_011_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: Homepage is loaded successfully
        EXPECTED: And RPG/GYML module is also loaded with games
        """
        recently_played_games_module = wait_for_cms_reflection(lambda: self.site.recently_played_games.is_displayed(),
                                                               timeout=3, ref=self, haul=3, expected_result=True)
        self.assertTrue(recently_played_games_module,
                        msg="recentely played games is not displaying even after enabling it in CMS")

    def test_012_verify_see_all_gaming_link_is_displaying_below_the_thumbnails(self):
        """
        DESCRIPTION: Verify 'See All Gaming' link is displaying below the thumbnails.
        EXPECTED: user should be able to see the 'See All Gaming'
        EXPECTED: link below the thumbnails.
        """
        see_all_gaming_link = self.site.recently_played_games.see_more.is_displayed()
        self.assertTrue(see_all_gaming_link, msg="'See All Gaming' link is displayed in FE")

        actual_see_all_title = self.site.recently_played_games.see_more.text
        expected_see_all_title = 'See All Gaming'

        self.assertEqual(actual_see_all_title, expected_see_all_title, msg=f'actual see all title: {actual_see_all_title}'
                                                                           f' is not matching with expected see all title: {expected_see_all_title}')

        order_of_elements_of_rpg = self.site.recently_played_games.order_of_elements_inside_recently_played_games()
        self.assertTrue(order_of_elements_of_rpg.get('title')
                        < order_of_elements_of_rpg.get('rpg-carousel-thumbnails')
                        < order_of_elements_of_rpg.get('see-all-gaming-link'),
                        msg='Elements are not in the expected order, the expected order of elements is: '
                            'title, rpg-carousel-container, See All Gaming link')

    def test_013_click_on_see_all_gaming_link(self):
        """
        DESCRIPTION: Click on 'See All Gaming' link.
        EXPECTED: User should be able to navigate gaming page.
        """
        self.site.recently_played_games.see_more.click()
        self.assertEqual(self.expected_gaming_url, self.device.get_current_url(),
                         msg=f'User is redirected to the wrong page: "{self.device.get_current_url()}", '
                             f''f'expected is: "{self.expected_gaming_url}"')
        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('HomePage')

    def test_014_verify_the_recently_played_gamesgames_you_mightlikerpggyml_module_in_the_homepage(self):
        """
        DESCRIPTION: Verify the Recently Played Games/Games You Might
        DESCRIPTION: Like(RPG/GYML) module in the homepage
        EXPECTED: RPG/GYML module is not displayed&Acirc;&nbsp;&Acirc;&nbsp;when user is not logged in
        """
        self.site.logout()
        is_recently_played_games_displayed = self.site.has_recently_played_games(expected_result=False, timeout=3)
        self.assertFalse(is_recently_played_games_displayed,
                        msg='Recently Played Games Widget is not displayed!')

    def test_015_log_into_the_application_with_the_user_who_never_played_any_casino_games(self):
        """
        DESCRIPTION: Log into the application with the user who never played any Casino games
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_016_verify_the_recently_played_gamesgames_you_mightlikerpggyml_module_in_the_homepage(self):
        """
        DESCRIPTION: Verify the Recently Played Games/Games You Might
        DESCRIPTION: Like(RPG/GYML) module in the homepage
        EXPECTED: RPG/GYML module is not displayed
        """
        is_recently_played_games_displayed = self.site.has_recently_played_games(expected_result=False, timeout=3)
        self.assertFalse(is_recently_played_games_displayed,
                         msg='Recently Played Games Widget is not displayed!')
