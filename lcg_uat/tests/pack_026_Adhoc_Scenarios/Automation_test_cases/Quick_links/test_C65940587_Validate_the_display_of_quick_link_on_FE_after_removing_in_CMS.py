import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65940587_Validate_the_display_of_quick_link_on_FE_after_removing_in_CMS(Common):
    """
    TR_ID: C65940587
    NAME: Validate the display of quick link on FE after removing in CMS
    DESCRIPTION: This test case is to validate Quick link should not be displayed on FE after removing in
    DESCRIPTION: QUICK LINK MODULE page in CMS
    PRECONDITIONS: 1.Remove any existing quick link in QUICK LINK MODULE
    """
    keep_browser_open = True

    def test_001_launch_mobile_application(self):
        """
        DESCRIPTION: Launch mobile application.
        EXPECTED: Application should be loaded successfully. By default, home page should be loaded.
        """
        pass

    def test_002_validate_the_display_of_removed_quick_link_on_fe(self):
        """
        DESCRIPTION: Validate the display of removed quick link on FE
        EXPECTED: Removed quicklink should not be displayed on FE
        """
        pass
