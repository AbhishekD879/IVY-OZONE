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
class Test_C64749873_Verify_if_a_user_can_configure_a_backgroundimage_in_CMS_successfully(Common):
    """
    TR_ID: C64749873
    NAME: Verify if a user can configure a background
image in CMS successfully
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
        EXPECTED: a) User should be able to view Create super button CTA.
        EXPECTED: b) Existing super buttons should be displayed.
        EXPECTED: c) Title, content, segment(s),segment(s) exclusion,Enabled, Highlights, EDP, sports, display from, display to,Remove and Edit Columns should be displayed.
        """
        pass

    def test_003_upload_surface_bet_imageslogos_in_cms_from_image_manager(self):
        """
        DESCRIPTION: Upload Surface bet images/logos in CMS from image manager
        EXPECTED: background image should be changed for given surface bets.
        """
        pass

    def test_004_verify_by_entering__all_mandatory_feilds_and_click_create_cta(self):
        """
        DESCRIPTION: Verify by entering  all mandatory feilds and click Create CTA
        EXPECTED: Upon Clicking Create CTA ,new surface bet module should be created and appended at the end of the list of existing segment-specific configurations by default and allow reordering.
        """
        pass
