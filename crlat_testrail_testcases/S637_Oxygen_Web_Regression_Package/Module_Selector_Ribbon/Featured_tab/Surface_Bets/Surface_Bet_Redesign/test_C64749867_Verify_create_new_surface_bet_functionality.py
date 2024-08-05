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
class Test_C64749867_Verify_create_new_surface_bet_functionality(Common):
    """
    TR_ID: C64749867
    NAME: Verify create new surface bet functionality
    DESCRIPTION: This test case verifies the CMS configurations for surface bet
    PRECONDITIONS: User should have CMS admin access
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_click_on_surface_bet_link(self):
        """
        DESCRIPTION: Click on surface bet link.
        EXPECTED: a) User should be able to view Create super button CTA.
        EXPECTED: b) Existing super buttons should be displayed.
        EXPECTED: c) Title, content, segment(s),segment(s) exclusion,Enabled, Highlights, EDP, sports, display from, display to,Remove and Edit Columns should be displayed.
        """
        pass

    def test_003_click_on_create_surface_bet_moduleverify_detail_page(self):
        """
        DESCRIPTION: Click on create surface bet module,Verify detail page
        EXPECTED: surface bet module detail page should be opened with existing fields and new radio buttons Universal ,Segment(s) inclusion.
        """
        pass

    def test_004_verify_by_entering__all_mandatory_feilds_and_click_create_cta(self):
        """
        DESCRIPTION: Verify by entering  all mandatory feilds and click Create CTA
        EXPECTED: Upon Clicking Create CTA ,new surface bet module should be created and appended at the end of the list of existing segment-specific configurations by default and allow reordering.
        """
        pass
