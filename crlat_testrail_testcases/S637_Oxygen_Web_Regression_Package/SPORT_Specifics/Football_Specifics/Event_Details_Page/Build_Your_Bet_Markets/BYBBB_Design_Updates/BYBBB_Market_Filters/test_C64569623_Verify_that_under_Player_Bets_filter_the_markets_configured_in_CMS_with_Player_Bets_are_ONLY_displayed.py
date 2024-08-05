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
class Test_C64569623_Verify_that_under_Player_Bets_filter_the_markets_configured_in_CMS_with_Player_Bets_are_ONLY_displayed(Common):
    """
    TR_ID: C64569623
    NAME: Verify that under 'Player Bets' filter the markets configured in CMS with Player Bets are ONLY displayed
    DESCRIPTION: This test case verifies the display of Player Bets tab
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: In CMS &gt; BYB . BYB Markets - Atleast one or more markets should be configured for Player Bets
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_navigate_to_bybbb___player_bets_filter(self):
        """
        DESCRIPTION: Navigate to BYB/BB - Player Bets filter
        EXPECTED: * User should be able to click on Player Bets filter
        EXPECTED: * Markets should be displayed under player Bets
        EXPECTED: * Only those Markets which are configured in CMS with Market type as 'Player Bets' should be displayed
        """
        pass
