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
class Test_C9770750_Verify_Recently_Played_Games_module_BE_Enabler_response(Common):
    """
    TR_ID: C9770750
    NAME: Verify Recently Played Games module BE Enabler response
    DESCRIPTION: Test case verifies a proper BE response for Recently Played Games
    PRECONDITIONS: Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    PRECONDITIONS: - Correct example for  bundle URL -https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    """
    keep_browser_open = True

    def test_001_verify_the_ws_response_featured_structure_changed_with_module_recentlyplayedgamemodule_is_received_and_contains_the_current_configuration_for_the_home_page(self):
        """
        DESCRIPTION: Verify the WS response FEATURED_STRUCTURE_CHANGED with module RecentlyPlayedGameModule is received and contains the current configuration for the Home Page
        EXPECTED: Response of the following format is received:
        EXPECTED: {
        EXPECTED: "@type": "RecentlyPlayedGameModule"
        EXPECTED: ...
        EXPECTED: {
        EXPECTED: "@type": "RpgConfig"
        EXPECTED: },
        EXPECTED: ...
        EXPECTED: }
        """
        pass

    def test_002_verify_the_response_contains_data_on_the_recently_played_games_module(self):
        """
        DESCRIPTION: Verify the response contains data on the Recently Played Games module
        EXPECTED: Response contains data on configuration loaded from the CMS:
        EXPECTED: "sportId": 0
        EXPECTED: "gamesAmount": int
        EXPECTED: "seeMoreLink": "someURL"
        EXPECTED: "title": "someTitle"
        EXPECTED: **FROM OX99 Added 2 new parameters:**
        EXPECTED: "bundleUrl": bundle_URL
        EXPECTED: "loaderUrl": loader_URL
        """
        pass

    def test_003_open_some_sport_landing_page_verify_the_recently_played_games_response_isnt_received_on_any_other_page_except_of_homepage(self):
        """
        DESCRIPTION: Open some Sport Landing Page. Verify the Recently Played Games response isn't received on any other page except of Homepage
        EXPECTED: Response on Recently Played Games is not received
        """
        pass

    def test_004_in_the_cms_disable_the_recently_played_games_module(self):
        """
        DESCRIPTION: In the CMS disable the Recently Played Games module
        EXPECTED: 
        """
        pass

    def test_005_in_the_application_open_the_homepage_verify_the_recently_played_games_response_isnt_received_if_its_disabled_in_the_cms(self):
        """
        DESCRIPTION: In the application open the Homepage. Verify the Recently Played Games response isn't received if it's disabled in the CMS
        EXPECTED: Response on Recently Played Games is not received
        """
        pass
