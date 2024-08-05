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
class Test_C64569680_Verify_customer_clicks_done_after_editing_a_selection_GA_tagged(Common):
    """
    TR_ID: C64569680
    NAME: Verify customer clicks done after editing a selection GA tagged
    DESCRIPTION: This test case verifies clicking on done,edit after editing the selection in Quickbet is Ga tracked
    PRECONDITIONS: 1:Banach events should be available with all or ANY of the above Market
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

    def test_008_validate_editing_the_selection_from_bybbb_quick_bet_is_ga_tracked(self):
        """
        DESCRIPTION: validate Editing the selection from BYB/BB quick bet is Ga tracked
        EXPECTED: * Click on Editing the selection for the player is Ga tracked
        EXPECTED: ![](index.php?/attachments/get/30243ac5-9086-4562-85ba-e6fcc5b9c8f6)
        """
        pass

    def test_009_validate_when_customer_click_on_done_after_editing_the_selection_in_bybbb_quick_bet_is_ga_tagged(self):
        """
        DESCRIPTION: Validate when customer click on Done after editing the selection in BYB/BB quick bet is GA tagged
        EXPECTED: * Click on Done after editing the selection should be GA tagged in Quick bet BYB/BB
        EXPECTED: ![](index.php?/attachments/get/e7449552-98f8-4b25-9361-618db672efc4)
        """
        pass
