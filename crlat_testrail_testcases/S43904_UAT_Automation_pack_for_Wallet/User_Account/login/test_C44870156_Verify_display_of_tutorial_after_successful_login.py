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
class Test_C44870156_Verify_display_of_tutorial_after_successful_login(Common):
    """
    TR_ID: C44870156
    NAME: Verify display of tutorial after successful login
    DESCRIPTION: Not applicable for DESKTOP
    PRECONDITIONS: Clear local storage and Download the app.
    PRECONDITIONS: Clear all the cookies for WEB
    """
    keep_browser_open = True

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: User is logged in and on the Homepage
        """
        pass

    def test_002_check_home_tutorial_overlay_displaying(self):
        """
        DESCRIPTION: Check Home tutorial overlay displaying
        EXPECTED: Home tutorial displayed with arrows pointing to the following elements:
        EXPECTED: My bets ---> Cashout/Open bets/Bet history
        EXPECTED: Balance ---> Check your Balance
        EXPECTED: Avatar ---> Tap to open your My Account Menu
        EXPECTED: Betslip ---> Save bets to your Betslip
        """
        pass

    def test_003_scroll_down_to_see_the_close_tutorial_button(self):
        """
        DESCRIPTION: Scroll down to see the 'Close tutorial' button
        EXPECTED: 'Close' tab is present and when clicked > the tutorial is closed.
        """
        pass

    def test_004_navigate_to_football_page_and_check_football_tutorial(self):
        """
        DESCRIPTION: Navigate to Football page and check Football tutorial
        EXPECTED: Football tutorial is displayed with info about the FAVOURITES features.
        """
        pass

    def test_005_scroll_down_to_see_the_close_tutorial_button(self):
        """
        DESCRIPTION: Scroll down to see the 'Close tutorial' button
        EXPECTED: 'Close' tab is present and when clicked > the tutorial is closed.
        """
        pass
