import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28579_Verify_Bet_Now_button(Common):
    """
    TR_ID: C28579
    NAME: Verify 'Bet Now' button
    DESCRIPTION: This test case verifies 'Bet Now' button on Football Jackpot page
    PRECONDITIONS: Football Jackpot pool is available
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened with 15 events available
        EXPECTED: *   Each event has 3 buttons
        """
        pass

    def test_004_go_tobet_placement_section(self):
        """
        DESCRIPTION: Go to  Bet Placement section
        EXPECTED: 'Bet Now' button is disabled by default
        """
        pass

    def test_005_make_less_than_15_selections(self):
        """
        DESCRIPTION: Make less than 15 selections
        EXPECTED: 'Bet Now' button remains disabled
        """
        pass

    def test_006_make_1_selection_fromeach_of_15events(self):
        """
        DESCRIPTION: Make 1 selection from **each of 15 **events
        EXPECTED: 'Bet Now' button becomes enabled
        """
        pass

    def test_007_makemorethan_15_selections_at_least_1_from_each_event(self):
        """
        DESCRIPTION: Make **more** than 15 selections (at least 1 from each event)
        EXPECTED: 'Bet Now' button remains enabled
        """
        pass
