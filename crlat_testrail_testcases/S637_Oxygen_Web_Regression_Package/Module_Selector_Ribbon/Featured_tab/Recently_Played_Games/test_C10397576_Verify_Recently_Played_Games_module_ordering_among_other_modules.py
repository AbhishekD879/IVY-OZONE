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
class Test_C10397576_Verify_Recently_Played_Games_module_ordering_among_other_modules(Common):
    """
    TR_ID: C10397576
    NAME: Verify Recently Played Games module ordering among other modules
    DESCRIPTION: Test case verifies possibility to define a module order among other modules
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user with some playing history
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_verify_the_order_of_the_recently_played_games_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Recently Played Games module is as per order in the CMS
        EXPECTED: The order is as defined in CMS
        """
        pass

    def test_002_change_the_order_in_the_cmsin_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS.
        DESCRIPTION: In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
