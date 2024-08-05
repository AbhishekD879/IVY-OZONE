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
class Test_C10397575_Verify_a_proper_game_page_is_opened_if_click_this_game_icon(Common):
    """
    TR_ID: C10397575
    NAME: Verify a proper game page is opened if click this game icon
    DESCRIPTION: Test case verifies the proper redirecting when click the game thumbnail
    PRECONDITIONS: 1. Recently Played Games module is active and configured to show a few games
    PRECONDITIONS: 2. Login to the app as a user with some playing history
    PRECONDITIONS: 3. Open the app Home page
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: You can ask  about valid bundle URL from Patrick Tolosa.
    PRECONDITIONS: Links are different for Coral and Ladbrokes.
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_in_the_application_click_some_game_thumbnail(self):
        """
        DESCRIPTION: In the application click some game thumbnail
        EXPECTED: The appropriate game invitation ("Play now") page is opened
        EXPECTED: User is logged in
        """
        pass
