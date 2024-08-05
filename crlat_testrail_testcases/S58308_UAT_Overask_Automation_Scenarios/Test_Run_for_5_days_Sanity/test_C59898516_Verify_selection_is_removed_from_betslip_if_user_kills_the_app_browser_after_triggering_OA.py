import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898516_Verify_selection_is_removed_from_betslip_if_user_kills_the_app_browser_after_triggering_OA(Common):
    """
    TR_ID: C59898516
    NAME: Verify selection is removed from betslip if user kills the app/browser after triggering OA.
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Login, Add selection and trigger OA
        EXPECTED: OA is triggered
        """
        pass

    def test_002_kill_appbrowser(self):
        """
        DESCRIPTION: Kill app/browser
        EXPECTED: User is logged out and betslip is empty
        """
        pass

    def test_003_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: Uses logs in and betslip should be empty
        """
        pass
