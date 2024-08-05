import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C10397626_Verify_Recently_Played_Games_module_displaying_for_the_new_user(Common):
    """
    TR_ID: C10397626
    NAME: Verify Recently Played Games module displaying for the new user
    DESCRIPTION: Test case verifies the Recently Played Games module isn't shown for the new registered user/user that never played games
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user without playing history/new registered user
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
        PRECONDITIONS: 2. Login to the app as a user without playing history/new registered user
        PRECONDITIONS: 3. Open the app Home page
        PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
        PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
        """
        rpg_cms_module = self.cms_config.get_sport_module(sport_id=0, module_type='RECENTLY_PLAYED_GAMES')[0]
        if rpg_cms_module.get('disabled'):
            raise CmsClientException('"Recently Played Games" module is disabled for homepage')

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.wait_content_state('HomePage')

    def test_001_verify_the_recently_played_games_module_isnt_shown_if_there_is_not_playing_history(self):
        """
        DESCRIPTION: Verify the Recently Played Games module isn't shown if there is not playing history
        EXPECTED: Recently Played Games module isn't shown
        """
        result = False
        try:
            self.site.recently_played_games.is_displayed(timeout=3)
        except Exception:
            result = True
        self.assertTrue(result,
                        msg='Recently Played Games Widget is displayed, whereas it should not display for newly registered user')
