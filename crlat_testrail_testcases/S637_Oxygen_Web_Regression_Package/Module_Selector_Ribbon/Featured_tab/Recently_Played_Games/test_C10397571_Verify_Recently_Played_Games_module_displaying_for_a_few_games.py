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
class Test_C10397571_Verify_Recently_Played_Games_module_displaying_for_a_few_games(Common):
    """
    TR_ID: C10397571
    NAME: Verify Recently Played Games module displaying for a few games
    DESCRIPTION: Verify the displaying of the Recently Played Games module if a few games were played
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games (3+)
    PRECONDITIONS: 2. Login to the app as a user who played a few games (3+)
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_recently_played_games_module_with_a_few_games(self):
        """
        DESCRIPTION: Verify displaying of Recently Played Games module with a few games
        EXPECTED: Module contains elements:
        EXPECTED: * Module title, defined in the CMS
        EXPECTED: * See More >, link
        EXPECTED: * 2.5 thumbnails are shown
        """
        pass

    def test_002_in_the_cms_set_games_amount_to_1(self):
        """
        DESCRIPTION: In the CMS set Games amount to 1
        EXPECTED: 
        """
        pass

    def test_003_in_the_app_refresh_the_page_verify_now_there_is_one_thumbnail_within_the_module(self):
        """
        DESCRIPTION: In the app refresh the page. Verify now there is one thumbnail within the module
        EXPECTED: One thumbnail with the played game is shown (the most recent)
        """
        pass
