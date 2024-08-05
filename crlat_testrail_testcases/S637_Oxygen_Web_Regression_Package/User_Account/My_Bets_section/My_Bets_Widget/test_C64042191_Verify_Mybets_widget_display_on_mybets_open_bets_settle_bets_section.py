import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C64042191_Verify_Mybets_widget_display_on_mybets_open_bets_settle_bets_section(Common):
    """
    TR_ID: C64042191
    NAME: Verify Mybets widget display on mybets (open bets & settle bets) section
    DESCRIPTION: Verify Mybets widget display on mybets (open bets & settle bets) section
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User should enable mybets toggle on in system-configuration/structure
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_login_as_cms_admin(self):
        """
        DESCRIPTION: Login as CMS admin
        EXPECTED: User should successful login to CMS
        """
        pass

    def test_002_navigate_to_system_configuration_and_enable_mybets_widget(self):
        """
        DESCRIPTION: Navigate to system configuration and enable mybets widget
        EXPECTED: user should able to navigate and enable mybets section
        """
        pass

    def test_003_load_the_app_or_url(self):
        """
        DESCRIPTION: Load the app or URL
        EXPECTED: "User should be able to launch the URL
        EXPECTED: Mobile App: User should able to launch the app"
        """
        pass

    def test_004_navigate_to_football_section_and_place_5a_side_bets(self):
        """
        DESCRIPTION: Navigate to football section and place 5a side bets
        EXPECTED: User should able to place 5a side bets
        """
        pass

    def test_005_navigate_to_open_bets_section_and_verify_the_my_bets_leaderboard_widget_is_displayed(self):
        """
        DESCRIPTION: Navigate to open bets section and verify the my bets leaderboard widget is displayed
        EXPECTED: Mybets widget is displayed in open bets section
        """
        pass
