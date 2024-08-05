import pytest
import tests
import datetime as dt
from tzlocal import get_localzone
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul, wait_for_result, wait_for_cms_reflection
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.mobile_only
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.one_two_free
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.timeout(700)
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C65934240_Verify_behavior_of_special_super_button_and_super_button_for_1_2_Free_predicted_customer(Common):
    """
    TR_ID: C65934240
    NAME: Verify behavior of special super button and super button for 1-2 Free predicted customer
    DESCRIPTION: To validate the display of super button and special super button for 1-2 Free predicted user.
    PRECONDITIONS: 1-2 Free game view should be configured in CMS and running.
    PRECONDITIONS: Special Super button should be configured in CMS and in running state.
    PRECONDITIONS: 1-2 Free prediction already done by the customer.
    PRECONDITIONS: Super button should be configured in CMS and in running state.
    PRECONDITIONS: Select home tabs (ex: Highlights, World cup) to display Super button
    PRECONDITIONS: Note- 1. Special super button is only applicable for Ladbrokes
    PRECONDITIONS: 2. Refer Test case C65934239 for Creating special super button and to predict 1-2 Free game through it.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    faker = Faker()
    competition_name = f'Auto big competition sb{faker.city()}'
    new_id = faker.random.randint(200, 1000)
    timezone = str(get_localzone())
    disabled_special_super_buttons =[]

    def verify_and_create_one_two_free_game(self):
        """
        Verify and if no active One-Two Free game is available then create a One-Two Free game.
        Create the Season, Gamification, Game View in CMS if none of them are available.
        raises: SiteServeException if there's no event data available for English Premier League football.
        param : no mandatory arguments are needed to be sent.
        """
        def get_response_url(url):
            """
            :param url: Required URl
            :return: Complete url
            """
            perflog = self.device.get_performance_log()
            for log in list(reversed(perflog)):
                try:
                    data_dict = log[1]['message']['message']['params']['request']
                    request_url = data_dict['url']
                    if url in request_url:
                        self.count = + 1
                        return request_url
                except (KeyError, JSONDecodeError, TypeError, IndexError):
                    continue
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
            event_to_outcome_response = get_response_url(
                'EventToOutcomeForType/442?simpleFilter=event.eventSortCode:notIntersects')
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
            game_response = self.cms_config.update_game_view_status(game_id, enabled=True)

        season_created_flag = False
        # Retrieve a list of all available 1-2-Free games from the CMS.
        get_games = self.cms_config.get_games()
        # Find the active game by iterating through the list and checking if it is enabled and within its display date range.
        self.__class__.active_game = next((game for game in get_games if
                                           game.get('enabled') is True and game.get('displayFrom') <= dt.datetime.utcnow().isoformat() <= game.get('displayTo')), None)
        if not self.active_game:
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
                                         0]) <= dt.datetime.utcnow().day <= int(season.get('displayTo').split("-")[2].split('T')[0])) and
                                        (int(season.get('displayFrom').split("-")[1]) <= dt.datetime.utcnow().month <= int(season.get('displayTo').split("-")[1]))),
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
            self.__class__.active_gamification = next((gamification for gamification in get_gamification if
                                                       gamification.get('seasonName') == active_season.get('seasonName') and
                                                       gamification.get('displayFrom') <= dt.datetime.utcnow().isoformat() <= gamification.get('displayTo')), None)
            #  if a new season is not created and no active gamification is present then raise CMSException.
            if not season_created_flag and not self.active_gamification:
                raise CMSException("There is already active season.So gamification cannot be created")
            # Creates gamification if it doesn't exist for the active season.
            if not self.active_gamification and season_created_flag:
                self.active_gamification = self.cms_config.create_gamification(active_season.get('id'))
            # Updates the active season.
            if season_created_flag and self.active_gamification:
                self.cms_config.update_season(active_season)

            create_game(active_season=active_season)

    def create_big_competition_and_sport_category(self, type_id):

        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=type_id, competition_name=self.competition_name)
        # Assign IDs and URIs from the new competition data
        self.__class__.new_competition_id = f"{new_competition.get('id')}"
        self.__class__.new_competition_uri = new_competition.get('uri')
        # Construct the URL for the new category
        new_category_ulr = f'big-competition{self.new_competition_uri}'
        # Create a new tab under the created Big competition
        new_tab_id = self.cms_config.create_tab_for_big_competition(competition_id=self.new_competition_id,
                                                                    tab_name='highlight').get('id')
        # Wait for a short time
        wait_for_haul(2)

        # Create a new module under the previously created big competition tab.
        # This module is necessary to house the super button for the big competition.
        # The super button will be positioned on top of this module.
        self.cms_config.create_module_for_big_competation(competition_id=self.new_competition_id,
                                                          tab_id=new_tab_id, module_name='surfaceBet',
                                                          module_type='SURFACEBET')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new sport category for the Big competition which is created
        self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                              ssCategoryCode=self.new_id, targetUri=new_category_ulr,
                                              tier='UNTIED', showInAZ=True, showInHome=True)

    def create_eventhub_and_add_it_to_sport_module_and_featured_tab(self, event_id):


        # Retrieve all existing event hubs from the CMS configuration.
        existing_event_hubs = self.cms_config.get_event_hubs()

        # maximum number of allowed eventhub is 6
        if len(existing_event_hubs) >= 6:
            # Get all module ribbon tabs
            all_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data

            # Filter inactive EventHub tabs using list comprehension
            all_inactive_eventhub_ids = [
                tab['internalId'].replace('tab-eventhub-', '')
                for tab in all_module_ribbon_tabs
                if tab.get('directiveName') == 'EventHub'
                   and (not tab.get('visible')
                   or dt.datetime.utcnow().isoformat() > tab.get('displayTo'))
            ]

            # Delete inactive EventHub modules
            for tab in existing_event_hubs:
                if str(tab.get('indexNumber')) in all_inactive_eventhub_ids:
                    self.cms_config.delete_event_hub_module(tab.get('id'))
                    break

        # Retrieve existing event hubs from the CMS configuration.
        existing_event_hubs = self.cms_config.get_event_hubs()

        # Extract the index numbers of existing event hubs.
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # Find the next available index number (from 1 to 19) that is not already in use.
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)

        # Create a new event hub with the determined index number.
        self.cms_config.create_event_hub(index_number=self.index_number)

        # Add a sport module of type 'FEATURED' to the event hub.
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')

        # Add a featured tab module to the event hub, specifying various parameters.
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=event_id,
                                                              page_type='eventhub',
                                                              page_id=self.index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)

        # Set the module name to the uppercase version of its title.
        self.__class__.module_name = module_data['title'].upper()

        # Define an internal ID for the event hub tab.
        internal_id = f'tab-eventhub-{self.index_number}'

        # Create a tab for the event hub in module ribbon tabs with specified details.
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=self.index_number,
                                                                           display_date=True)

        # Set the event hub tab name to the uppercase version of its title.
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def validate_super_button(self, page_content, special_super_button=False):

        configured_data = self.created_special_super_button if special_super_button else self.created_super_button
        if page_content == 'home':
            wait_for_cms_reflection(
                lambda: self.site.home.super_button_section.super_button.button.name.upper() == configured_data[
                    'title'].upper(), ref=self)
            page_content = self.site.home
        else:
            wait_for_cms_reflection(
                lambda: self.site.big_competitions.super_button_section.super_button.button.name.upper() ==
                        configured_data['title'].upper(), ref=self)
            page_content = self.site.big_competitions
        self.assertTrue(page_content.super_button_section.super_button.has_button,
                        msg='Super button is not displayed')

        expected_title = configured_data['title'].upper()
        actual_title = page_content.super_button_section.super_button.button.name.upper()
        self.assertEqual(actual_title, expected_title,
                         msg=f'Actual button name "{actual_title}" is not same as '
                             f'Expected button name {expected_title}')

        expected_description = configured_data['description'].upper()
        actual_description = page_content.super_button_section.super_button.description.upper()
        self.assertEqual(actual_description, expected_description,
                         msg=f'Actual button description "{actual_description}" is not same as '
                             f'Expected button description {expected_description}')
        if not special_super_button:
            expected_theme = configured_data['themes'].replace('_', '').upper()
            actual_theme = page_content.super_button_section.super_button.get_attribute('class').upper()
            self.assertIn(expected_theme, actual_theme,
                          msg=f'Actual button theme "{actual_theme}" is not same as '
                              f'Expected button theme {expected_theme}')

            expected_alignment = configured_data['ctaAlignment'].upper()
            actual_alignment = page_content.super_button_section.cta_alignment.upper()
            self.assertIn(actual_alignment, expected_alignment,
                          msg=f'Actual alignment "{actual_alignment}" is not in '
                              f'Expected alignment {expected_alignment}')

    def disable_all_other_super_buttons(self, home_tab=""):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        all_special_super_buttons = self.cms_config.get_mobile_special_super_buttons()
        for super_button in all_special_super_buttons:
            all_super_buttons.append(super_button)
        for supper_button in all_super_buttons:
            if supper_button.get('enabled') and home_tab in supper_button.get('homeTabs'):
                if self.timezone.upper() == "UTC":
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False)[:-3] + 'Z'
                elif self.timezone.upper() == 'EUROPE/LONDON':
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False, hours=-1)[:-3] + 'Z'
                else:
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False, hours=-5.5)[:-3] + 'Z'
                if not (supper_button.get('validityPeriodStart') <= now <= supper_button.get('validityPeriodEnd')):
                    continue
                if supper_button.get('featureTag'):
                    self.cms_config.update_mobile_special_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_special_super_buttons.append(supper_button.get('title'))
                else:
                    self.cms_config.update_mobile_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_super_buttons.append(supper_button.get('title'))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Super Button creation
        DESCRIPTION: Special Super Button creation
        """
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            event_id = event['event']['id']
            type_id = event['event']['typeId']
        else:
            # Add a new football event to the England Premier League and Assign event ID based on the added event
            event = self.ob_config.add_football_event_to_england_premier_league()
            event_id = event.event_id
            type_id = event.ss_response['event']['typeId']

        self.verify_and_create_one_two_free_game()

        self.create_big_competition_and_sport_category(type_id=type_id)

        self.create_eventhub_and_add_it_to_sport_module_and_featured_tab(event_id=event_id)

        wait_for_haul(10)
        home_tab_1 = f"/home/eventhub/{self.index_number}"
        self.disable_all_other_super_buttons(home_tab=home_tab_1)

        home_tab_2 = f"/home/eventhub/{self.index_number}"
        self.disable_all_other_super_buttons(home_tab=home_tab_2)
        wait_for_haul(10)

        # creating super button
        super_button_config = {
            'name': "super_button_C65934240",
            'competition_id': [self.new_competition_id],
            'target_uri': '/1-2-free',
            'category_id': [],
            'home_tabs': [f"/home/eventhub/{self.index_number}"]
        }
        self.__class__.created_super_button = self.cms_config.add_mobile_super_button(**super_button_config)

        # creating special super button
        special_super_button_config = {
            'name': "special_SButton_C65934240",
            'competition_id': [self.new_competition_id],
            'target_uri': '/1-2-free',
            'category_id': [],
            'home_tabs': [f"/home/eventhub/{self.index_number}"]
        }
        self.__class__.created_special_super_button = self.cms_config.add_mobile_special_super_button(
            **special_super_button_config)
        wait_for_haul(10)

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues.
        EXPECTED: By default home/featured tab should be loaded
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: Verify newly created Super button on Home page (FE).
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config.
        EXPECTED: Super button will not be displayed If current date and time is before the configured start date and time.
        EXPECTED: Special super button should not displayed.
        """
        self.validate_super_button(page_content='home')

    def test_003_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_004_verify_special_super_button_displaying_in_fe(self):
        """
        DESCRIPTION: Verify Special super button displaying in FE
        EXPECTED: Only Special super button should be displayed by default post login.
        EXPECTED: Super button should not be displayed now .
        """
        self.navigate_to_page(f'/big-competition{self.new_competition_uri}')
        self.validate_super_button(page_content='big_competitions', special_super_button=True)

    def test_005_verify_special_super_button_displaying_on__home_tabs(self):
        """
        DESCRIPTION: Verify Special super button displaying on  Home tabs
        EXPECTED: Special super button should be displayed on Home tabs as per CMS config
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        self.validate_super_button(page_content='home', special_super_button=True)

    def test_006_verify_the_navigating__url_of_special_super_button_after_clicking_on_it(self):
        """
        DESCRIPTION: Verify the navigating  URL of Special super button after clicking on it
        EXPECTED: Special super button should navigate to the url which is configured in CMS as Destination url
        """
        # click on super button
        self.site.home.super_button_section.super_button.button.click()
        wait_for_haul(5)
        # getting the current URL
        actual_super_button_url = self.device.get_current_url()
        expected_super_button_url = self.created_special_super_button['targetUri']
        self.assertIn(expected_super_button_url, actual_super_button_url,
                      msg=f'Current url: "{actual_super_button_url}" is not the same as expected: "{expected_super_button_url}"')

    def test_008_verify_1_2_free_game_page_as_per_cms_config(self):
        """
        DESCRIPTION: Verify 1-2-Free game page as per CMS config
        EXPECTED: 1-2-Free game page should be navigate and can see teams to add prediction of scores
        """
        if self.device_type == 'mobile':
            one_two_free = self.site.one_two_free

            # Wait for the 'play_button' on the welcome screen to be displayed and then click it
            wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed())
            one_two_free.one_two_free_welcome_screen.play_button.click()

            # Wait for the 'submit_button' on the current screen to be enabled within a timeout of 15 seconds and
            # Ensure that the 'submit_button' is active
            submit_button = wait_for_result(lambda: one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                expected_result=True), timeout=15)
            self.assertTrue(submit_button, msg='"Submit Button" is not active')

            # Check if the 'close' button on the current screen is displayed
            self.assertTrue(one_two_free.one_two_free_current_screen.close.is_displayed(),
                            msg='Close button not displayed on one two free')

            # Process and validate match or prediction related information
            matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
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

    def test_009_verify_prediction_is_happening_in_1_2_free_game_page(self):
        """
        DESCRIPTION: Verify Prediction is happening in 1-2-Free game page
        EXPECTED: Should be able to submit the predictions in the 1-2-Free game page
        """
        if self.device_type == 'mobile':
            self.__class__.one_two_free = self.site.one_two_free
            wait_for_result(lambda:
                            self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                expected_result=True),
                            timeout=15)
            match = list(self.one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
            for score in match:
                score_switchers = score.score_selector_container.items
                for score_switcher in score_switchers:
                    self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                    msg=f'Upper arrow not displayed for "{score.name}".')
                    score_switcher.increase_score_up_arrow.click()
                    wait_for_haul(1)
                    actual_score = score_switcher.score
                    self.assertEqual(actual_score, '1',
                                     msg=f'Actual Score "{actual_score}" is not the same as expected "1"')
                    break

            submit_button = self.one_two_free.one_two_free_current_screen.submit_button
            self.assertTrue(submit_button, msg='"Submit Button" is not active')
            submit_button.click()

    def test_010_verify_the_close_link_by_clicking_on_x_mark_on_top_right_after_submitting_score_predictions(self):
        """
        DESCRIPTION: Verify the close link by clicking on "X" mark on top right after submitting score predictions
        EXPECTED: Should be able to exit from 1-2-Free game page and should be navigate to home page of Application
        """
        one_two_free_you_are_in = self.site.one_two_free.one_two_free_you_are_in
        self.assertTrue(one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')
        self.assertTrue(one_two_free_you_are_in.close, msg='"Close Button" is not active')
        wait_for_haul(4)
        one_two_free_you_are_in.close.click()
        self.site.wait_content_state('homepage')

    def test_011_verify_special_super_button_display_on_home_page(self):
        """
        DESCRIPTION: Verify Special super button display on home page
        EXPECTED: Special super button should not display once predictions are submitted
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        special_super_button_displayed = wait_for_cms_reflection(
            lambda: self.site.home.super_button_section.super_button.button.name.upper()
                    != self.created_special_super_button['title'].upper(), ref=self)
        self.assertTrue(special_super_button_displayed,
                        msg="Special super button should not display once predictions are submitted, but still displaying in FE")

    def test_012_verify_super_button_displaying_home_page(self):
        """
        DESCRIPTION: Verify Super button displaying home page
        EXPECTED: Super button should be displayed if the setted Validity period of end date, time of super button is not expired
        """
        self.validate_super_button(page_content='home')

    def test_013_verify_logout_from_avatar_menu(self):
        """
        DESCRIPTION: Verify logout From Avatar menu
        EXPECTED: Logout should be performed without any issues
        """
        self.site.logout()
        # after logout user is navigated back to home page
        self.site.wait_content_state('homepage')

    def test_014_verify_super_button_post_logout(self):
        """
        DESCRIPTION: Verify Super button post logout
        EXPECTED: Super button should be displayed as per CMS config
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        self.validate_super_button(page_content='home')
