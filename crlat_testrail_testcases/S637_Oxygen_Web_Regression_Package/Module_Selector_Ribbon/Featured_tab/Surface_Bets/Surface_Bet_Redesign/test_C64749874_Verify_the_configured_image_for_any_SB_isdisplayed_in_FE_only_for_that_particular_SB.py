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
class Test_C64749874_Verify_the_configured_image_for_any_SB_isdisplayed_in_FE_only_for_that_particular_SB(Common):
    """
    TR_ID: C64749874
    NAME: Verify the configured image for any SB is
displayed in FE only for that particular SB
    DESCRIPTION: Testcase verifies if user can configure a background
    DESCRIPTION: image in CMS.
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

    def test_002_navigate_to_surface_bet_module_and_click_on_surface_bet_link(self):
        """
        DESCRIPTION: Navigate to surface bet module and click on surface bet link.
        EXPECTED: User should be able to enter all mandatory fields.
        """
        pass

    def test_003_upload_surface_bet_imageslogos_in_cms_from_image_manager_and_verify_uploaded_image_is_configured_for_only_particular_surfacebet(self):
        """
        DESCRIPTION: Upload Surface bet images/logos in CMS from image manager and verify uploaded image is configured for only particular surfacebet.
        EXPECTED: background image should be changed for only particular surfacebet and make sure that image is not uploaded for others.
        """
        pass
