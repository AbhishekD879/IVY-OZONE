import pytest
import tests
import random
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


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
class Test_C65950032_Verify_link_at_maxpayout_message(BaseBetSlipTest):
    """
    TR_ID: C65950032
    NAME: Verify link at maxpayout message
    DESCRIPTION: This test case is to verify link at maxpayout message
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True
    line_name = 'Line 1'
    bet_amount = 0.10 if tests.settings.backend_env == 'prod' else 1
    selected_numbers = []
    is_first_time_draws_selection = True


    def select_random_draws(self, draw_dict):
        if not draw_dict:
            raise SiteServeException('Draw buttons are not available')
        if self.is_first_time_draws_selection:
            self.__class__.draw_dict_list = list(draw_dict)
            self.is_first_time_draws_selection = False
        date_name = random.sample(self.draw_dict_list, 1)[0]
        self.__class__.draw_dict_list.remove(date_name)
        time_draw = draw_dict[date_name].items_as_ordered_dict
        time_draw_name = random.sample(list(time_draw), 1)[0]
        words = (time_draw_name.split())[:-1]
        draw_name = ' '.join(word.capitalize() for word in words)
        expected_day_and_time = f'{date_name} - {time_draw_name.split()[-1]}'
        time_draw[time_draw_name].click()
        return draw_name, expected_day_and_time

    def verify_betslip(self, draw_name, expected_day_and_time, bet_amount, verify_details=True):
        lottery_name = "49's 6 Ball Draw" if self.brand == "bma" else "49's 6 Ball"
        # Common verification logic for both draws
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        numbers = ' '.join(item for item in self.selected_numbers)
        lotto_bestslip_name = self.site.lotto_betslip
        cleaned_day_and_time = expected_day_and_time.replace("('", "").replace("')", "")
        bet_identifier = f"{lottery_name}-{draw_name}-{cleaned_day_and_time}-{numbers}"
        lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(bet_identifier)
        lotto_bet.amount_form.input.click()
        lotto_bet.amount_form.input.value = bet_amount
        if verify_details:
            bet_slip_line_numbers = lotto_bet.betslip_selected_numbers
            self.assertListEqual(bet_slip_line_numbers, self.selected_numbers,
                                 msg=f'Actual numbers from FE: {bet_slip_line_numbers} is not the same as expected numbers: {self.selected_numbers}')
            betslip_draw_date = lotto_bet.draw_date
            self.assertEqual(betslip_draw_date, expected_day_and_time,
                             msg=f'Actual Day from Betslip: {betslip_draw_date} is not equal to expected day from Line summary: {expected_day_and_time}')
            betslip_time = lotto_bet.draw_heading
            self.assertEqual(betslip_time, draw_name,
                             msg=f'Actual time from Betslip: {betslip_time} is not equal to expected time from Line summary: {draw_name}')

            actual_est_return_value = "{:.2f}".format(float(lotto_bet.est_returns_value.replace(',', '')))
            # calculating estimations returns according to added selections
            expected_est_return_value = "{:.2f}".format(
                (self.bet_amount * 1) + (self.main_winning_amount * self.bet_amount))
            self.assertEqual(actual_est_return_value, expected_est_return_value)
            pay_out_info = self.site.lotto_betslip.max_payout_info
            self.assertFalse(pay_out_info, msg=f'max pay out exceeded messages is not displayed {pay_out_info}')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled') == True:
                raise CmsClientException('"LOTTO" Page is not configured')

        get_lotto = self.cms_config.get_lotto_main_page_configuration()
        lotteries = get_lotto['lottoConfig']
        for lotto in lotteries:
            lotto_name = lotto['label']
            if lotto_name == "49's Lottery":
                self.__class__.max_payout = lotto['maxPayOut']

        self.site.login(username=tests.settings.betplacement_user)

    def test_002_navigate_to_lottos_page_and_select_any_lottery_by_choose_numbers_or_any_lucky_dip(self):
        """
        DESCRIPTION: Navigate to Lottos Page and Select any Lottery by choose Numbers or any Lucky Dip
        EXPECTED: Able to navigate to the Lottos page and could able to select Numbers or lucky dip
        """
        # navigating to lotto page
        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        potential_returns = self.site.lotto.tab_content.potential_returns.items_as_ordered_dict
        self.__class__.main_winning_amount = potential_returns.get(3)
        self.__class__.single_ball_winning_amount = potential_returns.get(1)
        self.__class__.double_ball_winning_amount = potential_returns.get(2)

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to choose numbers and could able to add the line and navigated to Line Summary page
        """
        lucky_buttons = list(self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict.values())
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons[0].click()
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
        actual_selected_numbers = self.site.lotto.line_summary.line_section.items_as_ordered_dict
        line = actual_selected_numbers.get('Line 1')
        selected_numbers_ui = line.selected_numbers
        self.assertListEqual(self.selected_numbers, selected_numbers_ui,
                             msg=f'Actual numbers from FE : {selected_numbers_ui} is not same expected numbers:{self.selected_numbers}')

    def test_004_verify_the_line_summary_page(self):
        """
        DESCRIPTION: Verify the Line Summary Page
        EXPECTED: Able to see the Below Info-
        """
        url = self.device.get_current_url()
        self.assertIn('linesummary', url, msg=f'linesummary page is not open')
        choose_your_draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        length_choose_your_draws = len(choose_your_draws)
        if length_choose_your_draws > 0:
            # Selecting random draws for the first and second time
            self.__class__.first_draw_name, self.__class__.first_expected_day_and_time = self.select_random_draws(
                choose_your_draws)
            self.__class__.second_draw_name, self.__class__.second_expected_day_and_time = self.select_random_draws(
                choose_your_draws)

        # verifying week buttons are available under "How Many Weeks"
        number_of_week_selection = '1'
        def weeks_dict():
            weeks_ordered_dict = self.site.lotto.line_summary.how_many_weeks_section.week_selections_items
            if number_of_week_selection in weeks_ordered_dict:
                return weeks_ordered_dict

        weeks = wait_for_result(
            lambda: weeks_dict(),
            timeout=10,
            expected_result=True,
            name=f'Section "{number_of_week_selection}" is in weeks list',
            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, IndexError, VoltronException)
        )
        if len(weeks) > 0:
            weeks[number_of_week_selection].click()
        else:
            raise SiteServeException(f'week buttons are not available under "How Many Weeks"')

    def test_005_Added_lines_with_chossen_numbers(self):
        """
        DESCRIPTION: 
        EXPECTED: Added lines with chossen numbers
        """
        #covered above

    def test_006_Avaliable_Draws_Information(self):
        """
        DESCRIPTION: 
        EXPECTED: Avaliable Draws Information
        """
        #covered above

    def test_007_How_Many_weeks_INformation(self):
        """
        DESCRIPTION: 
        EXPECTED: How Many weeks INformation
        """
        #covered above

    def test_008_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg='add To Betslip is not visible in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()
        lotto_betslip_name = self.site.lotto_betslip
        bets = lotto_betslip_name.betslip_sections_list.items_as_ordered_dict
        self.assertTrue(bets, msg='Bet-slip is not displayed ')

    def test_009_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        self.verify_betslip(self.first_draw_name, self.first_expected_day_and_time,self.bet_amount,  verify_details=True)
        self.verify_betslip(self.second_draw_name, self.second_expected_day_and_time,self.bet_amount,  verify_details=True)

    def test_010_verify_payout_at_estreturns_when_payout_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout exceeds max payout
        EXPECTED: user could see the Payout limit exceeded message
        """
        self.verify_betslip(self.first_draw_name, self.first_expected_day_and_time, self.max_payout+1, verify_details=False)
        pay_out_info_msg = self.site.lotto_betslip.has_max_payout_info
        self.assertTrue(pay_out_info_msg, msg=f'payout msg is not displayed')
    def test_011_click_on_the_hyper_link_in_the__maxpayout_message(self):
        """
        DESCRIPTION: Click on the hyper link in the  maxpayout message
        EXPECTED: user should able to navigate to the Maximum Payouts Information page
        """
        self.site.lotto_betslip.max_payout_link.click()
        if self.brand == 'bma':
            expected_max_payout_url = 'https://help.coral.co.uk/en/sports-help/sports-queries/maximum-payouts'
        else:
            expected_max_payout_url = 'https://help.ladbrokes.com/en/sports-help/sports-queries/maximum-payouts'
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, expected_max_payout_url, msg=f'urls dont match expected "{expected_max_payout_url}" and actual "{current_url}"')


