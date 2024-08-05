import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
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

    def test_001_verify_the_recently_played_games_module_isnt_shown_if_there_is_not_playing_history(self):
        """
        DESCRIPTION: Verify the Recently Played Games module isn't shown if there is not playing history
        EXPECTED: Recently Played Games module isn't shown
        """
        pass
