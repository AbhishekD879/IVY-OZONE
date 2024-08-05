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
class Test_C64749876_Verify_if_the_BG_image_is_displayed_without_any_graphical_errors_glitches(Common):
    """
    TR_ID: C64749876
    NAME: Verify if the BG image is displayed without 
any graphical errors/glitches
    DESCRIPTION: Testcase verifies if BG image is displayed without any graphical errors/glitches
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

    def test_002_upload_surface_bet_imageslogos_in_cms_from_image_manager_and_verify_uploaded_image_is_displyed_in_fe_without_any_glitches(self):
        """
        DESCRIPTION: Upload Surface bet images/logos in CMS from image manager and verify uploaded image is displyed in FE without any glitches.
        EXPECTED: proper Background image should be displayed in FE without any glitches
        """
        pass
