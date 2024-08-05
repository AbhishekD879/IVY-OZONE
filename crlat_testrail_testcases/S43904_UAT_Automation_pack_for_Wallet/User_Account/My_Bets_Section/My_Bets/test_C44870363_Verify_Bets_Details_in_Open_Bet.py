import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870363_Verify_Bets_Details_in_Open_Bet(Common):
    """
    TR_ID: C44870363
    NAME: Verify Bets Details in Open Bet.
    DESCRIPTION: This TC verifies bet details in Open Bet tab.
    DESCRIPTION: Verify user can see the OPEN BETS TAB by Default in My Bets tab
    PRECONDITIONS: User should be logged in.
    PRECONDITIONS: Uses must have placed bets (single, double, each way and accumulator)
    """
    keep_browser_open = True

    def test_001_load_application__log_in(self):
        """
        DESCRIPTION: Load Application & Log in
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        pass

    def test_002_click_on_my_betsorclick_on_cashout_icon_on_footer_menuorclick_on_my_bets_in_bet_slip_for_desktoporclick_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Click on My Bets
        DESCRIPTION: or
        DESCRIPTION: Click on Cashout icon on Footer Menu.
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets in Bet Slip (for Desktop)
        DESCRIPTION: or
        DESCRIPTION: Click Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: My Bets page should open.
        """
        pass

    def test_003__verify_user_can_see_the_open_bets_tab_by_default_verify_open_bets_page_shows_all_placed_open_betsnote_user_see_cashout__tab_by_default_when_navigated_from_cashout_via_footer_menu_on_mobile_user_sees_settled_bets_tab_by_default_when_navigated_from_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: -Verify user can see the OPEN BETS TAB by Default
        DESCRIPTION: -Verify 'Open bets' page shows all placed open bets
        DESCRIPTION: Note: User see Cashout  tab by default when navigated from Cashout via Footer menu on Mobile &
        DESCRIPTION: User sees Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: OPEN BETS is selected by default.
        EXPECTED: User should be able to to all Open Bets (Bets which are not settled or cashed out)
        """
        pass

    def test_004_verify_open_bet_pending_bet_detailsverify_below_details_of_the_bet__date_and_time_of_the_event__selection_name__event_name__market_name__stake_and_estimated_returns__silks_for_horse_racing__signposting_if_available(self):
        """
        DESCRIPTION: Verify open bet pending bet details
        DESCRIPTION: Verify below details of the bet
        DESCRIPTION: - date and time of the event.
        DESCRIPTION: - Selection name
        DESCRIPTION: - Event name
        DESCRIPTION: - Market name
        DESCRIPTION: - Stake and Estimated returns
        DESCRIPTION: - Silks for horse racing
        DESCRIPTION: - Signposting if available
        EXPECTED: User is able to see these details
        EXPECTED: - date and time of the event
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Market Name
        EXPECTED: - Stake and Estimated returns
        EXPECTED: - Silks for horse racing
        EXPECTED: - Signposting if available
        """
        pass

    def test_005_verify_header_it_should_display_bet_type_for_each_bet_single__double__acca_etc_(self):
        """
        DESCRIPTION: Verify Header it should display bet type for each bet (Single / Double / ACCA etc )
        EXPECTED: -User should be able to see all these headers for bets, such as SINGLE, SINGLE (EACH WAY), DOUBLE, TREBLE, ACCA(no. of selections) etc
        """
        pass

    def test_006_verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: Customer should see all these three tabs Sports Lotto Pools
        """
        pass

    def test_007_verify_settled_bets_are_moved_to_settled_tab(self):
        """
        DESCRIPTION: Verify Settled Bets are moved to Settled Tab
        EXPECTED: User is able to see bets in Settled Tab once bet is settled or Cashed out.
        """
        pass

    def test_008_verify_bets_shown_in_open_betscash_out_tab_should_have_this_informationstakepotential_returnsestimate_returns(self):
        """
        DESCRIPTION: Verify bets shown in Open Bets/Cash Out Tab should have this information
        DESCRIPTION: Stake
        DESCRIPTION: Potential Returns/Estimate Returns.
        EXPECTED: Customer should be able to see Stake and Potential Returns for all bets placed.
        """
        pass
