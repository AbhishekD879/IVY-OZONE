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
class Test_C57732001_Verify_Pop_Up_of_iOS_App_toggle_on_other_platforms(Common):
    """
    TR_ID: C57732001
    NAME: Verify Pop-Up of iOS App toggle on other platforms
    DESCRIPTION: This test case verifies Pop-Up of iOS App toggle on other platforms
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. iOS App toggle is Turned On from Qubit CMS
    """
    keep_browser_open = True

    def test_001_tap_on_the_quick_link_play_1_2_free_on_homepage_or_football_sports_pageuse_android_wrapper(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on Homepage or Football sports page
        DESCRIPTION: (Use Android wrapper)
        EXPECTED: 1-2-Free successfully opened without Pop-Up related to OS App toggle
        """
        pass

    def test_002_tap_on_the_quick_link_play_1_2_free_on_homepage_or_football_sports_pageuse_mobile_chrome_browser(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on Homepage or Football sports page
        DESCRIPTION: (Use mobile Chrome browser)
        EXPECTED: 1-2-Free successfully opened without Pop-Up related to OS App toggle
        """
        pass

    def test_003_tap_on_the_quick_link_play_1_2_free_on_homepage_or_football_sports_pageuse_mobile_safari_browser(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on Homepage or Football sports page
        DESCRIPTION: (Use mobile Safari browser)
        EXPECTED: 1-2-Free successfully opened without Pop-Up related to OS App toggle
        """
        pass
