import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C64749879_Verify_the_BG_image_adjusts_properly_for_diff_sizes_of_SB_SB_height_increases_if_we_enter_more_text(Common):
    """
    TR_ID: C64749879
    NAME: Verify the BG image adjusts properly for 
diff sizes of SB (SB height increases if we enter more text)
    DESCRIPTION: Testcase verifies if BG image adjusts properly for
    DESCRIPTION: diff sizes of SB (SB height increases if we enter more text)
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_upload_different_sized_surface_bet_imageslogos_in_cms_from_image_manager(self):
        """
        DESCRIPTION: Upload different sized Surface bet images/logos in CMS from image manager.
        EXPECTED: Background image should be uploaded in FE.
        """
        pass

    def test_003_verify_bg_image_adjusts_properly_fordiff_sizes_of_sb(self):
        """
        DESCRIPTION: Verify BG image adjusts properly for
        DESCRIPTION: diff sizes of SB
        EXPECTED: The height of a surface bet is not fixed currently and so that it should stretches to the box that has the most text on it. As a result we will need to make sure that the background is applied from the top of the box and not made central so that they don't have white space at the bottom on larger surface bets
        """
        pass
