import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62700707_Verify_My_bets_widget_toggle_in_CMS(Common):
    """
    TR_ID: C62700707
    NAME: Verify My bets widget toggle in CMS
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
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

    def test_001_login_to_cms_with_valid_credentials(self):
        """
        DESCRIPTION: Login to CMS with valid credentials
        EXPECTED: User should be loggedin to CMS
        """
        pass

    def test_002_go_to_system_configurations__gt_fiveasideleaderboarwidget(self):
        """
        DESCRIPTION: Go to system configurations--&gt; FiveASideLeaderboarWidget
        EXPECTED: User should see FiveASideLeaderboarWidget
        """
        pass

    def test_003_enable_toggle(self):
        """
        DESCRIPTION: Enable toggle
        EXPECTED: Toggle should be enabled
        """
        pass

    def test_004_login_to_sportsbook_application_with_user_who_entered_into_any_contest(self):
        """
        DESCRIPTION: Login to sportsbook application with user who entered into any contest
        EXPECTED: User should be logged into sportsbook application
        """
        pass

    def test_005_go_to_my_bets_openbetssettledbets(self):
        """
        DESCRIPTION: Go to My bets openbets/settledbets
        EXPECTED: User should e navigated to My bets--&gt; openbets/settledbets
        """
        pass

    def test_006_observe_my_bets_widget_is_displayed(self):
        """
        DESCRIPTION: Observe My bets widget is displayed
        EXPECTED: My bets widget should be displayed
        """
        pass

    def test_007_go_to_cms_and_disable_toggle(self):
        """
        DESCRIPTION: Go to CMS and disable toggle
        EXPECTED: Toggle should be disabled
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass

    def test_009_refresh_my_bets_page_in_sportbook(self):
        """
        DESCRIPTION: Refresh my bets page in sportbook
        EXPECTED: My bets widget should be undisplayed
        """
        pass
