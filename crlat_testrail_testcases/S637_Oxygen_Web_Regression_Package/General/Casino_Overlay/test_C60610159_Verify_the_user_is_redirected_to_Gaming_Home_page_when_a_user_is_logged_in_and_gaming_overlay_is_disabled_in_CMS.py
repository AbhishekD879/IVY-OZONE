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
class Test_C60610159_Verify_the_user_is_redirected_to_Gaming_Home_page_when_a_user_is_logged_in_and_gaming_overlay_is_disabled_in_CMS(Common):
    """
    TR_ID: C60610159
    NAME: Verify the user is redirected to Gaming Home page when a user is logged in and gaming overlay is disabled in CMS
    DESCRIPTION: 
    PRECONDITIONS: Pre- Requisite:
    PRECONDITIONS: Gaming Overlay must be disable in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_url_in_mobile_web(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL in mobile web
        EXPECTED: Ladbrokes/Coral URL should be launched
        """
        pass

    def test_002_click_on_login_and_fill_in_the_login_details(self):
        """
        DESCRIPTION: Click on Login and fill in the login details
        EXPECTED: Login should be successful.
        """
        pass

    def test_003_gaming_overlay_is_disabled_in_cms(self):
        """
        DESCRIPTION: Gaming Overlay is disabled in CMS
        EXPECTED: Gaming Overlay should be disabled
        """
        pass

    def test_004_click_on_gaming_icon(self):
        """
        DESCRIPTION: Click on Gaming Icon
        EXPECTED: User should be navigated to the gaming home page
        """
        pass

    def test_005_click_on_any_game(self):
        """
        DESCRIPTION: Click on any Game
        EXPECTED: User should be redirected to the appropriate games page
        """
        pass
