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
class Test_C64569622_Verify_that_CMS_user_can_modify_the_filters_for_ANY_market(Common):
    """
    TR_ID: C64569622
    NAME: Verify that CMS user can modify the filters for ANY market
    DESCRIPTION: This test case verifies that CMS user can modify Market filters at any time and the same changes are reflected in FE
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: User should have access to CMS
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

    def test_003_validate_the_markets_displayed_in_bybbb_tab(self):
        """
        DESCRIPTION: Validate the Markets displayed in BYB/BB tab
        EXPECTED: * Four Filters - All Markets , Popular Markets , Player Bets , Team Bets should be displayed
        """
        pass

    def test_004_change_popular_marketpick_any_market_displayed_under_popular_market_and_in_cms_change_it___disable_the_popular_market_check_box(self):
        """
        DESCRIPTION: Change **Popular Market**
        DESCRIPTION: Pick any Market displayed under Popular Market and in CMS change it - Disable the Popular Market Check box
        EXPECTED: * That Market should no longer be displayed under Popular Markets tab
        EXPECTED: * Make sure that Market is still displayed under All Markets tab and no change in it
        """
        pass

    def test_005_change_team_betspick_any_market_displayed_under_team_bets_and_in_cms_change_it___market_type_to_na(self):
        """
        DESCRIPTION: Change **Team Bets**
        DESCRIPTION: Pick any Market displayed under Team Bets and in CMS change it - Market Type to N/A
        EXPECTED: * That Market should no longer be displayed under Team Bets tab
        EXPECTED: * Make sure that Market is still displayed under All Markets tab and no change in it
        """
        pass

    def test_006_change_player_betspick_any_market_displayed_under_player_bets_and_in_cms_change_it___market_type_to_na(self):
        """
        DESCRIPTION: Change **Player Bets**
        DESCRIPTION: Pick any Market displayed under Player Bets and in CMS change it - Market type to N/A
        EXPECTED: * That Market should no longer be displayed under Player Bets tab
        EXPECTED: * Make sure that Market is still displayed under All Markets tab and no change in it
        """
        pass

    def test_007_change_player_bets_to_team_betspick_any_market_displayed_under_player_bets_and_in_cms_change_it___market_type_to_team_bets(self):
        """
        DESCRIPTION: Change **Player Bets** to **Team Bets**
        DESCRIPTION: Pick any Market displayed under Player Bets and in CMS change it - Market type to Team Bets
        EXPECTED: * That Market should no longer be displayed under Player Bets tab
        EXPECTED: * That Market should be displayed under Team Bets tab
        EXPECTED: * Make sure that Market is still displayed under All Markets tab and no change in it
        """
        pass

    def test_008_change_team_bets_to_player_betspick_any_market_displayed_under_team_bets_and_in_cms_change_it___market_type_to_player_bets(self):
        """
        DESCRIPTION: Change **Team Bets** to **Player Bets**
        DESCRIPTION: Pick any Market displayed under Team Bets and in CMS change it - Market type to Player Bets
        EXPECTED: * That Market should no longer be displayed under Team Bets tab
        EXPECTED: * That Market should be displayed under Player Bets tab
        EXPECTED: * Make sure that Market is still displayed under All Markets tab and no change in it
        """
        pass
