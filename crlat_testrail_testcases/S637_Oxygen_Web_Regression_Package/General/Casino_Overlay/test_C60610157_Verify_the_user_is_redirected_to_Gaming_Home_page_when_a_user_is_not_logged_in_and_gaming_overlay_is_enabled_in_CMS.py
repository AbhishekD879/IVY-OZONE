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
class Test_C60610157_Verify_the_user_is_redirected_to_Gaming_Home_page_when_a_user_is_not_logged_in_and_gaming_overlay_is_enabled_in_CMS(Common):
    """
    TR_ID: C60610157
    NAME: Verify the user is redirected to Gaming Home page when a user is not logged in and gaming overlay is enabled in CMS
    DESCRIPTION: 
    PRECONDITIONS: Pre Requisite:
    PRECONDITIONS: Gaming Overlay must be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_url_in_mobile_web(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL in mobile web
        EXPECTED: Ladbrokes/Coral URL should be launched
        """
        pass

    def test_002_gaming_overlay_is_enabled_in_cms(self):
        """
        DESCRIPTION: Gaming Overlay is enabled in CMS
        EXPECTED: Gaming Overlay should be enabled
        """
        pass

    def test_003_click_on_gaming_icon(self):
        """
        DESCRIPTION: Click on Gaming Icon
        EXPECTED: User should be navigated to gaming home page
        """
        pass
