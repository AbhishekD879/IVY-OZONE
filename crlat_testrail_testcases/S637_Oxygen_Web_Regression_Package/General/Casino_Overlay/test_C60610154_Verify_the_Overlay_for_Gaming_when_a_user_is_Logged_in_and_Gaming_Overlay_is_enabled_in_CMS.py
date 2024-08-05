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
class Test_C60610154_Verify_the_Overlay_for_Gaming_when_a_user_is_Logged_in_and_Gaming_Overlay_is_enabled_in_CMS(Common):
    """
    TR_ID: C60610154
    NAME: Verify the Overlay for Gaming when a user is Logged in and Gaming Overlay is enabled in CMS
    DESCRIPTION: 
    PRECONDITIONS: Pre- Requisite:
    PRECONDITIONS: Gaming Overlay must be enabled in CMS
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

    def test_003_gaming_overlay_is_enabled_in_cms(self):
        """
        DESCRIPTION: Gaming Overlay is enabled in CMS
        EXPECTED: Gaming Overlay should be enabled
        """
        pass

    def test_004_click_on_gaming_icon(self):
        """
        DESCRIPTION: Click on Gaming Icon
        EXPECTED: User should be navigated to gaming overlay page
        EXPECTED: Note: User can scroll up and down to view the list of games(The Close button and the header should be sticky).
        """
        pass

    def test_005_click_on_any_game(self):
        """
        DESCRIPTION: Click on any Game
        EXPECTED: User should be redirected to the appropriate game page.
        """
        pass

    def test_006_user_can_close_the_overlay_by_clicking_on_the_close_button(self):
        """
        DESCRIPTION: User can close the overlay by clicking on the Close button
        EXPECTED: User should be redirected to the appropriate page in which he is in previously
        EXPECTED: Note:
        EXPECTED: The page should not refresh
        """
        pass
