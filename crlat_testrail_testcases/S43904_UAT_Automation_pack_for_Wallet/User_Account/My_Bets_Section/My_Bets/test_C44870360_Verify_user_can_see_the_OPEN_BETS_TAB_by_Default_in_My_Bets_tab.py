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
class Test_C44870360_Verify_user_can_see_the_OPEN_BETS_TAB_by_Default_in_My_Bets_tab(Common):
    """
    TR_ID: C44870360
    NAME: "Verify  user can see the OPEN BETS TAB by Default in My Bets tab
    DESCRIPTION: "Verify  user can see the OPEN BETS TAB by Default in My Bets tab
    PRECONDITIONS: Used should be logged in
    PRECONDITIONS: User must have some single, double, each way and accumulator bets placed.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        pass

    def test_002_click_on_my_betsorclick_on_my_bets_icon_on_footer_menuorclick_on_my_bets_in_bet_slip_for_desktoporclick_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Click on My Bets
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets icon on Footer Menu.
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets in Bet Slip (for Desktop)
        DESCRIPTION: or
        DESCRIPTION: Click Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: My Bets page should open.
        """
        pass

    def test_003__verify__user_can_see_the_open_bets_tab_by_default_verify_open_bets_page_shows_all_placed_open_betsnote_user_see_settled_bets_tab_by_default_when_navigated_from_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: -Verify  user can see the OPEN BETS TAB by Default
        DESCRIPTION: -Verify 'Open bets' page shows all placed open bets
        DESCRIPTION: Note: User see Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: - OPEN BETS is selected by default.
        EXPECTED: - User should be able to to all Open Bets (Bets which are not settled or cashed out)
        EXPECTED: Note: User see Settled bets tab by default when navigated from Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        """
        pass

    def test_004__verify_see_retail_bets_on_the_shop_bet_tracker_navigates_to_shop_bets_verify_cash_out_terms__conditions_verify_edit_my_acca_terms__conditionsby_scrolling_down_your_bets_and_see_if_links_are_navigating_to_relevant_pages(self):
        """
        DESCRIPTION: -Verify See Retail bets on the Shop bet tracker navigates to shop bets
        DESCRIPTION: -Verify Cash Out Terms & Conditions
        DESCRIPTION: -Verify Edit My Acca Terms & Conditions
        DESCRIPTION: by scrolling down your bets and see if links are navigating to relevant pages.
        EXPECTED: - User should be able to see
        EXPECTED: See Retail Bets on Shop Bet Tracker > navigated to shop bets
        EXPECTED: Cash Out Terms & Conditions
        EXPECTED: Edit My Acca Terms & Conditions
        """
        pass

    def test_005__verify_header_it_should_display_bet_type_for_each_bet_single__double__acca_etc_(self):
        """
        DESCRIPTION: -Verify Header it should display bet type for each bet (Single / Double / ACCA etc )
        EXPECTED: -User should be able to see all these headers for bets, such as SINGLE, SINGLE (EACH WAY), DOUBLE, TREBLE, ACCA(no. of selections) etc
        """
        pass

    def test_006__verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: -Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: - Customer should see all these three tabs
        EXPECTED: Sports   Lotto  Pools
        """
        pass

    def test_007_verify_my_bets_tabcash_out_if_configured_in_cmsopen_betssettled_betsshop_bets(self):
        """
        DESCRIPTION: Verify My Bets tab
        DESCRIPTION: Cash Out (if configured in CMS)
        DESCRIPTION: Open Bets
        DESCRIPTION: Settled Bets
        DESCRIPTION: Shop bets
        EXPECTED: User is able to see these tabs
        EXPECTED: Cash Out    Open Bets     Settled Bets   Shop bets
        """
        pass

    def test_008__verify_bets_shown_in_open_betscash_out_tab_should_have_this_informationstakepotential_returnsestimate_returns(self):
        """
        DESCRIPTION: -Verify bets shown in Open Bets/Cash Out Tab should have this information
        DESCRIPTION: Stake
        DESCRIPTION: Potential Returns/Estimate Returns.
        EXPECTED: Customer should be able to see Stake and Potential Returns for all bets placed.
        """
        pass
