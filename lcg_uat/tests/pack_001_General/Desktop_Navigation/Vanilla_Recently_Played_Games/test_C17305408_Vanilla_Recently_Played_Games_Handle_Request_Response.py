import pytest
from tests.base_test import vtest
from tests.Common import Common
import tests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
# This test case is now outdated due to changes in the Recently Played Games feature.
# It has transformed from an iframe to a module.
# Please refer to the new test case C65939806 for updated testing instructions.
class Test_C17305408_Vanilla_Recently_Played_Games_Handle_Request_Response(Common):
    """
    TR_ID: C17305408
    VOL_ID: C35209663
    NAME: [Vanilla] Recently Played Games: Handle Request/Response
    DESCRIPTION: This test case verifies  handle the request/response between iFrame and the GVC RPG Component
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Recently Played games widget is created and configured in CMS > Sports Pages > Homepage > Recently Played Games;
        DESCRIPTION: 2. Recently Played games widget is active in CMS;
        DESCRIPTION: 3. Oxygen app is loaded;
        DESCRIPTION: 4. User is registered and logged into the app;
        DESCRIPTION: 5. User is landed on the Home page;
        DESCRIPTION: 6. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
        DESCRIPTION: NOTE:
        DESCRIPTION: 1. Link to visual designs: https://app.zeplin.io/project/5cf14a4dd64fdd1e164d8159?seid=5cf7e65e2d86001d8c6e58
        DESCRIPTION: 2. Link to technical documentation: https://docs.google.com/document/d/1niWXC8SbCIXGGidLkyWRBZyLk0yCI_sVYZGZpSMhGgI/edit?usp=sharing
        """
        rpg_cms_module = self.cms_config.get_sport_module(sport_id=0, module_type='RECENTLY_PLAYED_GAMES')[0]
        if rpg_cms_module.get('disabled'):
            raise CmsClientException('"Recently Played Games" module is disabled for homepage')

        self.site.login(username=tests.settings.recently_played_games_user)
        self.site.wait_content_state('HomePage')

    def test_001_observe_the_page(self):
        """
        DESCRIPTION: Observe the page;
        EXPECTED: - Recently Played Games iframe is loaded and visible to User;
        EXPECTED: - "eventName: LobbyLoaded is loaded" notification is visible in Console;
        """
        self.assertTrue(self.site.recently_played_games.is_displayed(timeout=3),
                        msg='Recently Played Games Widget is not displayed!')

    def test_002_tap_on_the_one_of_the_gvc_mini_games_displayed_within_iframe(self):
        """
        DESCRIPTION: Tap on the one of the GVC mini games displayed within iframe
        EXPECTED: - Game launch notification is received:
        EXPECTED: {Name:GameLaunch,
        EXPECTED: params:
        EXPECTED: redirectUrl: xx}
        EXPECTED: - User is redirected to the respective URL within the same window.
        """
        self.__class__.rpg_widget = self.site.recently_played_games.stick_to_iframe()
        games = self.rpg_widget.items_as_ordered_dict
        self.assertTrue(games, msg='No games found in RPG widget!')
        first_game_name, first_game = list(games.items())[0]
        expected_url_part = f'en/rpwidgetrp/launchEmbedded/{first_game_name}'

        first_game.click()
        result = wait_for_result(lambda: expected_url_part in self.device.get_current_url(),
                                 timeout=10,
                                 name='Game to open')
        self.assertTrue(result, msg=f'User is redirected to the wrong page: "{expected_url_part}" not found in URL: "{self.device.get_current_url()}"')

    def test_003_return_to_the_home_screen(self):
        """
        DESCRIPTION: Return to the Home screen
        EXPECTED: User is landed on the Home screen;
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')

    def test_004_navigate_to_iframe_and_click_on_see_all_link(self):
        """
        DESCRIPTION: Navigate to iframe and click on "See All" link;
        EXPECTED: The User is redirected to the Games Lobby
        """
        self.site.recently_played_games.see_more.click()
        expected_url = tests.settings.gaming_url
        self.assertEqual(expected_url, self.device.get_current_url(),
                         msg=f'User is redirected to the wrong page: "{self.device.get_current_url()}", '
                             f''f'expected is: "{expected_url}"')
