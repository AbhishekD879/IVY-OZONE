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
class Test_C26832985_Header_bar_stick_to_top_if_user_added_some_selection_before_scrolling(Common):
    """
    TR_ID: C26832985
    NAME: Header bar stick to top if user added some selection before scrolling
    DESCRIPTION: TC verifies that header bar stick to top if user added some selection
    PRECONDITIONS: App is installed
    PRECONDITIONS: Some user should exist
    """
    keep_browser_open = True

    def test_001_start_the_app_and_add_some_selection_to_betslip(self):
        """
        DESCRIPTION: Start the app and add some selection to betslip
        EXPECTED: App main screen appears with initial header bar
        """
        pass

    def test_002_scroll_down(self):
        """
        DESCRIPTION: Scroll down
        EXPECTED: Header bar stick to top
        """
        pass

    def test_003_scroll_to_top_again(self):
        """
        DESCRIPTION: Scroll to top again
        EXPECTED: Header bar stick to top
        """
        pass

    def test_004_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Header bar stick to top
        """
        pass

    def test_005_scroll_down(self):
        """
        DESCRIPTION: Scroll down
        EXPECTED: Header bar stick to top
        """
        pass

    def test_006_scroll_to_top_again(self):
        """
        DESCRIPTION: Scroll to top again
        EXPECTED: Header bar stick to top
        """
        pass

    def test_007_login_and_repear_steps_1_6(self):
        """
        DESCRIPTION: Login and repear steps 1-6
        EXPECTED: Header bar beheves the same
        """
        pass
