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
class Test_C64749877_Verify_the_content_header_text_is_displayed_in_white_color_when_BG_image_is_uploaded(Common):
    """
    TR_ID: C64749877
    NAME: Verify the content header & text is displayed in white color when BG image is uploaded
    DESCRIPTION: Testcase verifies if content header & text is displayed in white color when BG image is uploaded
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

    def test_002_upload_surface_bet_imageslogos_in_cms_from_image_manager(self):
        """
        DESCRIPTION: Upload Surface bet images/logos in CMS from image manager.
        EXPECTED: Background image should be uploaded in FE.
        """
        pass

    def test_003_verify_the_content_header__text_colour_displayed_in_fe_when_bg_image_is_uploaded(self):
        """
        DESCRIPTION: Verify the content header & text colour displayed in FE when BG image is uploaded
        EXPECTED: Content header & text should be displayed in white color when BG image is uploaded
        """
        pass

    def test_004_verify_the_content_header__text_colour_displayed_in_fe_when_bg_image_is_not_uploaded(self):
        """
        DESCRIPTION: Verify the content header & text colour displayed in FE when BG image is not uploaded
        EXPECTED: Content header & text should be displayed in default Black color when BG image is not uploaded
        """
        pass
