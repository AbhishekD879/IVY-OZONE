import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_driver


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.adhoc_suite
@pytest.mark.adhoc24thJan24
@pytest.mark.back_button
@pytest.mark.desktop
@pytest.mark.navigation
@pytest.mark.other
@vtest
class Test_C66017358_Verify_the_Sports_Browser_Back_Button(Common):
    """
    TR_ID: C66017358
    NAME: Verify the Sports Browser Back Button
    DESCRIPTION: Verify the Sports URL by using browser back button
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_000_launch_the_front_end_application(self):
        """
        DESCRIPTION: Launch the front end application
        EXPECTED: Homepage is loaded successfully
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User navigated to Football landing page successfully
        """
        self.site.open_sport('Football')
        self.site.wait_content_state(state_name='football')

    def test_002_click_on_browser_back_button(self):
        """
        DESCRIPTION: Click on browser back button
        EXPECTED: User should navigates to Homepage(previously opened page)
        """
        web_driver = get_driver()
        web_driver.back()
        homepage = self.site.wait_content_state('Homepage')
        self.assertTrue(homepage, msg='User not on home page')

    def test_003_navigate_to_football_page_again(self):
        """
        DESCRIPTION: Navigate to Football page again
        EXPECTED: User navigated to Football landing page successfully
        """
        self.site.open_sport('Football')
        self.site.wait_content_state(state_name='football')

    def test_004_next_navigate_to_tennis_page(self):
        """
        DESCRIPTION: Next Navigate to Tennis page
        EXPECTED: User navigated to Tennis landing page successfully
        """
        web_driver = get_driver()
        web_driver.get('https://beta-sports.coral.co.uk/sport/tennis')
        self.site.wait_content_state(state_name='tennis')

    def test_005_click_on_browser_back_button(self):
        """
        DESCRIPTION: Click on browser back button
        EXPECTED: User should navigates to Football page(previously opened page)
        """
        web_driver = get_driver()
        web_driver.back()
        football_slp = self.site.wait_content_state('football')
        self.assertTrue(football_slp, msg='User not on football slp page')
        self.navigate_to_page('/')


    def test_006_repeat_above_all_steps_after_logging_to_the_front_end_application(self):
        """
        DESCRIPTION: Repeat above all steps After logging to the front end application
        EXPECTED: The results should be as above.
        """
        self.site.login()
        self.test_001_navigate_to_football_page()
        self.test_002_click_on_browser_back_button()
        self.test_003_navigate_to_football_page_again()
        self.test_004_next_navigate_to_tennis_page()
        self.test_005_click_on_browser_back_button()


