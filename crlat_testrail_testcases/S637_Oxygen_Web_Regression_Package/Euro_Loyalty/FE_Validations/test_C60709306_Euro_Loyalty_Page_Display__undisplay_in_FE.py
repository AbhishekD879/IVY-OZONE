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
class Test_C60709306_Euro_Loyalty_Page_Display__undisplay_in_FE(Common):
    """
    TR_ID: C60709306
    NAME: Euro Loyalty Page- Display / undisplay in FE
    DESCRIPTION: This test case is to validate Euro Loyalty page is displaying or underplaying as per CMS configuration
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  configuration for  Euro Loyalty Page should done in sports categories
    """
    keep_browser_open = True

    def test_001_hit_the_cms_url(self):
        """
        DESCRIPTION: Hit the CMS URL
        EXPECTED: User is on CMS application
        """
        pass

    def test_002_navigate_to_sports_pages___sports_category___euroloyaltyprogram(self):
        """
        DESCRIPTION: Navigate to sports pages - sports category - EuroLoyaltyProgram
        EXPECTED: EuroLoyalty config page should open
        """
        pass

    def test_003_uncheck_active_check_box_and_save_changes_in_cms(self):
        """
        DESCRIPTION: uncheck active check box and save changes in CMS
        EXPECTED: in FE euro loyalty should not display for desktop, mobile and tab
        """
        pass

    def test_004_repeat_above_step_check_uncheck_for_following_optionshow_in_a_z_menushow_in_appis_top_sportshow_in_sport_ribbon(self):
        """
        DESCRIPTION: repeat above step check uncheck for following option
        DESCRIPTION: Show in A-Z menu
        DESCRIPTION: show in App
        DESCRIPTION: IS top sport
        DESCRIPTION: show in sport ribbon
        EXPECTED: should works as expected changes made in CMS should reflect in FE
        """
        pass

    def test_005_changes_svg_icon_or_browse_icon_for_euro_in_cms_and_verify_it_in_fe(self):
        """
        DESCRIPTION: Changes SVG icon or browse icon for euro in CMS and verify it in FE
        EXPECTED: Respective svg icon should display in FE
        EXPECTED: sports ribbon
        EXPECTED: a-z menu mobile and desktop
        """
        pass
