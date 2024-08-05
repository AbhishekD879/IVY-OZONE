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
class Test_C62817029_Verify_Promotions_screen_with_banner_for_not_login(Common):
    """
    TR_ID: C62817029
    NAME: Verify Promotions screen with banner for not login
    DESCRIPTION: This test case verifies displaying Promotions content for not login user
    PRECONDITIONS: User not  logged into  FE
    """
    keep_browser_open = True

    def test_001_navigate_to_application(self):
        """
        DESCRIPTION: Navigate to application
        EXPECTED: No user is logged in
        """
        pass

    def test_002_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: .Promotions' page is opened
        """
        pass

    def test_003_(self):
        """
        DESCRIPTION: 
        EXPECTED: .List of all available promotions is present
        """
        pass

    def test_004_check_the_promotion_content_and__banner_available(self):
        """
        DESCRIPTION: Check the promotion content and  banner available
        EXPECTED: No content information  should be availabel for not login
        """
        pass
