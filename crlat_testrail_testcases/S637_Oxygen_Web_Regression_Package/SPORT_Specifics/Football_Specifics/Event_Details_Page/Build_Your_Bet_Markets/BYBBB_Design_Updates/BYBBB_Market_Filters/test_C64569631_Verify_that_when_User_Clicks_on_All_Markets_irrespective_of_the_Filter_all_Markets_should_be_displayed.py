import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569631_Verify_that_when_User_Clicks_on_All_Markets_irrespective_of_the_Filter_all_Markets_should_be_displayed(Common):
    """
    TR_ID: C64569631
    NAME: Verify that when User Clicks on All Markets  irrespective of the Filter all Markets  should be displayed
    DESCRIPTION: This test case verifies the display of all markets irrespective of the filter they are tagged to
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_gt_edp_gt_build_your_bet_bet_builder(self):
        """
        DESCRIPTION: Navigate to Football &gt; EDP &gt; Build Your Bet/ Bet Builder
        EXPECTED: * Bet Beuilder / Build Your Bet markets should be displayed
        """
        pass

    def test_003_validate_the_display_of_all_markets_section(self):
        """
        DESCRIPTION: Validate the display of all Markets section
        EXPECTED: * By default All Markets filter should be selected
        EXPECTED: * First Market should be expanded by default
        EXPECTED: * All the Markets should be displayed even though they are tagged to Team Bets, Player Bets, Popular Markets filter in CMS
        """
        pass
