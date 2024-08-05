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
class Test_C10397569_Verify_Recently_Played_Games_module_enabling_disabling(Common):
    """
    TR_ID: C10397569
    NAME: Verify Recently Played Games module enabling/disabling
    DESCRIPTION: Test case verifies possibility to enable or disable the Recently Played Games module
    PRECONDITIONS: 1. There is logged in user with some playing history
    PRECONDITIONS: 2. Open the app Home page
    PRECONDITIONS: Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    """
    keep_browser_open = True

    def test_001_in_the_cms_make_a_module_not_active_and_save_changes(self):
        """
        DESCRIPTION: In the CMS make a module not active and save changes.
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_refresh_the_homepageverify_the_recently_played_games_module_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the homepage.
        DESCRIPTION: Verify the Recently Played Games module isn't displayed
        EXPECTED: Recently Played Games module isn't shown
        """
        pass

    def test_003_in_the_cms_make_a_module_active_and_save_changes(self):
        """
        DESCRIPTION: In the CMS make a module active and save changes.
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_refresh_the_homepageverify_the_recently_played_games_module_is_displayed(self):
        """
        DESCRIPTION: In the application refresh the homepage.
        DESCRIPTION: Verify the Recently Played Games module is displayed
        EXPECTED: Recently Played Games is shown
        """
        pass
