import time
import pytest
from tests.base_test import vtest
import random
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.new_lotto
@vtest
class Test_C65950043_Verify_max_payout_message_for_Bonus_ball(BaseCashOutTest):
    """
    TR_ID: C65950043
    NAME: Verify max payout message for Bonus ball
    DESCRIPTION: This test case is to verify max payout message for Bonus ball
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True
    stake = 0.1

    def generate_random_numbers(self):
        """
        DESCRIPTION :Generate 5 unique random numbers between 1 and 49
        """
        # Generate 5 unique random numbers between 1 and 49
        random_numbers = random.sample(range(1, 50), 5)
        return random_numbers

    def test_000_preconditions(self):
        """
        DESCRIPTION : verifying lotto page is disable or not in cms
        DESCRIPTION : getting "use bonus ball" odds from "site server" call
        """
        lottery_name = "49's 7 Ball Draw" if self.brand == "bma" else "49's 7 ball"
        lotto_filter = self.ss_query_builder.add_filter(simple_filter(LEVELS.LOTTERY, ATTRIBUTES.HAS_OPEN_DRAW))
        lotto_resp = self.ss_req.ss_lottery_to_draw(query_builder=lotto_filter)
        lottery_resp = next(i.get('lottery') for i in lotto_resp if lottery_name == i.get('lottery').get('name'))
        lottery_prices_lists = [prices_res for prices_res in lottery_resp.get('children') if prices_res.get('lotteryPrice')]
        # getting "use bonus ball" odds from "site server" call
        for lottery_prices_list in lottery_prices_lists:
            if lottery_prices_list['lotteryPrice']['numberCorrect'] == '1' and lottery_prices_list['lotteryPrice']['numberPicks'] == '1':
                self.__class__.bonus_single_ball = float(lottery_prices_list['lotteryPrice']['priceNum'])
            if lottery_prices_list['lotteryPrice']['numberCorrect'] == '2' and lottery_prices_list['lotteryPrice']['numberPicks'] == '2':
                self.__class__.bonus_double_ball = float(lottery_prices_list['lotteryPrice']['priceNum'])
            if lottery_prices_list['lotteryPrice']['numberCorrect'] == '5' and lottery_prices_list['lotteryPrice']['numberPicks'] == '5':
                self.__class__.main_winning_amount = float(lottery_prices_list['lotteryPrice']['priceNum'])
        # verifying lotto page is disable or not in cms
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled') == True:
                raise CmsClientException(f'"LOTTO" Page is not configured')
        # getting max payout limit from cms
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
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        self.site.login()

    def test_002_navigate_to_lottos_page_and_select_any_lottery_by_choose_numbers_or_any_lucky_dip(self):
        """
        DESCRIPTION: Navigate to Lottos Page and Select any Lottery by choose Numbers or any Lucky Dip
        EXPECTED: Able to navigate to the Lottos page and could able to select Numbers or lucky dip
        """
        # navigating to lotto page
        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        # clicking on choose numbers button
        self.assertTrue(self.site.lotto.tab_content.choose_numbers.is_displayed(),
                        msg=f'choose numbers button is not present in lotto page')
        self.site.lotto.tab_content.choose_numbers.click()

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to choose numbers and could be able to add the line and navigated to Line Summary page
        """
        # verifying whether select number dialogue popup is visible or not in lotto page
        dialog_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=5)
        self.assertIsNotNone(dialog_popup, msg=f'Dialogue popup is not opened')
        #  generating random numbers to select numbers in select numbers dialogue page
        self.__class__.lotto_numbers = self.generate_random_numbers()
        # getting ui numbers from select numbers dialogue page
        ui_lotto_numbers = dialog_popup.number_selectors_ordered_dict
        # selecting random five numbers in select number dialogue page
        for lotto_number in self.lotto_numbers:
            ui_lotto_numbers.get(str(lotto_number)).click()
            wait_for_haul(2)
        # checking whether add line button is visible or not in select numbers dialogue page
        self.assertTrue(dialog_popup.done_button.is_displayed(),
                        msg=f'add line button is not visible in select numbers dialogue')
        dialog_popup.done_button.click()
        # checking whether user is able to navigate "line summary" page
        current_url = self.device.get_current_url()
        self.assertIn("linesummary", current_url, msg=f'Not able to navigate to line summary page')

    def test_004_verify_the_line_summary_page(self):
        """
        DESCRIPTION: Verify the Line Summary Page
        EXPECTED: Able to see the Below Information
        EXPECTED: Added lines with chosen numbers
        EXPECTED: Available Draws Information
        EXPECTED: How Many weeks Information
        """
        # verifying "selection numbers" which user added from "choose number selection" dialogue popup page
        self.__class__.expected_selection_numbers = self.lotto_numbers
        actual_selected_numbers = list(map(int, self.site.lotto.line_summary.line_section.items_as_ordered_dict.get(
            'Line 1').selected_numbers))
        self.__class__.expected_select_numbers = sorted(self.expected_selection_numbers)
        self.__class__.numbers = ' '.join(str(item) for item in self.expected_select_numbers)
        self.assertListEqual(actual_selected_numbers, self.expected_select_numbers,
                             msg=f'Actual numbers from FE : {actual_selected_numbers} is not same expected numbers:{sorted(self.expected_selection_numbers)}')
        # verifying lucky buttons are available under "Choose Your Draws"
        choose_your_draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        length_cyd = len(choose_your_draws)
        if length_cyd > 0:
            first_day_name, first_item = next(((first_day_name, first_item) for first_day_name, first_item in choose_your_draws.items()), None)
            time_draws = first_item.items_as_ordered_dict
            first_time_draw_name, first_time_item = next(
                ((first_time_draw_name, first_item) for first_time_draw_name, first_item in time_draws.items()), None)
            words = (first_time_draw_name.split())[:-1]
            self.__class__.draw_name = ' '.join(word.capitalize() for word in words)
            self.__class__.expected_day_and_time = f'{first_day_name} - {first_time_draw_name.split()[-1]}'
            first_time_item.click()
        else:
            raise SiteServeException(f'lucky buttons are not available under "choose your draws"')
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

    def test_005_verify_adding_bonus_ball(self):
        """
        DESCRIPTION: Verify adding Bonus ball
        EXPECTED: user can be able to add the bonus ball
        """
        # verifying "Use Bonus Ball" is visible to user or not and able to Select or not.
        expected_use_bonus_line = "Use Bonus Ball"
        line_data = self.site.lotto.line_summary.line_section.items_as_ordered_dict
        actual_use_bonus_line = line_data.get('Line 1').bonus_ball_name
        self.assertEqual(expected_use_bonus_line.upper(), actual_use_bonus_line.upper(),
                         msg=f'{expected_use_bonus_line.upper()} is not same as {actual_use_bonus_line.upper()}')
        # verifying user is able to select "User Bonus Ball"
        line_data.get('Line 1').bonus_ball_check_box.click()
        self.assertTrue(line_data.get('Line 1').bonus_ball_check_box.is_enabled(),
                         msg=f'User is not able to click on "User Bonus Ball" check box')

    def test_006_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg=f'add To Betslip is not visible in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()

    def test_007_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        lottery_name = "49's 7 Ball Draw" if self.brand == "bma" else "49's 7 Ball"
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        lotto_bestslip_name = self.site.lotto_betslip
        self.__class__.lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(f"{lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{self.numbers}")
        # getting line numbers from betslip
        numbers = self.lotto_bet.betslip_selected_numbers
        bet_slip_line_numbers = [int(i) for i in numbers]
        self.assertListEqual(bet_slip_line_numbers, sorted(self.expected_selection_numbers),
                             msg=f'Actual numbers from FE : {bet_slip_line_numbers} is not same expected numbers:{self.expected_selection_numbers}')
        betslip_day_and_time = self.lotto_bet.draw_date.replace(', ', '')
        self.assertEqual(betslip_day_and_time, self.expected_day_and_time,
                         msg=f'Actual Day from Betslip: {betslip_day_and_time} is not equal to expected day from Line summary:{self.expected_day_and_time}')
        # calculating estimations returns according to added selections
        # here we are getting use bonus ball odds from more info/lotto rules
        # Single bet verification
        self.lotto_bet.show_hide_multiples.click()
        selection1 = self.lotto_bet.items_as_ordered_dict.get('Single')
        selection1.amount_form.input.click()
        selection1.amount_form.input.value = self.stake
        single_bet_est_return_value = float(selection1.est_returns.replace(',',''))
        actual_single_bet_est_return_value = "{:.2f}".format(single_bet_est_return_value)
        single_estimation_returns = round((self.stake * 1) + (self.bonus_single_ball * self.stake), 2)*5
        expected_single_estimation_returns = "{:.2f}".format(single_estimation_returns)
        self.assertEqual(actual_single_bet_est_return_value, expected_single_estimation_returns,
                        msg=f'Actual single estimations returns {actual_single_bet_est_return_value} is not same as expected single estimations returns {expected_single_estimation_returns}')
        selection1.amount_form.input.clear()

        # Multiple bet verification
        selection2 = self.lotto_bet.items_as_ordered_dict.get('Double')
        selection2.amount_form.input.click()
        selection2.amount_form.input.value = self.stake
        double_bet_est_return_value = float(selection2.est_returns.replace(',', ''))
        actual_double_bet_est_return_value = "{:.2f}".format(double_bet_est_return_value)
        double_estimation_returns = round((self.stake * 1) + (self.bonus_double_ball * self.stake), 2) * 10
        expected_double_estimation_returns = "{:.2f}".format(double_estimation_returns)
        self.assertEqual(actual_double_bet_est_return_value, expected_double_estimation_returns,
                        msg=f'Actual double estimations returns {actual_double_bet_est_return_value} is not same as expected double estimations returns {expected_double_estimation_returns}')
        selection2.amount_form.input.clear()

    def test_008_verify_payout_at_estreturns_when_payout_is_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout is exceeds max payout
        EXPECTED: user can see the Payout limit exceeded message
        """
        # Verify max payout message in ui
        self.lotto_bet.amount_form.input.click()
        stake = round((self.max_payout+ 1) / (1 + self.main_winning_amount), 2) + 1
        self.lotto_bet.amount_form.input.click()
        self.lotto_bet.amount_form.input.value = stake
        self.assertTrue(self.site.lotto_betslip.has_max_payout_info(), msg="Max Payout limit message is not display")
        self.lotto_bet.amount_form.input.clear()
        # Verify max payout message for single
        bet_sections = self.lotto_bet.items_as_ordered_dict
        single_bet_section = bet_sections.get('Single')
        stake = round((self.max_payout + 1) / (1 + self.bonus_single_ball), 2) + 1
        single_bet_section.amount_form.input.click()
        single_bet_section.amount_form.input.value = stake
        self.assertTrue(self.site.lotto_betslip.has_max_payout_info(), msg="Max Payout limit message is not display for single")
        single_bet_section.amount_form.input.clear()
        # Verify max payout message for double
        double_bet_section = bet_sections.get('Double')
        stake = round((self.max_payout + 1) / (1 + self.bonus_double_ball), 2) + 1
        double_bet_section.amount_form.input.click()
        double_bet_section.amount_form.input.value = stake
        self.assertTrue(self.site.lotto_betslip.has_max_payout_info(), msg="Max Payout limit message is not display for double")