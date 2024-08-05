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
class Test_C10397577_Verify_Recently_Played_Games_ordering_within_a_module(Common):
    """
    TR_ID: C10397577
    NAME: Verify Recently Played Games ordering within a module
    DESCRIPTION: Test case verifies the order of games within the Recently Played Games module
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user who played a few games
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_in_the_app_click_on_the_last_thumbnail_within_the_recently_played_games_modulereturn_to_the_home_page_and_verify_the_thumbnail_is_now_placed_to_the_first_position(self):
        """
        DESCRIPTION: In the app click on the last thumbnail within the Recently Played Games module
        DESCRIPTION: Return to the Home page and verify the thumbnail is now placed to the first position
        EXPECTED: Clicked thumbnail is moved to the first position
        """
        pass
