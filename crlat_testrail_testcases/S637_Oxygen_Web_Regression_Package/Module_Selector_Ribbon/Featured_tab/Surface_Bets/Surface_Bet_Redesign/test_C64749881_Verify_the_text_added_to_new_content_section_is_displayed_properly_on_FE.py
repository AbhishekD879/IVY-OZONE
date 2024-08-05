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
class Test_C64749881_Verify_the_text_added_to_new_content_section_is_displayed_properly_on_FE(Common):
    """
    TR_ID: C64749881
    NAME: Verify the text added to new content section is displayed properly on FE
    DESCRIPTION: Testcase verifies the text added to new content section is displayed properly on FE
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

    def test_002_click_on_create_surface_bet(self):
        """
        DESCRIPTION: Click on create surface bet.
        EXPECTED: User should see one additional content textbox.
        """
        pass

    def test_003_enter_any_text_in_context_box(self):
        """
        DESCRIPTION: Enter any text in context box.
        EXPECTED: User should be able to use contect box.
        """
        pass

    def test_004_verify_if_text_added_to_new_content_section_is_displayed_properly_on_fe(self):
        """
        DESCRIPTION: Verify if text added to new content section is displayed properly on FE
        EXPECTED: text added to new content section should displayed properly on FE
        """
        pass
