import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870405_Verify_Coral_site_logo_display_and_navigation(Common):
    """
    TR_ID: C44870405
    NAME: Verify Coral site logo display and navigation
    DESCRIPTION: Coral logo should be visible in it's respective header on all pages of the website and user should be able to click on the logo and navigate to the homepage via this logo.
    PRECONDITIONS: Coral logo is available in logged in and logged out state.
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        pass

    def test_002_click_on_in_play_via_header_links(self):
        """
        DESCRIPTION: Click on In-Play via header links
        EXPECTED: In-play page displayed and Coral logo is displayed in header at the top.
        """
        pass

    def test_003_click_on_coral_logo(self):
        """
        DESCRIPTION: Click on Coral logo.
        EXPECTED: User directed back to the homepage.
        """
        pass

    def test_004_click_on_a_sport_in_the_a_z_sports_menu_list(self):
        """
        DESCRIPTION: Click on a sport in the A-Z Sports menu list.
        EXPECTED: Respective sport displayed and Coral logo is displayed in header at the top.
        """
        pass

    def test_005_click_on_coral_logo(self):
        """
        DESCRIPTION: Click on Coral logo.
        EXPECTED: User directed back to the homepage.
        """
        pass

    def test_006_repeat_above_steps_for_a_range_of_areas_on_the_site(self):
        """
        DESCRIPTION: Repeat above steps for a range of areas on the site
        EXPECTED: Respective pages displayed and Coral logo is displayed in header at the top. User should always be able to direct back to the homepage by clicking on the Coral site logo.
        """
        pass
