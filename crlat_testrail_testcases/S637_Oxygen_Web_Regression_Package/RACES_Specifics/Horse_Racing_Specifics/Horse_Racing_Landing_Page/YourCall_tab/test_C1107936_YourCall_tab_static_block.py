import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1107936_YourCall_tab_static_block(Common):
    """
    TR_ID: C1107936
    NAME: YourCall tab static block
    DESCRIPTION: This test case verifies YourCall tab with static block and twitter button
    PRECONDITIONS: * The user is on Coral homepage
    PRECONDITIONS: * CMS contains configuration for the static block of YOURCALL tab (Your Call > Your Call Static Block > select "yourcall-racing" from the grid): html markup for text and "TWEET NOW" button with link
    """
    keep_browser_open = True

    def test_001_navigate_on_the_horse_racing_tab(self):
        """
        DESCRIPTION: Navigate on the Horse racing tab
        EXPECTED: When the page is loaded YOURCALL tab is present
        """
        pass

    def test_002_click_on_the_yourcall_tab(self):
        """
        DESCRIPTION: Click on the YOURCALL tab
        EXPECTED: The tab is shown as per design:
        EXPECTED: * configurable (on CMS) static text ('#YourCall' is highlighted with different color)
        EXPECTED: * "TWEET NOW" button
        """
        pass

    def test_003_verify_the_position_of_the_tweet_now_button(self):
        """
        DESCRIPTION: Verify the position of the "TWEET NOW" button
        EXPECTED: * On mobile the button is located under the static block
        EXPECTED: * On desktop the button is located next to the static block
        """
        pass

    def test_004_click_on_the_tweet_now_button(self):
        """
        DESCRIPTION: Click on the "TWEET NOW" button
        EXPECTED: Coral twitter account is opened
        EXPECTED: https://mobile.twitter.com/Coral (configured on CMS)
        """
        pass
