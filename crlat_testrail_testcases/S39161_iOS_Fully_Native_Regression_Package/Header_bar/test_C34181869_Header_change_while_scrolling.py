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
class Test_C34181869_Header_change_while_scrolling(Common):
    """
    TR_ID: C34181869
    NAME: Header change while scrolling
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

    def test_003_remove_selection_and_scroll_to_the_top(self):
        """
        DESCRIPTION: Remove selection and scroll to the top
        EXPECTED: App main screen appears with initial header bar
        """
        pass

    def test_004_scroll_down_and_add_some_selection(self):
        """
        DESCRIPTION: Scroll down and add some selection
        EXPECTED: Scrolled header is shown and stick to the top
        """
        pass

    def test_005_scroll_to_top_again(self):
        """
        DESCRIPTION: Scroll to top again
        EXPECTED: Scrolled header bar is shown
        """
        pass

    def test_006_remove_selection_and_scroll_top_and_and_down(self):
        """
        DESCRIPTION: Remove selection and scroll top and and down
        EXPECTED: Header changed to Initial
        """
        pass
