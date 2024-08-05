import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.desktop
@pytest.mark.insprint_auto
@pytest.mark.additional_navigation
@vtest
class Test_C66137589_Verify_whether_Profit__Loss_signposting_display_under_settled(BaseBetSlipTest):
    """
    TR_ID: C66137589
    NAME: Verify whether Profit / Loss signposting display under settled
    DESCRIPTION: This test case is to verify Profit /  Loss Signposting display under settled tab
    PRECONDITIONS: User should be have settled bets for sports/races/lottos/pools
    """
    keep_browser_open = True

    def test_000_launch_application(self):
        """
        DESCRIPTION: Launch Application
        EXPECTED: Application shold be launched succesfully
        """
        # covering in below step

    def test_001_log_in_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Log in to the application with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        bet_info = self.place_single_bet_on_cashout_selection()
        self.site.open_my_bets_cashout()
        bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(bet, msg='Bet is not available under Cash Out tab')
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

    def test_002_go_to_mybets_and_navigate_to_settled_tab(self):
        """
        DESCRIPTION: Go to Mybets and navigate to Settled tab
        EXPECTED: User should be able to navigate to settled tab of mybets Note: Sports sub tab will be selected by default under settled
        """
        self.site.open_my_bets_settled_bets()

    def test_003_verify_the__display_of_profit__loss_signposting_under_settled(self):
        """
        DESCRIPTION: Verify the  display of Profit / Loss signposting under settled
        EXPECTED: Should be able  to see Profit / Loss signposting
        """
        self.assertTrue(self.site.bet_history.tab_content.has_profit_or_loss_link(),
                        '"SEE PROFIT/LOSS" link is not displayed under settled tab')

    def test_004_verify_the__display_of_profit__loss_signposting_location_under_settled(self):
        """
        DESCRIPTION: Verify the  display of Profit / Loss signposting Location under settled
        EXPECTED: Profit / Loss signposting should be located below Bet filter under Mybets settled
        EXPECTED: ![](index.php?/attachments/get/d08b8d75-1d48-4e30-8c25-5961570ebb3b)
        """
        bet_filter_position = self.site.bet_history.tab_content.bet_filter.location.get('y')
        profit_or_loss_link_position = self.site.bet_history.tab_content.profit_or_loss_link.location.get('y')
        self.assertLess(bet_filter_position, profit_or_loss_link_position,
                        '"BET FILTER" located below the "SEE PROFIT/LOSS" link')

    def test_005_repeat_the_step_3_to_step_5_and_verify_for_races_lottospools(self):
        """
        DESCRIPTION: Repeat the step 3 to step 5 and verify for races/ lottos/pools
        EXPECTED: Result should be same as above
        EXPECTED: ![](index.php?/attachments/get/8e65ac94-a1c1-4d66-b3ca-29c786d37e05)
        """
        # pools/lotto/sports are descoped
