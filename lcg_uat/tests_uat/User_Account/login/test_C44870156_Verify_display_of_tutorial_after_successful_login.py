import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.crl_uat
@pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.medium
@pytest.mark.p2
@pytest.mark.mobile_only
@pytest.mark.user_account
@vtest
class Test_C44870156_Verify_display_of_tutorial_after_successful_login(Common):
    """
    TR_ID: C44870156
    NAME: Verify display of tutorial after successful login
    DESCRIPTION: Not applicable for DESKTOP
    PRECONDITIONS: Clear local storage and Download the app.
    PRECONDITIONS: Clear all the cookies for WEB
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Not applicable for DESKTOP
        PRECONDITIONS: Clear local storage and Download the app.
        PRECONDITIONS: Clear all the cookies for WEB
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.device.driver.implicitly_wait(5)

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: User is logged in and on the Homepage
        """
        self.site.login(async_close_banners=True)

    def test_002_check_home_tutorial_overlay_displaying(self):
        """
        DESCRIPTION: Check Home tutorial overlay displaying
        EXPECTED: Home tutorial displayed with arrows pointing to the following elements:
        EXPECTED: My bets ---> Cashout/Open bets/Bet history
        EXPECTED: Balance ---> Check your Balance
        EXPECTED: Avatar ---> Tap to open your My Account Menu
        EXPECTED: Betslip ---> Save bets to your Betslip
        """
        self.assertTrue(self.site.wait_for_tutorial_overlay(), msg='"Tutorial overlay" is not displayed')
        self.__class__.tutorial_overlay = self.site.tutorial_arrow_panel
        self.site.wait_for_tutorial_overlay()
        tutorial_overlay_elements = self.tutorial_overlay.tutorial_arrow_overlay
        tutorial_elements = []
        for element in tutorial_overlay_elements:
            tutorial_elements.append(' '.join(list(element.text.split('\n'))))
        self.assertEqual(tutorial_elements, vec.BMA.TUTORIAL_ELEMENTS,
                         msg=f'Actual text: "{tutorial_elements}" is not same as'
                             f'Expected text: "{vec.BMA.TUTORIAL_ELEMENTS}"')

    def test_003_scroll_down_to_see_the_close_tutorial_button(self):
        """
        DESCRIPTION: Scroll down to see the 'Close tutorial' button
        EXPECTED: 'Close' tab is present and when clicked > the tutorial is closed.
        """
        self.assertTrue(self.tutorial_overlay.text_panel.close_button.is_displayed(), msg='"close tutorial" '
                                                                                          'button not displayed')
        self.tutorial_overlay.text_panel.close_button.click()
        self.assertFalse(self.site.wait_for_tutorial_overlay(timeout=2), msg=f'"Tutorial overlay" is not closed')

    def test_004_navigate_to_football_page_and_check_football_tutorial(self):
        """
        DESCRIPTION: Navigate to Football page and check Football tutorial
        EXPECTED: Football tutorial is displayed with info about the FAVOURITES features.
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        self.__class__.football_overlay_panel = self.site.football_overlay
        self.site.wait_for_tutorial_overlay()
        football_tutorial_info = self.football_overlay_panel.football_tutorial
        football_tutorial_element = []
        for item in football_tutorial_info:
            football_tutorial_element.append(' '.join(list(item.text.split('\n'))))
        self.assertEqual(football_tutorial_element, vec.BMA.FOOTBALL_TUTORIAL_ELEMENTS,
                         msg=f'Actual text: "{football_tutorial_element}" is not same as'
                             f'Expected text: "{vec.BMA.FOOTBALL_TUTORIAL_ELEMENTS}"')

    def test_005_scroll_down_to_see_the_close_tutorial_button(self):
        """
        DESCRIPTION: Scroll down to see the 'Close tutorial' button
        EXPECTED: 'Close' tab is present and when clicked > the tutorial is closed.
        """
        self.assertTrue(self.site.football_overlay.close_football_tutorial.is_displayed(),
                        msg='"close tutorial" button not displayed')
        self.site.football_overlay.close_football_tutorial.click()
        self.assertFalse(self.site.wait_for_tutorial_overlay(timeout=2), msg='"Tutorial overlay" is not closed')
