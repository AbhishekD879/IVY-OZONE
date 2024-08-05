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
class Test_C44870331_Verify_AEM_banner_display_on_homepage_all_sports_landing_pages_and_racing_landing_pages(Common):
    """
    TR_ID: C44870331
    NAME: Verify AEM banner display on homepage, all sports landing pages and racing landing pages.
    DESCRIPTION: This test case verifies AEM Banners displaying according to New / Existing Users
    PRECONDITIONS: AEM Banners should be enabled in CMS
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

    def test_003_verify_aem_banners(self):
        """
        DESCRIPTION: Verify AEM banners
        EXPECTED: AEM banners are displayed on Homepage
        """
        pass

    def test_004_go_to_all__sport_or_race_page_and_repeat_step_3(self):
        """
        DESCRIPTION: Go to all  <Sport> or <Race> page and repeat step #3
        EXPECTED: AEM banners are displayed on all sports or races
        """
        pass

    def test_005_log_out_and_verify_the_step_3__4(self):
        """
        DESCRIPTION: Log out and verify the step #3 & #4
        EXPECTED: AEM banners are displayed on Homepage
        EXPECTED: AEM banners are displayed on all sports or races
        """
        pass
