import pytest
import tests
import datetime as dt
from voltron.utils.helpers import get_response_url
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.helpers import do_request
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.adhoc_suite
@pytest.mark.module_ribbon
@pytest.mark.one_two_free
@pytest.mark.responsible_gambler_yellow
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C65940568_MRT__Verify_the_1_2_free_tab_display_and_navigationLads_for_RGY_and_Non_RGY_user(Common):
    """
    TR_ID: C65940568
    NAME: MRT - Verify the 1-2-free tab display and navigation(Lads) for RGY and Non-RGY user
    DESCRIPTION: This test case is to verify the 1-2-free tab display and navigation for RGY and Non-RGY user
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    one_two_free_title = vec.bma.OTF_PAGE_TITLE
    one_two_free_config = {
        'title': one_two_free_title.upper(),
        'directive_name': 'Featured',
        'visible': True,
        'internal_id': one_two_free_title.lower(),
        'devices_android': True,
        'devices_ios': True,
        'devices_wp': True,
        'url': '1-2-free',
        'show_tabs_on': 'both',
    }

    def verify_and_create_one_two_free_game(self):
        """
        Verify and if no active One-Two Free game is available then create a One-Two Free game.
        Create the Season, Gamification, Game View in CMS if none of them are available.
        raises: SiteServeException if there's no event data available for English Premier League football.
        param : no mandatory arguments are needed to be sent.
        """

        def create_game(active_season):
            """
            Retrieves a complete URL from the performance log,
            and make a get request to that URL to Retrieves event data for English Premier League football events.
            Then Creates the Game View and Adds predictions to the game view with the help of event data.
            and enables the game view status to active.
            """
            game_response = self.cms_config.create_gameView(active_season.get('id'))
            game_id = game_response.get('id')
            self.navigate_to_page('/competitions/football/english/premier-league', timeout=10)
            event_to_outcome_response = get_response_url(self,
                                        url='EventToOutcomeForType/442?simpleFilter=event.eventSortCode:notIntersects')
            sportsbook_api_response = do_request(method='GET',
                                                 url=event_to_outcome_response.rstrip('childCount=event')[:-1])[
                "SSResponse"]["children"]
            if not event_to_outcome_response:
                raise SiteServeException('No event data available for english premier league for football sport')
            english_premier_league_event_id_list = []
            for event_data in sportsbook_api_response:
                try:
                    event_id = event_data['event']['id']
                    english_premier_league_event_id_list.append(event_id)
                except KeyError:
                    continue
            self.cms_config.add_prediction_to_game_view(game_id, english_premier_league_event_id_list)
            self.cms_config.update_game_view_status(game_id, enabled=True)

        season_created_flag = False
        # Checks for an active season based on display dates.
        getSeasons = self.cms_config.get_seasons()
        active_season = next((season for season in getSeasons if
                              season.get(
                                  'displayFrom') <= dt.datetime.utcnow().isoformat() <= season.get(
                                  'displayTo')), None)
        # If no active season is found, creates a new season.
        if not active_season:
            inactive_season = next((season for season in getSeasons if
                                    (int(season.get('displayFrom').split("-")[2].split('T')[
                                             0]) <= dt.datetime.utcnow().day <= int(
                                        season.get('displayTo').split("-")[2].split('T')[0])) and
                                    (int(season.get('displayFrom').split("-")[
                                             1]) <= dt.datetime.utcnow().month <= int(
                                        season.get('displayTo').split("-")[1]))),
                                   None)
            # Handles inactive seasons by deleting associated gamification and the season itself.
            if inactive_season:
                if inactive_season.get('gamificationLinked'):
                    get_gamification = self.cms_config.get_gamification()
                    inactive_gamification = next((gamification for gamification in get_gamification if
                                                  gamification.get('seasonName') == inactive_season.get(
                                                      'seasonName')), None)
                    self.cms_config.delete_gamification(inactive_gamification.get('id'))
                self.cms_config.delete_season(inactive_season.get('id'))
            active_season = self.cms_config.create_season()
            season_created_flag = True

        # Checks for active gamification for the active season.
        get_gamification = self.cms_config.get_gamification()
        active_gamification = next((gamification for gamification in get_gamification if
                                    gamification.get('seasonId') == active_season.get('id') and
                                    gamification.get('displayFrom') <= dt.datetime.utcnow().isoformat() <=
                                    gamification.get('displayTo')), None)

        # Creates gamification if it doesn't exist for the active season.
        if not active_gamification and season_created_flag:
            active_gamification = self.cms_config.create_gamification(active_season.get('id'))
        # Updates the active season.
        if season_created_flag and active_gamification:
            self.cms_config.update_season(active_season)

        # Retrieve a list of all available 1-2-Free games from the CMS.
        get_games = self.cms_config.get_games()
        # Find the active game by iterating through the list and checking if it is enabled and within its display date range.
        active_games = []
        for game in get_games:
            if game.get('enabled') is True and game.get('displayFrom') <= dt.datetime.utcnow().isoformat() <= game.get('displayTo'):
                active_games.append(game)

        active_game_with_active_season = next((game for game in active_games if game['seasonId'] == active_season.get('id')), None)

        if not active_game_with_active_season:
            for game in active_games:
                self.cms_config.update_game_view_status(gameId=game.get('id'), enabled=False)
            create_game(active_season=active_season)

    def is_rgy_module_in_bonus_suppression_module(self, rgy_module, rgy_bonus_suppression_module):
        """
        Check if the 'rgy_module' exists within 'rgy_bonus_suppression_module'.

        Args:
            rgy_module (dict): The module to search for.
            rgy_bonus_suppression_module (dict): The bonus suppression module to search within.

        Returns:
            dict or None: If found, returns the matching module, otherwise returns None.
        """
        rgy_module_id = rgy_module['id']
        all_module = rgy_bonus_suppression_module['modules']
        for module in all_module:
            if rgy_module_id == module['id']:
                return module

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
        PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
        PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
        PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
        PRECONDITIONS: -Module ribbon tab title
        PRECONDITIONS: -Directive name option from dropdown like Featured, Coupon,In-play, Live stream,Multiples, next races, top bets, Build your bet
        PRECONDITIONS: -id - 1-2-free
        PRECONDITIONS: -URL - 1-2-free
        PRECONDITIONS: -Click on "Create" CTA button
        PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
        PRECONDITIONS: -Active
        PRECONDITIONS: -IOS
        PRECONDITIONS: -Android
        PRECONDITIONS: -Windows Phone
        PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
        PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
        PRECONDITIONS: -Click on "Save changes" button
        PRECONDITIONS: 6)Navigate to Bonus supression from left menu in main navigation.Able to  see two sub sections
        PRECONDITIONS: -Modules
        PRECONDITIONS: -Configuration
        PRECONDITIONS: Modules - Click on Add Module and enter all required Fields:
        PRECONDITIONS: -Module Name            - 1-2-Free
        PRECONDITIONS: -Alias Module Names - One-Two-Free
        PRECONDITIONS: -Click on Save button
        PRECONDITIONS: Configuration - Click on Problem Gambler Low Risk Level and Add created Module.
        """
        # RGY USER = 'Responsible Gambler Yellow User'
        # These users are given Yellow Flag as they did not follow gambling rules,
        # Due to which they are restricted from few of the functionalities such as '1-2-FREE'

        # Set risk level and reason code constants
        risk_level = self.cms_config.constants.BONUS_SUPPRESSION_RISK_LEVEL.risk_level_one
        reason_code = self.cms_config.constants.BONUS_SUPPRESSION_REASON_CODE.reason_code_one

        # Verify and create the 'one_two_free_game'
        self.verify_and_create_one_two_free_game()

        one_two_free_my_badges = self.cms_config.get_one_two_free_my_badges()
        if not one_two_free_my_badges['viewBadges'] or not one_two_free_my_badges['lastUpdatedFlag']:
            self.cms_config.update_one_two_free_my_badges(viewBadges=True, lastUpdatedFlag=True)

        if self.device_type == 'mobile':
            # For mobile devices, get module data by directive name
            module_ribbon_tab_data = self.get_module_data_by_directive_name_from_cms(directiveName='Featured',
                                                                                     expected_tab_display_name=self.one_two_free_title.upper())
            # If module data not found, create a new tab
            if not module_ribbon_tab_data:
                self.cms_config.module_ribbon_tabs.create_tab(**self.one_two_free_config)
        else:
            # For desktop, check if header submenu exists
            header_submenu_does_not_exists = True
            header_submenus = self.cms_config.get_header_submenus()
            for header_submenu in header_submenus:
                if (
                        header_submenu.get('linkTitle') == self.one_two_free_title.upper() and
                        header_submenu.get('disabled') == False and
                        header_submenu.get('targetUri') == self.one_two_free_title.lower() and
                        header_submenu.get('inApp') == True
                ):
                    header_submenu_does_not_exists = False
            if header_submenu_does_not_exists:
                # If header submenu doesn't exist, create it
                created_submenu = self.cms_config.create_header_submenu(name=self.one_two_free_title.upper(),
                                                                        target_url=self.one_two_free_title.lower())
                self.assertTrue(created_submenu, msg=f'the header sub-menu with name '
                                                     f'"{self.one_two_free_title.upper()}" is not  been created')

        # check if rgy module with alias exists
        rgy_module_with_alias = self.cms_config.get_rgy_module_with_alias(module_name=self.one_two_free_title.upper())
        #  If rgy module with alias doesn't exist, create rgy module
        if not rgy_module_with_alias:
            rgy_module_with_alias = self.cms_config.add_rgy_module(module_name=self.one_two_free_title.upper())

        # check if rgy bonus suppression module exists
        rgy_bonus_suppression_module = self.cms_config.get_rgy_bonus_suppression_module(
            risk_level=risk_level, reason_code=reason_code)
        #  If rgy bonus suppression module doesn't exist, create rgy bonus suppression module
        if not rgy_bonus_suppression_module:
            rgy_bonus_suppression_module = self.cms_config.add_rgy_bonus_suppression_module(
                risk_level=risk_level, reason_code=reason_code,
                bonus_suppression_enabled=True, rgy_module_ids=[rgy_module_with_alias['id']])

        # Check if rgy module('1-2-FREE') is in  rgy bonus suppression module
        is_rgy_module_in_bonus_suppression_module = self.is_rgy_module_in_bonus_suppression_module(
            rgy_module=rgy_module_with_alias, rgy_bonus_suppression_module=rgy_bonus_suppression_module)

        # If not in the module, update rgy bonus suppression module to include it
        if not is_rgy_module_in_bonus_suppression_module:
            self.cms_config.update_rgy_bonus_suppression_module(
                risk_level=risk_level, reason_code=reason_code,
                bonus_suppression_enabled=True, rgy_module_ids=[rgy_module_with_alias['id']])

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.navigate_to_page(name='/')

    def test_002_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on 1-2 Free tab
        EXPECTED: 1-2 Free splash page should be opened
        EXPECTED: For logged in user - 1-2-free page should be opened
        EXPECTED: For logged out user - "Login to play" and "Cancel" button should be displayed. User should click on "Login to play" button to Login to the application
        """
        if self.device_type == 'mobile':
            # Mobile specific
            # getting tabs in home page for mobile, then clicking on the module ribbon tab
            self.site.home.tabs_menu.items_as_ordered_dict.get(self.one_two_free_title.upper()).click()
        else:
            # Desktop specific
            # getting header tab in home page, then clicking on the sport menu
            self.site.header.sport_menu.items_as_ordered_dict.get(self.one_two_free_title.upper()).click()

        # Wait for the login dialog to appear within a 15-second timeout
        dialog = self.site._wait_for_login_dialog(15)
        self.assertTrue(dialog, '"Log In" pop-up is not displayed')
        # Close the login dialog
        dialog.close_dialog()

        # Ensure the "Log In" dialog is removed from the dialog manager
        self.assertFalse(vec.dialogs.DIALOG_MANAGER_LOG_IN in self.site.dialog_manager.items_as_ordered_dict,
                         msg='"Log In" dialog should not be displayed on the screen')

        self.assertTrue(self.site.one_two_free.login_to_play_button.is_displayed(),
                        msg='1-2-Free login to play is not shown')
        self.assertTrue(self.site.one_two_free.login_page_cancel_button.is_displayed(),
                        msg='1-2-Free login page cancel is not shown')

        self.site.one_two_free.login_to_play_button.click()
        # Wait for the "Log In" dialog to appear with a 10-second timeout
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(dialog, msg='"Log In" dialog is not shown')

        # Set the username and password in the "Log In" dialog
        dialog.username = tests.settings.betplacement_user
        dialog.password = tests.settings.default_password

        # Click the login button in the "Log In" dialog
        dialog.click_login()

        # Wait for the "Log In" dialog to be closed
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Failed to close Login dialog')

        # Wait for the "Odds Boost" dialog to appear
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        if dialog:
            # If the "Odds Boost" dialog appears, close it
            dialog.close_dialog()
            dialog.wait_dialog_closed()

        self.assertTrue(self.site.one_two_free.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')

        # For mobile devices, attempt to close the timeline splash page
        if self.device_type == "mobile":
            try:
                self.site.timeline.timeline_splash_page.close_button.click()
            except VoltronException:
                # Handle exceptions silently if the timeline splash page does not appear
                pass

    def test_003_click_on_play_here_cta_button(self):
        """
        DESCRIPTION: Click on "PLAY HERE CTA" Button
        EXPECTED: 1-2 Free page is loaded and  Three tabs can be seen(This week, Last week results, My badges)if game view is active
        """
        one_two_free = self.site.one_two_free
        if self.device_type == 'mobile':
            # If it's a mobile device, wait for the "PLAY HERE!" button to be displayed
            welcome_screen_play_here_button = wait_for_result(
                lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(), timeout=15)
            self.assertTrue(welcome_screen_play_here_button, msg='"PLAY HERE!" button is not available')

            # Click on the "PLAY HERE!" button
            one_two_free.one_two_free_welcome_screen.play_button.click()

        actual_tab_list = list(one_two_free.one_two_free_current_screen.tab_items.items_as_ordered_dict.keys())

        tab_name_configuration = self.cms_config.get_one_two_free_tab_name_configuration()
        self.__class__.current_tab_label = tab_name_configuration["currentTabLabel"].strip().upper()
        self.__class__.previous_tab_label = tab_name_configuration["previousTabLabel"].strip().upper()
        self.__class__.my_badges = self.cms_config.get_one_two_free_my_badges().get("label").strip().upper()

        expected_tabs_list = [self.current_tab_label, self.previous_tab_label, self.my_badges]
        # Compare the actual and expected 1-2-FREE tab lists
        self.assertListEqual(actual_tab_list, expected_tabs_list,
                             msg=f"Tabs present in 1-2 Free page {actual_tab_list} "
                                 f"is not as expected {expected_tabs_list}")

    def test_004_click_on_this_week_tab(self):
        """
        DESCRIPTION: Click on This week tab
        EXPECTED: Game view can be seen
        """
        one_two_free = self.site.one_two_free.one_two_free_current_screen

        current_active_tab_name = one_two_free.tab_items.current
        expected_active_tab_name = self.current_tab_label
        # Compare the actual and expected 1-2-FREE current active tab.
        self.assertEqual(current_active_tab_name, expected_active_tab_name,
                         msg=f"actual active tab {current_active_tab_name} is not as expected expected active tab {expected_active_tab_name} in 1-2 Free")

        # Process and validate match or prediction related information
        matches = list(one_two_free.items_as_ordered_dict.values())

        for match in matches:
            # Check if match start date is displayed for each match
            self.assertTrue(match.match_start_date,
                            msg=f'match start time is not displayed for "{match.name}".')
            for shirt in list(match.items_as_ordered_dict.values()):
                self.assertTrue(shirt.silk_icon.is_displayed(),
                                msg=f' Teams t-shirts not displayed for "{match.name}".')
                self.assertTrue(shirt.name,
                                msg=f'Team names not displayed for "{match.name}".')

            # Check various elements related to score switchers for each match
            score_switchers = match.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.decrease_score_down_arrow.is_displayed(),
                                msg=f'Down arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.score,
                                msg=f'Score is not displayed for "{match.name}".')

    def test_005_click_on_last_weel_results_tab(self):
        """
        DESCRIPTION: Click on Last weel Results tab
        EXPECTED: Able to see previous week game results
        """

        def has_did_not_play_game_label():
            """
            Check if the "You didn’t play 1-2-Free last weekend." label is displayed on the current screen.

            Returns:
                bool: True if the label is displayed, False otherwise.
            """
            return wait_for_result(
                lambda: self.site.one_two_free.one_two_free_current_screen.last_week_results.did_not_play_game_label ==
                        vec.onetwofree.DID_NOT_PLAY_LAST_WEEKEND, timeout=5
            )

        one_two_free = self.site.one_two_free.one_two_free_current_screen

        # clicking on "LAST WEEKS RESULTS" tab
        one_two_free.tab_items.items_as_ordered_dict.get(self.previous_tab_label).click()

        current_active_tab_name = one_two_free.tab_items.current
        expected_active_tab_name = self.previous_tab_label
        # Compare the actual and expected 1-2-FREE current active tab.
        self.assertEqual(current_active_tab_name, expected_active_tab_name,
                         msg=f"actual active tab {current_active_tab_name} is not as expected expected active tab {expected_active_tab_name} in 1-2 Free")

        if not has_did_not_play_game_label():
            # Process and validate predicted match related information
            matches = list(one_two_free.items_as_ordered_dict.values())

            # Validates if match number(example: 'MATCH 1'), match result(example: 'Result 2-1')
            # and match lost or won(example: 'LOST' or 'WON') are displayed for each match or not
            for match in matches:
                self.assertTrue(match.match_number,
                                msg=f'match start time is not displayed for "{match.name}".')
                self.assertTrue(match.match_result,
                                msg=f'match start time is not displayed for "{match.name}".')
                self.assertTrue(match.lost_or_won,
                                msg=f'match start time is not displayed for "{match.name}".')

                # validate if Teams t-shirts and Team names are displayed or not
                for shirt in list(match.items_as_ordered_dict.values()):
                    self.assertTrue(shirt.silk_icon.is_displayed(),
                                    msg=f' Teams t-shirts not displayed for "{match.name}".')
                    self.assertTrue(shirt.name,
                                    msg=f'Team names not displayed for "{match.name}".')

                # Check element related to score for each match
                scores = match.score_selector_container.items
                for score in scores:
                    self.assertTrue(score.my_prediction,
                                    msg=f'Score is not displayed for "{match.name}".')

    def test_006_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on My badges tab
        EXPECTED: Primary and Secondary badges can be seen
        """
        # complete validation of Primary and Secondary badges is covered in Test case C64895003
        one_two_free = self.site.one_two_free.one_two_free_current_screen

        # clicking on "MY BADGES" tab
        one_two_free.tab_items.items_as_ordered_dict.get(self.my_badges).click()

        current = one_two_free.tab_items.current

        # Compare the actual and expected 1-2-FREE current active tab.
        self.assertEqual(current, self.my_badges, msg=f'Actual tab: {current} is not same as'
                                                 f'Expected tab: {self.my_badges}')
        self.assertTrue(one_two_free.my_badges.my_badges_text,
                        msg="My Badges description is not displayed")

    def test_007_click_on_close_buttonx_at_top_right_corner(self):
        """
        DESCRIPTION: Click on close button('x') at top Right corner
        EXPECTED: It should navigate to home page
        """
        self.site.one_two_free.one_two_free_current_screen.close.click()
        self.site.wait_content_state('homepage')

    def test_008_login_to_application_with_rgy_user(self):
        """
        DESCRIPTION: Login to application with RGY user
        EXPECTED: User should be logged in successfully
        """
        self.site.logout()
        # Below User is a Responsible Gambler Yellow User
        # In the future if the user is not working change it with new RGY user.
        # We can get the users from the Manual Team Lead's for prod/beta environment.
        # For lower environments, please use the below link
        # https://localreports.ivycomptech.co.in/pls/new_stagingezecash/p_r_rg_update_allvrfn_details?in_user_id={brand_USERNAME}
        # Above brand_USERNAME = For Coral brand use, cl_USERNAME AND For Ladbrokes brand use, ld_USERNAME
        self.site.login(username='ganeshgunjal99', password='Sand1234')

    def test_009_verify_the_display_of_1_2_free(self):
        """
        DESCRIPTION: Verify the display of 1-2-Free
        EXPECTED: 1-2-Free should not display for RGY user
        """
        if self.device_type == 'mobile':
            # getting tabs in home page for mobile
            home_page_tabs = list(self.site.home.tabs_menu.items_as_ordered_dict.keys())
        else:
            # Desktop specific
            home_page_tabs = list(self.site.header.sport_menu.items_as_ordered_dict.keys())
        home_page_tabs = [tab.upper() for tab in home_page_tabs]
        self.assertNotIn(self.one_two_free_title.upper(), home_page_tabs,
                         msg=f'Actual module ribbon tab {self.one_two_free_title.upper()} should not be displayed in home page module ribbon tabs list {home_page_tabs}')
