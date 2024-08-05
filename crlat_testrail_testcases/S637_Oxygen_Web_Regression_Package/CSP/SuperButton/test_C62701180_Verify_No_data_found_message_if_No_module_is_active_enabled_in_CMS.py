import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C62701180_Verify_No_data_found_message_if_No_module_is_active_enabled_in_CMS(Common):
    """
    TR_ID: C62701180
    NAME: Verify "No data found " message if No module is active/enabled in CMS
    DESCRIPTION: This test case verifies " No data found "message if  No module is active/enabled in CMS
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;- CMS &gt; Sports pages &gt; Super button
    PRECONDITIONS: 2) No module should be active/enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_universalsegmented_user(self):
        """
        DESCRIPTION: Launch oxygen application and login Universal/segmented user
        EXPECTED: User should able to launch and login successfully
        """
        pass

    def test_002_navigate_to_home_pageevent_hub(self):
        """
        DESCRIPTION: Navigate to Home page/Event hub
        EXPECTED: "No data found " message should be shown in FE
        """
        pass
