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
class Test_C44870332_Verify_functionality_of_banners_including_swipe_and_navigationNavigational_arrow_(Common):
    """
    TR_ID: C44870332
    NAME: "Verify functionality of banners including swipe and navigation(Navigational arrow) "
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

    def test_003_verify_aem_banners_on_hp(self):
        """
        DESCRIPTION: Verify AEM banners on HP
        EXPECTED: AEM banners are displayed on Homepage
        """
        pass

    def test_004_verify_functionality_of_banners_including_swipe_and_navigationnavigational_arrow(self):
        """
        DESCRIPTION: Verify functionality of banners including swipe and navigation(Navigational arrow)
        EXPECTED: User can scroll left or right within Banner Carousel
        EXPECTED: Dynamic Banners are navigated automatically
        EXPECTED: Dynamic Banners are shown in continuous loop
        EXPECTED: Verify the content is displayed correctly
        """
        pass

    def test_005_go_to_all_sport_or_race_page_and_repeat_step_4(self):
        """
        DESCRIPTION: Go to all <Sport> or <Race> page and repeat step #4
        EXPECTED: User can scroll left or right within Banner Carousel
        EXPECTED: Dynamic Banners are navigated automatically
        EXPECTED: Dynamic Banners are shown in continuous loop
        EXPECTED: Verify the content is displayed correctly
        """
        pass

    def test_006_log_out_and_repeat_step_3_4_5(self):
        """
        DESCRIPTION: Log out and repeat step #3 #4 #5
        EXPECTED: 
        """
        pass
