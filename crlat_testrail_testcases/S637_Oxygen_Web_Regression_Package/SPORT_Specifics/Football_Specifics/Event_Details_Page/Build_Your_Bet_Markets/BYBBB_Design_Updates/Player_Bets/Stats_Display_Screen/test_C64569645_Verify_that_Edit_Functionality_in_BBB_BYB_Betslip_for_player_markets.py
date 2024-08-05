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
class Test_C64569645_Verify_that_Edit_Functionality_in_BBB_BYB_Betslip_for_player_markets(Common):
    """
    TR_ID: C64569645
    NAME: Verify that Edit Functionality in BBB/BYB Betslip for player markets
    DESCRIPTION: This test case verifies Edit Functionality in betslip for player market
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be Configure in CMS
    PRECONDITIONS: Goals
    PRECONDITIONS: Goals inside the box
    PRECONDITIONS: Goals outside the box
    PRECONDITIONS: Offsides
    PRECONDITIONS: Passes
    PRECONDITIONS: Shots
    PRECONDITIONS: Shots on target
    PRECONDITIONS: Shots outside the box
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Markets
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
        EXPECTED: * User should be navigated to EDP
        EXPECTED: * Build Your Bet /Bet Builder tab should be displayed
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: * BYB/BB tab should be displayed
        EXPECTED: * Filters should be displayed
        EXPECTED: * All Markets tab should be displayed by default
        """
        pass

    def test_004_click_on_any_of_the_player_market_either_from_all_markets_filter_or_player_bets_filtergoalsgoals_inside_the_boxgoals_outside_the_boxoffsidespassesshotsshots_on_targetshots_outside_the_box(self):
        """
        DESCRIPTION: Click on ANY of the Player Market either from All Markets filter or Player Bets filter
        DESCRIPTION: Goals
        DESCRIPTION: Goals inside the box
        DESCRIPTION: Goals outside the box
        DESCRIPTION: Offsides
        DESCRIPTION: Passes
        DESCRIPTION: Shots
        DESCRIPTION: Shots on target
        DESCRIPTION: Shots outside the box
        EXPECTED: * Market should be expanded
        EXPECTED: * Players should be displayed
        """
        pass

    def test_005_add_few_combinable_selections_to_bybbet_builder_to__dashboard_from_different_markets_accordions_and_add_them_to__betslip(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder to  Dashboard from different markets accordions and add them to  betslip
        EXPECTED: * Selected selections are highlighted within accordions and added to betslip
        """
        pass

    def test_006_verify_the_build_your_bet_for_coral_bet_builderfor_lads_click_on_dashboard_content_area_to_expand_the_betslip(self):
        """
        DESCRIPTION: Verify the Build Your Bet (for Coral)/ Bet Builder(for lads) click on Dashboard content area to expand the betslip
        EXPECTED: * Dashboard  content area should be expanded where the selections are added
        """
        pass

    def test_007_tapclick_on_edit_icon_next_to_one_of_player_bet_selections_in_dashboard(self):
        """
        DESCRIPTION: Tap/click on 'Edit' icon next to one of Player Bet selections in dashboard
        EXPECTED: 'Edit selection' section is shown, consisting of:
        EXPECTED: * Edit selection' section title
        EXPECTED: * Done' label
        EXPECTED: * Change player' title and drop-down with previously selected player
        EXPECTED: * Change statistic' title and 2 drop-downs with previously selected statistics
        """
        pass

    def test_008_tapclick_on_change_player_dropdown_and_verify_list_of_player_names(self):
        """
        DESCRIPTION: Tap/click on 'Change player' dropdown and verify list of player names
        EXPECTED: List of players corresponds to name attribute received in players
        """
        pass

    def test_009_click_on_statistic_statistic_value_dropdown_and_verify_statistics_values(self):
        """
        DESCRIPTION: click on 'Statistic, statistic value' dropdown and verify statistics values
        EXPECTED: * List of statistics corresponds to title attribute received in player-statistics
        EXPECTED: * Select any  statistic value from the list
        """
        pass

    def test_010_tapclick_on_done_label(self):
        """
        DESCRIPTION: Tap/click on 'Done' label
        EXPECTED: * 'Edit selection' section is closed
        EXPECTED: * Newly selected values are displayed in dashboard
        EXPECTED: * 'Edit' and 'delete' icons are displayed next to selection
        """
        pass
