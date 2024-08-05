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
class Test_C64881024_Verify_HC_when_inplay_check_box_is_checked(Common):
    """
    TR_ID: C64881024
    NAME: Verify HC when inplay check box is checked
    DESCRIPTION: This Test case verifies HC for live events
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>HC
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to see the HC module page with existing Universal HC records
        """
        pass

    def test_003_click_on_create_highlight_carousel_cta(self):
        """
        DESCRIPTION: Click on Create highlight carousel CTA
        EXPECTED: User should able view detail page
        """
        pass

    def test_004_create_hc_with_display_inplay_check_box_is_checked(self):
        """
        DESCRIPTION: Create HC with display inplay check box is checked
        EXPECTED: HC should able to create successfully
        """
        pass

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_006_verify_hc__in_home_page(self):
        """
        DESCRIPTION: Verify HC  in Home page
        EXPECTED: Inplay events should display in HC ,as display inplay check box is checked in CMS
        """
        pass

    def test_007_create_hc_with_display_inplay_check_box_is_unchecked(self):
        """
        DESCRIPTION: Create HC with display inplay check box is unchecked
        EXPECTED: HC should able to create successfully
        """
        pass

    def test_008_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_009_verify_hc__in_home_page(self):
        """
        DESCRIPTION: Verify HC  in Home page
        EXPECTED: Pre events should only display in HC ,as display inplay check box is unchecked in CMS
        """
        pass
