import time
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.new_lotto
@pytest.mark.other
@vtest
class Test_C65950033_Verify_the_max_payout_information_area_to_be_displayed_above_the_Total_Stake_and_Returns_area_near_placebet_button(Common):
    """
    TR_ID: C65950033
    NAME: Verify the max payout information area to be displayed above the Total Stake and Returns area near placebet button
    DESCRIPTION: This test case is to verify max payout information area to be displayed above the Total Stake and Returns area near placebet button
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True
    stake = 0.10
    selected_numbers =[]

    def expected_est_returns(self, expected_bet_type=''):
        if expected_bet_type == 'Main':
            expected_est_return_value = round((self.stake * 1) + (self.main_winning_amount * self.stake), 2)
        elif expected_bet_type == 'Single':
            expected_est_return_value = round(((self.stake * 1) + (self.single_ball_winning_amount * self.stake)) * 4 ,2)
        else:
            expected_est_return_value = round(((self.stake * 1) + (self.double_ball_winning_amount * self.stake)) * 6 ,2)

        return expected_est_return_value

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Verifying LOTTO is enabled or not
        """
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled') == True:
                raise CmsClientException(f'LOTTO Page is not configured')
        get_lotto = self.cms_config.get_lotto_main_page_configuration()
        lotteries = get_lotto['lottoConfig']
        for lotto in lotteries:
            lotto_name = lotto['label']
            if lotto_name == "49's Lottery":
                self.__class__.max_payout = lotto['maxPayOut']

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
        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        potential_returns = self.site.lotto.tab_content.potential_returns.items_as_ordered_dict
        self.__class__.main_winning_amount = potential_returns.get(4)
        self.__class__.single_ball_winning_amount = potential_returns.get(1)
        self.__class__.double_ball_winning_amount = potential_returns.get(2)

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to choose numbers and could able to add the line and navigated to Line Summary page
        """
        # selecting LUCKY 4
        lucky_buttons = list(self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict.values())
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons[1].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                            timeout=5)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers Below" pop up is not found')
        lotto_selections = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(lotto_selections, msg=f'There is no lotto buttons')
        available_selections = len(lotto_selections)
        self._logger.debug('Number of available selections is: %s' % available_selections)
        for item_name, item in lotto_selections.items():
            if item.is_selected():
                self.selected_numbers.append(item_name)
        choose_lucky_num_dialog.done_button.click()
        choose_lucky_num_dialog.wait_dialog_closed()
        lines = self.site.lotto.line_summary.line_section.items_as_ordered_dict
        line = lines.get('Line 1')
        selected_numbers_ui = line.selected_numbers
        self.assertListEqual(self.selected_numbers, selected_numbers_ui,
                             msg=f'Actual numbers from FE : {selected_numbers_ui} is not same expected numbers:{self.selected_numbers}')

    def test_004_verify_the_line_summary_page(self):
        """
        DESCRIPTION: Verify the Line Summary Page
        EXPECTED: Able to see the Below Info-
        """
        url = self.device.get_current_url()
        self.assertIn('linesummary',url,msg=f'linesummary page is not open')

    def test_005_(self):
        """
        DESCRIPTION:
        EXPECTED: Added lines with chossen numbers
        """
        # Covered in above step

    def test_006_(self):
        """
        DESCRIPTION:
        EXPECTED: Avaliable Draws Information
        """
        draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        self.assertIsNotNone(draws, msg="Draws are not present below choose your draws section")
        first_day_name, first_item = next(
            ((first_day_name, first_item) for first_day_name, first_item in draws.items()), None)
        time_draws = first_item.items_as_ordered_dict
        self.assertIsNotNone(time_draws, msg="Time draws are not available")
        first_time_draw_name, first_time_item = next(
            ((first_time_draw_name, first_item) for first_time_draw_name, first_item in time_draws.items()), None)
        first_time_item.click()
        self.site.lotto.line_summary.add_to_betslip.click()
        # Time and date splitting based for bet slip
        time_from_st1 = first_time_draw_name.split()[-1]
        self.__class__.expected_time = ' '.join(first_time_draw_name.split()[:-1])
        self.__class__.expected_day = first_day_name[:-1] + ')'+' ' + '-'+' '+time_from_st1

    def test_007_(self):
        """
        DESCRIPTION:
        EXPECTED: How Many weeks Information
        """
        # covered in above step

    def test_008_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_enabled(),msg="Add to Betslip button not enabled")
        self.site.lotto.line_summary.add_to_betslip.click()

    def test_009_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        lottery_name = "49's 6 Ball" if self.brand == "ladbrokes" else "49's 6 Ball Draw"
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        lotto_bestslip_name = self.site.lotto_betslip
        self.__class__.lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(f"{lottery_name}-{self.expected_time.title()}-{self.expected_day}-{' '.join(self.selected_numbers)}")
        self.lotto_bet.amount_form.input.click()
        self.lotto_bet.amount_form.input.value = self.stake
        bet_slip_line_numbers = self.lotto_bet.betslip_selected_numbers
        self.assertListEqual(bet_slip_line_numbers,self.selected_numbers,
                             msg=f'Actual numbers from FE : {bet_slip_line_numbers} is not same expected numbers:{self.selected_numbers}')
        betslip_day = self.lotto_bet.draw_date.replace(', ', '')
        self.assertEqual(betslip_day, self.expected_day,
                         msg= f'Actual Day from Betslip: {betslip_day} is not equal to expected day from Line summary:{self.expected_day}')
        betslip_time = self.lotto_bet.draw_heading
        self.assertEqual(betslip_time, self.expected_time.title(),
                         msg=f'Actual time from Betslip: {betslip_time} is not equal to expected time from Line summary:{self.expected_time.title()}')
        actual_total_stake = round(float(self.lotto_bet.est_returns_value.replace(',','')), 2)
        expected_total_stake = self.expected_est_returns(expected_bet_type='Main')
        self.assertEqual(actual_total_stake,expected_total_stake,
                         msg=f'Actual total stake from FE:{actual_total_stake} is not same as expected total stake calculations:{expected_total_stake}')
        # Single bet verification
        self.lotto_bet.show_hide_multiples.click()
        single_selection = self.lotto_bet.items_as_ordered_dict.get('Single')
        single_selection.amount_form.input.click()
        single_selection.amount_form.input.value = self.stake
        actual_single_bet_est_return_value = round(float(single_selection.est_returns.replace(',','')), 2)
        expected_single_bet_est_return_value = self.expected_est_returns(expected_bet_type='Single')
        self.assertEqual(actual_single_bet_est_return_value, expected_single_bet_est_return_value,
                         msg=f'Actual total stake from FE:{actual_single_bet_est_return_value} is not same as expected total stake calculations:{expected_single_bet_est_return_value}')
        # Double bet verification
        double_selection = self.lotto_bet.items_as_ordered_dict.get('Double')
        double_selection.amount_form.input.click()
        double_selection.amount_form.input.value = self.stake
        actual_double_bet_est_return_value = round(float(double_selection.est_returns.replace(',','')), 2)
        expected_double_bet_est_return_value = self.expected_est_returns(expected_bet_type='Double')
        self.assertEqual(actual_double_bet_est_return_value, expected_double_bet_est_return_value,
                         msg=f'Actual total stake from FE:{actual_double_bet_est_return_value} is not same as expected total stake calculations:{expected_double_bet_est_return_value}')

    def test_010_verify_payout_at_estreturns_when_payout_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout exceeds max payout
        EXPECTED: user could see the Payout limit exceeded message
        """
        self.lotto_bet.amount_form.input.click()
        stakes = [1]
        for stake in stakes:
            # verifying Potential returns and max payout limit verifications
            est_return_value = round((stake * 1) + (self.main_winning_amount * stake), 2)
            if est_return_value > self.max_payout:
                self.site.lotto_betslip.max_payout_link.scroll_to_we()
                time.sleep(2)
                self.assertTrue(self.site.lotto_betslip.has_max_payout_info(),
                                msg="Max Payout limit message  is not display")
            else:
                self.assertFalse(self.site.lotto_betslip.has_max_payout_info(),
                                 msg="Max Payout limit message  is not display")
                self.lotto_bet.amount_form.input.click()
                self.lotto_bet.amount_form.input.value = stake + 10
                stakes.append(float(self.lotto_bet.amount_form.input.value))

    def test_011_verify_the_max_payout_information_area_to_be_displayed_above_the_total_stake_and_returns_area_near_placebet_button(self):
        """
        DESCRIPTION: Verify the max payout information area to be displayed above the Total Stake and Returns area near placebet button
        EXPECTED: Message is displaying above the Total Stake and Returns area near placebet button
        """
        # Can't Automate the positions/places in Lotto Betslip
