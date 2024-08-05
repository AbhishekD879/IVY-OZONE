import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C10397578_Verify_Recently_Played_Games_displaying_for_logged_out_user(Common):
    """
    TR_ID: C10397578
    NAME: Verify Recently Played Games displaying for logged out user
    DESCRIPTION: Test case verifies the displaying of the Recently Played Games module for logged in user only
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Open the app Home page
    PRECONDITIONS: 3. There is a logged out user with some playing history
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_verify_the_recently_played_games_module_is_not_shown_if_user_is_logged_out(self):
        """
        DESCRIPTION: Verify the Recently Played Games module is not shown if user is logged out
        EXPECTED: Recently Played Games module is not shown for logged out user
        """
        pass

    def test_002_login_to_the_applicationrefresh_the_home_pageverify_the_recently_played_games_module_is_shown(self):
        """
        DESCRIPTION: Login to the application
        DESCRIPTION: Refresh the Home page
        DESCRIPTION: Verify the Recently Played Games module is shown
        EXPECTED: Recently Played Games module is shown
        """
        pass

    def test_003_log_out_from_the_applicationrefresh_the_home_pageverify_the_recently_played_games_module_is_not_shown(self):
        """
        DESCRIPTION: Log out from the application
        DESCRIPTION: Refresh the Home page
        DESCRIPTION: Verify the Recently Played Games module is not shown
        EXPECTED: Recently Played Games module is not shown
        """
        pass
