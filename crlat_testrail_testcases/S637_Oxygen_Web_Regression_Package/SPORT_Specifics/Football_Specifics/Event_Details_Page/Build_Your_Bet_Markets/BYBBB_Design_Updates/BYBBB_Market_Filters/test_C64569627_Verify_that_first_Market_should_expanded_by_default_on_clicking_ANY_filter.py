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
class Test_C64569627_Verify_that_first_Market_should_expanded_by_default_on_clicking_ANY_filter(Common):
    """
    TR_ID: C64569627
    NAME: Verify that first Market should expanded by default on clicking ANY filter
    DESCRIPTION: This test case verifies the display of Market Expanded in all filters
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: Atleast one or more Markets should be configured in CMS - Popular Market enabled , Market Type - Team Bets and player Bets
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

    def test_003_click_on_bybbb(self):
        """
        DESCRIPTION: Click on BYB/BB
        EXPECTED: * BYB/BB should be displayed with all the Markets
        EXPECTED: * Market label should be displayed
        EXPECTED: * Description should be displayed below Market label - as configured in CMS
        EXPECTED: * Four Filters should be displayed - All Markets, Popular Markets , Player Bets, Team Bets
        EXPECTED: * All Markets should be selected by default - First Market should be expanded
        """
        pass

    def test_004_switch_between_the_filters___validate_the_display_of_the_markets(self):
        """
        DESCRIPTION: Switch between the filters - Validate the display of the Markets
        EXPECTED: **Popular Market**
        EXPECTED: First Market should be expanded by default
        EXPECTED: **Player Bets**
        EXPECTED: First Market should be expanded by default
        EXPECTED: **Team Bets**
        EXPECTED: First Market should be expanded by default
        """
        pass
