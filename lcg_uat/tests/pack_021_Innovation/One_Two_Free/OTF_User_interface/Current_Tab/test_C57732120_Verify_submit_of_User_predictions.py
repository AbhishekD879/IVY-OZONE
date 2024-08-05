import pytest
import tests
import datetime as dt
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result, wait_for_haul
from requests import HTTPError
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.helpers import get_response_url


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.high
@pytest.mark.other
@vtest
# this test case also covers C66007001, with Jira ID OZONE-9831
class Test_C57732120_Verify_submit_of_User_predictions(Common):
    """
    TR_ID: C57732120
    NAME: Verify submit of User predictions
    DESCRIPTION: This test case verifies submit of User predictions
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus'

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
            self.cms_config.update_game_view_status(game_id, enabled=True)

        season_created_flag = False
        # Retrieve a list of all available 1-2-Free games from the CMS.
        get_games = self.cms_config.get_games()
        # Find the active game by iterating through the list and checking if it is enabled and within its display date range.
        active_game = next((game for game in get_games if
                            game.get('enabled') is True and game.get(
                                'displayFrom') <= dt.datetime.utcnow().isoformat() <= game.get(
                                'displayTo')), None)
        if not active_game:
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
                                        gamification.get('seasonName') == active_season.get(
                                            'seasonName') and
                                        gamification.get(
                                            'displayFrom') <= dt.datetime.utcnow().isoformat() <= gamification.get(
                                            'displayTo')), None)
            #  if a new season is not created and no active gamification is present then raise CMSException.
            if not season_created_flag and not active_gamification:
                raise CMSException("There is already active season.So gamification cannot be created")
            # Creates gamification if it doesn't exist for the active season.
            if not active_gamification and season_created_flag:
                active_gamification = self.cms_config.create_gamification(active_season.get('id'))
            # Updates the active season.
            if season_created_flag and active_gamification:
                self.cms_config.update_season(active_season)

            create_game(active_season=active_season)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged In
        PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
        """
        if self.cms_config.get_bet_sharing_configuration().get('ftpBetSharingConfigs').get('enable'):
            self.cms_config.update_ftp_bet_sharing_configuration(enable=True)
        self.verify_and_create_one_two_free_game()

        # self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.__class__.username = tests.settings.default_username
        self.site.wait_content_state('Homepage')
        self.site.login(self.username)
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        self.assertTrue(bpp_token, msg='after login, token is not available')
        self.__class__.headers = {
            'Content-Type': 'application/json',
            'token': bpp_token
        }
        active_game_url = tests.settings.otf_url + f'{"initial-data/"}' + f'{self.username}'
        active_game = do_request(method='GET', url=active_game_url, headers=self.headers)
        self.__class__.active_game_id = active_game['activeGame']['id']

        url = tests.settings.otf_url + f'{"prediction/"}' + f'{self.username + "/"}' + f'{self.active_game_id}'
        self.navigate_to_page('1-2-free')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.one_two_free.one_two_free_welcome_screen.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')
        try:
            do_request(method='GET', url=url, headers=self.headers)
        except HTTPError as e:
            if '404' in e.args[0]:
                self._logger.info(
                    "User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)")
            else:
                raise e

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Current Tab' is successfully opened
        """
        self.__class__.one_two_free = self.site.one_two_free
        welcome_screen_play_here_button = wait_for_result(
            lambda: self.one_two_free.one_two_free_welcome_screen.play_button.is_displayed(), timeout=15)
        self.assertTrue(welcome_screen_play_here_button, msg='"PLAY HERE!" button is not available')
        self.one_two_free.one_two_free_welcome_screen.play_button.click()

    def test_002_choose_scores_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Choose scores and Tap on 'Submit' button
        EXPECTED: - FE send POST /api/v1/prediction with Game Id and User ID and body (see Swagger for actual request example)
        EXPECTED: - user should be navigated to 'You are in'
        """
        match = list(self.one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())[0]
        score_switchers = match.score_selector_container.items
        for score_switcher in score_switchers:
            self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                            msg=f'Upper arrow not displayed for "{match.name}".')
            score_switcher.increase_score_up_arrow.click()
        submit_button = wait_for_result(lambda: self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        self.one_two_free.one_two_free_current_screen.submit_button.click()
        wait_for_haul(2)
        url = tests.settings.otf_url + f'{"prediction/"}' + f'{self.username + "/"}' + f'{self.active_game_id}'
        otf_request = do_request(method='GET', url=url, headers=self.headers)
        self.assertIn('userId', otf_request.keys(),
                      msg='"userId" is not present in predictions')
        self.assertIn('gameId', otf_request.keys(),
                      msg='"gameId" is not present in predictions')
        self.assertTrue(self.one_two_free.one_two_free_you_are_in.has_you_are_in_icon_shown,
                        msg='You Are in page is not displayed')

        share_button_container = self.one_two_free.one_two_free_you_are_in.share_button_container

        actual_share_text = share_button_container.share_text.text
        expected_share_text = 'SHARE'
        self.assertEqual(actual_share_text, expected_share_text,
                         msg=f'Actual share text :"{actual_share_text}", does not match with'
                             f' expected share text :"{expected_share_text}"')

        share_logo = share_button_container.share_logo.get_attribute('src')
        self.assertTrue(share_logo, msg=f'share logo is not available, observed Logo source is :{share_logo}')

        horizontal_share_logo_location = share_button_container.share_logo.location.get('x')
        horizontal_share_text_location = share_button_container.share_text.location.get('x')

        self.assertLessEqual(horizontal_share_text_location, horizontal_share_logo_location,
                         msg=f' horizontal share text location value : "{horizontal_share_text_location}", is not less that'
                             f'horizontal share logo location value : "{horizontal_share_logo_location}"')

        Vertical_share_logo_location = share_button_container.share_logo.location.get('y')
        Vertical_share_text_location = share_button_container.share_text.location.get('y')

        Vertical_location = Vertical_share_logo_location - Vertical_share_text_location
        self.assertTrue(0 <= Vertical_location <= 2,
                         msg=f'Vertical share logo location: "{Vertical_share_logo_location}", does not match with'
                             f' Vertical share text location: "{Vertical_share_text_location}"')
