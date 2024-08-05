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
class Test_C10397572_Verify_Recently_Played_Games_module_displaying_if_Games_amount_is_0(Common):
    """
    TR_ID: C10397572
    NAME: Verify Recently Played Games module displaying if Games amount is 0
    DESCRIPTION: Test case verifies that module configured to show 0 games isn't shown
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show 0 games
    PRECONDITIONS: 2. Login to the app as a user who played a few games
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_verify_the_recently_played_games_module_isnt_shown_if_its_configured_to_shown_0_games(self):
        """
        DESCRIPTION: Verify the Recently Played Games module isn't shown if it's configured to shown 0 games
        EXPECTED: Recently Played Games module isn't shown
        """
        pass
