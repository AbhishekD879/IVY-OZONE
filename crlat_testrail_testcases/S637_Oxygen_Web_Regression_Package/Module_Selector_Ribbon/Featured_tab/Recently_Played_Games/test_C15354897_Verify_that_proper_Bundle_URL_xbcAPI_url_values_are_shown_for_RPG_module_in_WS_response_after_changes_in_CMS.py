import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C15354897_Verify_that_proper_Bundle_URL_xbcAPI_url_values_are_shown_for_RPG_module_in_WS_response_after_changes_in_CMS(Common):
    """
    TR_ID: C15354897
    NAME: Verify that proper 'Bundle URL' & 'xbcAPI url' values are shown for RPG module in WS response after changes in CMS.
    DESCRIPTION: Test case verifies that proper 'Bundle URL' & 'xbcAPI url' values are shown after changes in CMS.
    PRECONDITIONS: - Recently Played Games module is active and configured this right bundle URL in CMS.
    PRECONDITIONS: - Open the app Home page
    PRECONDITIONS: - Enter Dev tools -> Network->WS->Feature Changed->modules->bundle URL
    PRECONDITIONS: - Path for CMS configuration: Sports Pages > Homepage > Recently Played Games
    PRECONDITIONS: - Correct values for 'Bundle URL' field:
    PRECONDITIONS: Coral - https://apk.coral.co.uk/XBC/bundler-coral-sports-react-bundler/2.1.2
    PRECONDITIONS: Ladbrokes - https://apk.coral.co.uk/XBC/bundler-ladbrokes-bundler/feature/GEM-5061-MWSS-Recently-Migration
    PRECONDITIONS: - Correct values for 'xbcAPI URL' field:
    PRECONDITIONS: Coral - https://apk.coral.co.uk/XBC/xbc/feature/GEM-5061-MWSS-Recently-tag/loader.js
    PRECONDITIONS: Ladbrokes - https://apk.coral.co.uk/XBC/xbc/feature/GEM-5061-MWSS-Recently-tag/loader.js
    """
    keep_browser_open = True

    def test_001_verify_that_the_right_bundle_url_is_shown_in_ws_for_recently_played_games_module_on_the_homepage(self):
        """
        DESCRIPTION: Verify that the right 'Bundle URL' is shown in WS for Recently Played Games module on the Homepage.
        EXPECTED: Correct 'Bundle URL' value is shown in 'Featured Structure Changed' WS response in 'Recently Played Games' module (it should be the same as you configured in CMS).
        """
        pass

    def test_002_verify_that_the_right_xbcapi_url_is_shown_in_ws_for_recently_played_games_module_on_the_homepage(self):
        """
        DESCRIPTION: Verify that the right 'xbcAPI URL' is shown in WS for Recently Played Games module on the Homepage.
        EXPECTED: Correct 'xbcAPI URL' value is shown in 'Featured Structure Changed' WS response in 'Recently Played Games' module (it should be the same as you configured in CMS).
        """
        pass
