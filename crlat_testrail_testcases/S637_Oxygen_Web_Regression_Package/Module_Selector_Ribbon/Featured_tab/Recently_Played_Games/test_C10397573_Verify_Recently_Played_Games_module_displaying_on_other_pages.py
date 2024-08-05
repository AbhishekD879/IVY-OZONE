import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C10397573_Verify_Recently_Played_Games_module_displaying_on_other_pages(Common):
    """
    TR_ID: C10397573
    NAME: Verify Recently Played Games module displaying on other pages
    DESCRIPTION: Test case verifies that the Recently Played Games module is shown on the Home page only
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user who played a few games
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_open_the_neighboring_tabs_e_g_inplay_build_your_bet_and_verify_the_recently_played_games_module_isnt_shown(self):
        """
        DESCRIPTION: Open the neighboring tabs (e. g. Inplay, Build Your Bet) and verify the Recently Played Games module isn't shown
        EXPECTED: Recently Played Games module isn't shown
        """
        pass

    def test_002_open_the_sports_landing_pages_and_verify_the_recently_played_games_module_isnt_shown(self):
        """
        DESCRIPTION: Open the sports landing pages and verify the Recently Played Games module isn't shown
        EXPECTED: Recently Played Games module isn't shown
        """
        pass
