import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870408_Verify_A_Z_Sports_Menu(Common):
    """
    TR_ID: C44870408
    NAME: Verify A-Z Sports Menu
    DESCRIPTION: Verification of the A-Z Sports menu component.
    PRECONDITIONS: A-Z Sports menu is visible in logged in or logged out status.
    """
    keep_browser_open = True

    def test_001_open_httpsmsportsladbrokescom_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://msports.ladbrokes.com on Chrome browser.
        EXPECTED: https://msports.ladbrokes.com displayed on Chrome browser.
        """
        pass

    def test_002_verify_multiple_sports_displayed_in_a_z_sports_menu_on_left_hand_side(self):
        """
        DESCRIPTION: Verify multiple sports displayed in A-Z sports menu on left hand side.
        EXPECTED: Multiple sports displayed in A-Z sports menu on left hand side.
        """
        pass

    def test_003_verify_sports_are_available_with_respective_icon(self):
        """
        DESCRIPTION: Verify sports are available with respective icon.
        EXPECTED: Sports are available with respective icon.
        """
        pass

    def test_004_click_on_tennis(self):
        """
        DESCRIPTION: Click on Tennis
        EXPECTED: Tennis landing page is displayed with highlighted background for displayed page in grey.
        """
        pass

    def test_005_verify_web_page_breadcrumbs_below_tennis_header_bar_with_correct_page_displayed(self):
        """
        DESCRIPTION: Verify web page breadcrumbs below Tennis header bar with correct page displayed.
        EXPECTED: Web page breadcrumbs displayed below Tennis header bar with correct page displayed
        """
        pass

    def test_006_verify_above_scenario_on_all_a_z_sports_visible(self):
        """
        DESCRIPTION: Verify above scenario on all A-Z sports visible
        EXPECTED: All sports display respective page, url, breadcrumbs.
        """
        pass
