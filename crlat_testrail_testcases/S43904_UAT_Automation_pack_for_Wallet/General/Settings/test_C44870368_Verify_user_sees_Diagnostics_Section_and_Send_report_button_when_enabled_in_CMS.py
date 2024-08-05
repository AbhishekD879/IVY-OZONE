import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870368_Verify_user_sees_Diagnostics_Section_and_Send_report_button_when_enabled_in_CMS(Common):
    """
    TR_ID: C44870368
    NAME: Verify user sees Diagnostics Section and Send report button when enabled in CMS
    DESCRIPTION: 
    PRECONDITIONS: 1. User is logged in the application.
    PRECONDITIONS: 2. Diagnostics Section is enabled in CMS.
    """
    keep_browser_open = True

    def test_001_navigate_to_settings_from_the_my_accountright_menu_and_verify(self):
        """
        DESCRIPTION: Navigate to Settings from the My Account/Right menu and verify.
        EXPECTED: Diagnostics Section and Send report button is displayed.
        """
        pass
