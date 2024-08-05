import pytest
import voltron.environments.constants as vec
from random import choice , sample
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.new_lotto
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65950042_Verify_max_payout_message_for_Multiple_lines(BaseBetSlipTest):
    """
    TR_ID: C65950042
    NAME: Verify max payout message for Multiple lines
    DESCRIPTION: This test case is to verify payout message for Multiple lines
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True

    def select_number_and_verify(self, line_number=1):
        line = 'Line '+ str(line_number)
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                            timeout=5)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers Below" pop up is not found')
        lotto_selections = list(choose_lucky_num_dialog.items_as_ordered_dict)
        self.assertTrue(lotto_selections, msg=f'There is no lotto buttons')
        select_numbers = []
        for number, item in sample(list(choose_lucky_num_dialog.items_as_ordered_dict.items()),4):
            item.click()
            select_numbers.append(number)
        choose_lucky_num_dialog.done_button.click()

        line_summary = self.site.lotto.line_summary
        self.assertTrue(line_summary.is_displayed(), msg='line summary page is not displayed')
        selected_number = self.site.lotto.line_summary.line_section.items_as_ordered_dict[line].selected_numbers
        self.assertListEqual(sorted([int(number) for number in select_numbers]), sorted([int(number) for number in selected_number]),
                         msg=f'selected number {sorted(select_numbers)} and added number {selected_number}')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        self.site.login()

    def test_002_navigate_to_lottos_page_and_select_any_lottery_by_choose_numbers_or_any_lucky_dip(self):
        """
        DESCRIPTION: Navigate to Lottos Page and Select any Lottery by choose Numbers or any Lucky Dip
        EXPECTED: Able to navigate to the Lottos page and could able to select Numbers or lucky dip
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state(state_name='lotto')

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to choose numbers and could able to add the line and navigated to Line Summary page
        """
        # Lotto carousel
        lotto_carousel = self.site.lotto.lotto_carousel
        self.assertTrue(lotto_carousel.is_displayed(), msg='Lotto carousel is not displayed')

        self.__class__.balls = self.site.lotto.tab_content.potential_returns.items_as_ordered_dict

        # Numbers button
        self.site.lotto.tab_content.choose_numbers.click()

        self.select_number_and_verify(line_number=1)

    def test_004_verify_the_line_summary_page(self):
        """
        DESCRIPTION: Verify the Line Summary Page
        EXPECTED: Able to see the Below Info-
        """
        # This step is covered in step 003

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: Added lines with chossen numbers
        """
        # verified this step in step 003

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: Avaliable Draws Information
        """
        draw_info =  self.site.lotto.line_summary.choose_your_draws_section
        self.assertTrue(draw_info.is_displayed(), msg='Draws information is displayed')

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: How Many weeks INformation
        """
        weeks_info =  self.site.lotto.line_summary.how_many_weeks_section
        self.assertTrue(weeks_info.is_displayed(), msg='Weeks information is displayed')

    def test_008_verify_creating_a_new_line(self):
        """
        DESCRIPTION: Verify Creating a New Line
        EXPECTED: user can able to Create a new line and can see the multiple lines are added succesfully in line summary page
        """
        self.site.lotto.line_summary.line_section.create_a_new_line.click()
        self.select_number_and_verify(line_number=2)

    def test_009_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        draw = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        choice_day = choice(list(draw))
        choose_draw = choice(draw[choice_day].items)
        choose_draw.click()
        self.site.lotto.line_summary.add_to_betslip.click()
        bets = self.site.lotto_betslip.betslip_sections_list
        self.assertTrue(bets, msg='Bet-slip is not displayed ')

    def test_010_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        selection_1 = self.site.lotto_betslip.betslip_sections_list.items[0]
        selection_1.show_hide_multiples.click()
        selection = selection_1.items_as_ordered_dict.get('Single')
        selection.amount_form.input.click()
        selection.amount_form.input.value = self.bet_amount
        expected_est_return =float((self.bet_amount*self.balls[1]+self.bet_amount)*4)
        actual_est_return = float(self.site.lotto_betslip.betslip_sections_list.items[0].est_returns_value)
        self.assertEquals(round(expected_est_return,2), round(actual_est_return,2),
                          msg=f'actual est_return {round(actual_est_return,2)} and expected est_return {round(expected_est_return,2)} is not equal' )

        # Potential return for Double
        selection = self.site.lotto_betslip.betslip_sections_list.items[0].items_as_ordered_dict.get('Double')
        selection.amount_form.input.click()
        selection.amount_form.input.value = self.bet_amount
        wait_for_haul(2)
        expected_est_return =float(actual_est_return+(self.bet_amount*self.balls[2]+self.bet_amount)*6)
        actual_est_return = float(self.site.lotto_betslip.betslip_sections_list.items[0].est_returns_value)
        self.assertEquals(round(expected_est_return, 2), round(actual_est_return, 2),
                          msg=f'actual est_return {round(actual_est_return, 2)} and expected est_return {round(expected_est_return, 2)} is not equal')

        # Potential return for Treble
        selection = self.site.lotto_betslip.betslip_sections_list.items[0].items_as_ordered_dict.get('Treble')
        selection.amount_form.input.click()
        selection.amount_form.input.value = self.bet_amount
        wait_for_haul(2)
        expected_est_return = float(actual_est_return+(self.bet_amount*self.balls[3]+self.bet_amount)*4)
        actual_est_return = float(self.site.lotto_betslip.betslip_sections_list.items[0].est_returns_value)
        self.assertEquals(round(expected_est_return, 2), round(actual_est_return, 2),
                          msg=f'actual est_return {round(actual_est_return, 2)} and expected est_return {round(expected_est_return, 2)} is not equal')
    def test_011_verify_payout_at_estreturns_when_payout_is_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout is exceeds max payout
        EXPECTED: user can see the Payout limit exceeded message
        """
        self.site.lotto_betslip.betslip_sections_list.items[0].amount_form.input.click()
        self.site.lotto_betslip.betslip_sections_list.items[0].amount_form.input.value = 1000
        pay_out_info = self.site.lotto_betslip.max_payout_info
        self.assertTrue(pay_out_info, msg=f'max pay out exceeded messages is not displayed {pay_out_info}')