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
class Test_C60092378_Verify_the_navigation_on_tapping_Inline_banner(Common):
    """
    TR_ID: C60092378
    NAME: Verify the navigation on tapping Inline banner
    DESCRIPTION: This test case verifies that when user taps on the Inline banner , User is navigated to 5 A side pitch view for that match (respective Football event)
    PRECONDITIONS: 1: Inline banner for 5 A side should be enabled in CMS
    PRECONDITIONS: 2: Title, description should be added for Inline banner in CMS
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_url_app(self):
        """
        DESCRIPTION: Launch Ladbrokes URL/ app
        EXPECTED: User should be able to launch the app/URL successfully
        """
        pass

    def test_002_navigate_to_football_edp_which_has_5_a_side_available__check_pre_conditions_for_5_a_side(self):
        """
        DESCRIPTION: Navigate to Football EDP which has 5 A side available ( Check Pre-conditions for 5 A side)
        EXPECTED: User should be able to view Football EDP
        """
        pass

    def test_003_validate_the_inline_banner_display(self):
        """
        DESCRIPTION: Validate the Inline banner display
        EXPECTED: User should be able to view the Inline banner above Market collection tab depending on the postion set in CMS (If position is set to 0 then Iline banner will be displayed on the first market tab and if we set Position=3 then it will sit below market number 3. )
        """
        pass

    def test_004_tap_on_the_inline_banner_and_validate_the_user_navigation(self):
        """
        DESCRIPTION: Tap on the Inline banner and Validate the user navigation
        EXPECTED: User should be navigated to 5 A side pitch view for that football event
        """
        pass

    def test_005_build_5_a_side_and_place_bet(self):
        """
        DESCRIPTION: Build 5 A side and Place bet
        EXPECTED: User should be able to build a 5 A Side team and place bet successfully
        """
        pass

    def test_006_verify_the_ga_tracking_is_there_for_inline_banner_tap(self):
        """
        DESCRIPTION: Verify the GA tracking is there for Inline banner tap
        EXPECTED: 
        """
        pass
