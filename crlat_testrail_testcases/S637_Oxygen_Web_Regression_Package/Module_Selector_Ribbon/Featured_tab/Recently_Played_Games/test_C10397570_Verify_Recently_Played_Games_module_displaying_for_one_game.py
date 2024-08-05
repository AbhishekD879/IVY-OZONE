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
class Test_C10397570_Verify_Recently_Played_Games_module_displaying_for_one_game(Common):
    """
    TR_ID: C10397570
    NAME: Verify Recently Played Games module displaying for one game
    DESCRIPTION: Verify the displaying of the Recently Played Games module if one game was played
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user who played one game
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_recently_played_games_module_with_one_game(self):
        """
        DESCRIPTION: Verify displaying of Recently Played Games module with one game
        EXPECTED: Module contains elements:
        EXPECTED: * Module title, defined in the CMS
        EXPECTED: * See More >, link
        EXPECTED: * One thumbnail with the played game, aligned to the left
        """
        pass
