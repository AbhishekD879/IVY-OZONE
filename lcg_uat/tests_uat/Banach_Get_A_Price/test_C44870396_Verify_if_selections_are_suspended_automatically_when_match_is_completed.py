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
class Test_C44870396_Verify_if_selections_are_suspended_automatically_when_match_is_completed(Common):
    """
    TR_ID: C44870396
    NAME: Verify if selections are suspended automatically when match is completed
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com
        EXPECTED: Ladbrokes application launched
        """
        pass

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to football
        EXPECTED: Football LP displayed
        """
        pass

    def test_003_select_match_which_contains_banache_markets_and_selections(self):
        """
        DESCRIPTION: Select match which contains banache markets and selections
        EXPECTED: Banache markets and selections displayed
        """
        pass

    def test_004_verify_these_selections_suspend_when_match_completes(self):
        """
        DESCRIPTION: Verify these selections suspend when match completes
        EXPECTED: Corresponding banache selections are suspended.
        """
        pass
