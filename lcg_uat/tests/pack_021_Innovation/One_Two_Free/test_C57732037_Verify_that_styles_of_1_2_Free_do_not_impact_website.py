import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


# @pytest.mark.tst2  # one two free is not available in lower env
# @pytest.mark.stg2  # one two free is not available in lower env
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732037_Verify_that_styles_of_1_2_Free_do_not_impact_website(Common):
    """
    TR_ID: C57732037
    NAME: Verify that styles of 1-2-Free do not impact website
    DESCRIPTION: This test case verifies that styles of 1-2-Free do not impact website
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    """
    keep_browser_open = True

    def test_001_open_the_ladbrokescoral_website(self):
        """
        DESCRIPTION: Open the Ladbrokes/Coral website.
        EXPECTED: The website is opened
        """
        self.site.login(username=tests.settings.default_username)

    def test_002_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link
        EXPECTED: '1-2-Free' is succssefuly opened and displayed
        """
        self.navigate_to_page('1-2-free')
        try:
            self.__class__.one_two_free = self.site.one_two_free.one_two_free_welcome_screen
        except VoltronException:
            self.__class__.one_two_free = self.site.one_two_free.one_two_free_current_screen
        self.assertTrue(self.one_two_free, msg='"1-2-Free" welcome/current screen is not displayed')

    def test_003_close_1_2_free(self):
        """
        DESCRIPTION: Close '1-2-Free'
        EXPECTED: '1-2-Free' is succssefuly closed
        """
        if self.device_type == 'desktop':
            self.one_two_free.back_icon.click()
        else:
            try:
                self.one_two_free.cancel_button.click()
            except VoltronException:
                self.one_two_free.close.click()

    def test_004_open_the_homepage_and_check_if_any_styles_and_functionality_do_not_impact_website(self):
        """
        DESCRIPTION: Open the homepage and check if any styles and functionality do not impact website
        EXPECTED: - Spinner has NOT disappeared before featured data was loaded
        EXPECTED: - NO empty black screen instead of displaying spinner or featured data
        EXPECTED: - All functionality on the website works correctly as before opening '1-2-Free'
        """
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_content_state('homepage'), msg='User has not re-directed to homepage')
