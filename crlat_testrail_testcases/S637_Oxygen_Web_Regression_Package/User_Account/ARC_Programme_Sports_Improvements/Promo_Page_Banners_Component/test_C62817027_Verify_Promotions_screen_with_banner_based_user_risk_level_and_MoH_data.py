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
class Test_C62817027_Verify_Promotions_screen_with_banner_based_user_risk_level_and_MoH_data(Common):
    """
    TR_ID: C62817027
    NAME: Verify Promotions screen with banner based user risk level and MoH data
    DESCRIPTION: This test case verifies creating and displaying Promotions content based on banner
    PRECONDITIONS: User is logged FE
    """
    keep_browser_open = True

    def test_001_load_cms_gtpromotions(self):
        """
        DESCRIPTION: Load CMS-&gt;Promotions
        EXPECTED: 
        """
        pass

    def test_002_add_new_promotion_with_all_required_data_and_image(self):
        """
        DESCRIPTION: Add new Promotion with all required data and image
        EXPECTED: Added Promotion appears in the list of Promotions of Sportsbook brand in CMS.
        """
        pass

    def test_003_configure_the_user_risk_level_and_moh_in_cms(self):
        """
        DESCRIPTION: Configure the user risk level and MoH in CMS
        EXPECTED: Entered data should be saved
        """
        pass

    def test_004_login_to_application(self):
        """
        DESCRIPTION: Login to Application
        EXPECTED: User should login successfully
        """
        pass

    def test_005_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: .Promotions' page is opened
        EXPECTED: .List of all available promotions is present
        """
        pass

    def test_006_check_the_promotion_created_with_banner_available(self):
        """
        DESCRIPTION: Check the promotion created with banner available
        EXPECTED: content must be displayed if banners are available
        """
        pass
