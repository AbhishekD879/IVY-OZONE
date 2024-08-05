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
class Test_C44870333_Verify_user_navigated_to_another_tab_on_clicking_of_18_link_from_banner(Common):
    """
    TR_ID: C44870333
    NAME: Verify user navigated to another tab on clicking of 18+ link from banner
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

    def test_004_verify_user_navigated_to_correct_page_on_clicking_of_18plus_link_from_banner(self):
        """
        DESCRIPTION: Verify user navigated to correct page on clicking of 18+ link from banner
        EXPECTED: User navigated to promotion page
        """
        pass

    def test_005_repeat_step_4_for_all_sports_and_racing(self):
        """
        DESCRIPTION: repeat step #4 for all sports and racing
        EXPECTED: User navigated to promotion page
        """
        pass
