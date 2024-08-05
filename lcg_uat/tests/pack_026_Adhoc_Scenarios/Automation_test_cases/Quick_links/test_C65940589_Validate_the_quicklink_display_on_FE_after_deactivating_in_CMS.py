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
class Test_C65940589_Validate_the_quicklink_display_on_FE_after_deactivating_in_CMS(Common):
    """
    TR_ID: C65940589
    NAME: Validate the quicklink display on FE after deactivating in CMS
    DESCRIPTION: This test case is to validate that Quicklinks should not be displayed on FE after deactivation in CMS
    PRECONDITIONS: 1.Deactivate the currently running quicklink in Quicklink details page of CMS
    """
    keep_browser_open = True

    def test_001_launch_mobile_application(self):
        """
        DESCRIPTION: Launch mobile application.
        EXPECTED: Application should be loaded successfully. By default, home page should be loaded.
        """
        pass

    def test_002_verify_display_of_created_quick_link_on_fe(self):
        """
        DESCRIPTION: Verify display of created quick link on FE
        EXPECTED: Quick link should be displayed.
        EXPECTED: Quick link should not be displayed if current system date and time is less then configured date and time
        """
        pass

    def test_003_in_cms_now_deactivate_the_quicklink(self):
        """
        DESCRIPTION: In CMS, now deactivate the quicklink
        EXPECTED: Quicklink deactivated successfully.
        """
        pass

    def test_004_in_fe_validate_the_display_of_quicklink(self):
        """
        DESCRIPTION: In FE, validate the display of quicklink
        EXPECTED: Quik link should not be displayed on FE after deactivation
        """
        pass
