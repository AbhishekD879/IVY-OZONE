import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870330_iOS__Android__Verify_user_see_smart_banner_display_when_it_is_enabled_Disabled_on_the_CMSCheck_changes_reflected_on_front_end_(Common):
    """
    TR_ID: C44870330
    NAME: iOS / Android - "Verify user see smart banner display when it is enabled/Disabled on the CMSCheck changes reflected on front end "
    DESCRIPTION: This test case verifies Smart Banners displaying on HomePage to first time login user
    PRECONDITIONS: Smart Banners should be enabled/disabled in CMS
    PRECONDITIONS: UserName : goldebuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_new__existing_user(self):
        """
        DESCRIPTION: Log in with user new / existing user
        EXPECTED: User is logged in
        """
        pass

    def test_003_verify_user_see_smart_banner_on_hp(self):
        """
        DESCRIPTION: Verify user see smart banner on HP
        EXPECTED: Smart banner displayed on Homepage
        """
        pass
