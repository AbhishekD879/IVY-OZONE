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
class Test_C57732033_Verify_the_error_handling_of_the_long_loading_of_the_application(Common):
    """
    TR_ID: C57732033
    NAME: Verify the error handling of the long loading of the application
    DESCRIPTION: This test case verifies the error handling of the long loading (20+ seconds) of the application.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The User is logged in https://m.ladbrokes.com.
    PRECONDITIONS: 2. The Quick link 'Play 1-2-FREE predictor and win £150' is available on the Home page / Football page.
    """
    keep_browser_open = True

    def test_001_set_slow_3g_in_the_network_tab_of_the_devtools(self):
        """
        DESCRIPTION: Set 'Slow 3G' in the Network tab of the DevTools.
        EXPECTED: The 'Slow 3G' option is successfully set.
        """
        pass

    def test_002_open_the_website__app(self):
        """
        DESCRIPTION: Open the website / app.
        EXPECTED: The website / app is opened.
        """
        pass

    def test_003_tap_on_the_1_2_free_link(self):
        """
        DESCRIPTION: Tap on the '1-2-Free' link.
        EXPECTED: The 'This week' tab is opened.
        EXPECTED: The Splash page is opened (only on mobile).
        """
        pass

    def test_004_double_tap_on_the_play_now_button_only_on_mobile(self):
        """
        DESCRIPTION: Double tap on the 'Play now' button (only on mobile).
        EXPECTED: The 'This week' tab is opened (only on mobile).
        """
        pass

    def test_005_quickly_set_offline_in_the_network_tab_of_the_devtools(self):
        """
        DESCRIPTION: Quickly set 'Offline' in the Network tab of the DevTools.
        EXPECTED: The 'Offline' option is successfully set.
        """
        pass

    def test_006_wait_for_20plus_seconds(self):
        """
        DESCRIPTION: Wait for 20+ seconds.
        EXPECTED: The Error message with 'Go back' button is displayed.
        """
        pass

    def test_007_tap_on_the_go_back_button(self):
        """
        DESCRIPTION: Tap on the 'Go back' button.
        EXPECTED: The User is redirected to the Home page / Football page.
        """
        pass
