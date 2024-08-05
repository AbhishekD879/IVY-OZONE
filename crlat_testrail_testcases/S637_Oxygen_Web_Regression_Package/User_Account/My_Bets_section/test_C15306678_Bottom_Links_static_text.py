import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.bet_history_open_bets
@vtest
class Test_C15306678_Bottom_Links_static_text(Common):
    """
    TR_ID: C15306678
    NAME: Bottom Links & static text
    DESCRIPTION: This TC verifies the static links at the bottom of every tab within my bets: Cash-out(if available), Open Bets, Settled Bets.
    PRECONDITIONS: - 'Bottom Links & static text' block should be turned on in the CMS: System configuration->Structure->CashOut->terms (checkbox)
    PRECONDITIONS: - Bottom Links configurable in the CMS-> Statick blocks.
    PRECONDITIONS: - User should have placed/settled/cashouted bets.
    """
    keep_browser_open = True

    def test_001_log_in_into_the_app_and_open_my_bets_page(self):
        """
        DESCRIPTION: Log in into the app and open 'My Bets' page
        EXPECTED: 'My Bets' page opened successfully.
        """
        pass

    def test_002_open_cash_outif_availableopen_bets_tab_scroll_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Open 'Cash-out'(if available)/Open Bets tab, scroll to the bottom of the page
        EXPECTED: Use can see Bottom Links & static text:
        EXPECTED: - See retail bets on Shop bets tracker
        EXPECTED: - Cash Out Terms & Conditions
        EXPECTED: - Edit my Acca Terms & Conditions
        EXPECTED: - static text 'In Play score information is for guidance only and can be subject to a delay'
        """
        pass

    def test_003_click_on_see_retail_bets_on_shop_bets_tracker_link(self):
        """
        DESCRIPTION: Click on 'See retail bets on Shop bets tracker' link
        EXPECTED: The user navigated to the 'Shop Bets' tab
        """
        pass

    def test_004_press_back_button_and_click_cash_out_terms__conditions_link(self):
        """
        DESCRIPTION: Press 'Back' button and click 'Cash Out Terms & Conditions' link
        EXPECTED: The user navigated to the 'Cash Out Terms & Conditions' page.
        """
        pass

    def test_005_press_back_button_and_click_edit_my_acca_terms__conditions_link(self):
        """
        DESCRIPTION: Press 'Back' button and click 'Edit my Acca Terms & Conditions' link
        EXPECTED: The user navigated to the 'Edit my Acca Terms & Conditions' page.
        """
        pass

    def test_006_repeat_steps_2_6_for_settled_bets_tabs_and_subtabs_lotto_and_pools(self):
        """
        DESCRIPTION: Repeat Steps 2-6 for 'Settled Bets' tabs and subtabs ('Lotto' and 'Pools').
        EXPECTED: Links are displayed same way as on Open Bet tab
        """
        pass

    def test_007_login_into_the_app_new_user_user_with_no_placedsettledcashout_bets_and_open_cash_out_open_bets_settled_bets_tabs(self):
        """
        DESCRIPTION: Login into the app new user (user with NO placed/settled/cashout bets) and open Cash-out, Open Bets, Settled Bets tabs.
        EXPECTED: The user shouldn't be able to see 'Bottom Links & static text'
        """
        pass

    def test_008_turn_off_bottom_links__static_text_in_the_cms(self):
        """
        DESCRIPTION: Turn OFF 'Bottom Links & static text' in the CMS
        EXPECTED: 'Terms' checkbox should be unchecked
        """
        pass

    def test_009_log_in_into_the_app_user_should_have_placedsettledcashouted_bets__and_open_my_bets_page_cash_outif_available_open_bets_settled_bets_tabs(self):
        """
        DESCRIPTION: Log in into the app (user should have placed/settled/cashouted bets ) and open 'My Bets' page Cash-out(if available), Open Bets, Settled Bets tabs.
        EXPECTED: The user shouldn't be able to see 'Bottom Links & static text' on any tabs.
        """
        pass
