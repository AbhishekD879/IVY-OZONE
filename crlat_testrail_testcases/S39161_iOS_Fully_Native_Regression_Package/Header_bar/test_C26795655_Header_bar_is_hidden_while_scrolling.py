import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C26795655_Header_bar_is_hidden_while_scrolling(Common):
    """
    TR_ID: C26795655
    NAME: Header bar is hidden while scrolling
    DESCRIPTION: TC verifies if header bar is hidden while scrolling
    PRECONDITIONS: App is installed
    """
    keep_browser_open = True

    def test_001_start_the_app(self):
        """
        DESCRIPTION: Start the app
        EXPECTED: App main screen appears
        """
        pass

    def test_002_scroll_down(self):
        """
        DESCRIPTION: Scroll down
        EXPECTED: Header bar disappear
        """
        pass

    def test_003_scroll_to_top_again(self):
        """
        DESCRIPTION: Scroll to top again
        EXPECTED: Header bar appears
        """
        pass

    def test_004_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Header bar is shown
        """
        pass

    def test_005_scroll_down(self):
        """
        DESCRIPTION: Scroll down
        EXPECTED: Header bar disappear
        """
        pass

    def test_006_scroll_to_top_again(self):
        """
        DESCRIPTION: Scroll to top again
        EXPECTED: Header bar is shown
        """
        pass

    def test_007_login_and_repeat_steps_1_6(self):
        """
        DESCRIPTION: Login and repeat steps 1-6
        EXPECTED: Header bar behaves the same
        """
        pass
