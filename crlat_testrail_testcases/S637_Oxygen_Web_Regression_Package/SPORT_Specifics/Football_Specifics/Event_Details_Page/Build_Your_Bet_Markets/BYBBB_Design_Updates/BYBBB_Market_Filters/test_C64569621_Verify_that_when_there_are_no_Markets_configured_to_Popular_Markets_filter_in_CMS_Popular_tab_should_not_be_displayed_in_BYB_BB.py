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
class Test_C64569621_Verify_that_when_there_are_no_Markets_configured_to_Popular_Markets_filter_in_CMS_Popular_tab_should_not_be_displayed_in_BYB_BB(Common):
    """
    TR_ID: C64569621
    NAME: Verify that when there are no Markets configured to Popular Markets filter in CMS, Popular tab should not be displayed in BYB/BB
    DESCRIPTION: This test case verifies that Popular Markets filter tab is not displayed when there are NO markets configured in CMS
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: In CMS &gt; BYB &gt; BYB Markets - Popular Markets should not be enabled for any of the Market
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
        EXPECTED: EDP page should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB page should be displayed with all the markets
        """
        pass

    def test_004_validate_the_display_of_popular_markets(self):
        """
        DESCRIPTION: Validate the display of Popular Markets
        EXPECTED: * Popular Markets filter should NOT be displayed
        EXPECTED: * All Markets, Player Bets, Team Bets should be displayed
        """
        pass
