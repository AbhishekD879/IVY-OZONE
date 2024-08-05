import pytest
import tests
from tests.base_test import vtest
import random
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS


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
class Test_C65950044_Verify_est_returns_after_betplacement_in_bet_receipt_and_my_bets(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C65950044
    NAME: Verify est returns after betplacement in bet receipt and my bets
    DESCRIPTION: This test case is to verify est returns after betplacement in bet receipt and my bets
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True
    stake = 0.30

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
                self.__class__.bonus_single_ball = float(lottery_prices_list['lotteryPrice']['priceNum'])/float(lottery_prices_list['lotteryPrice']['priceDen'])
            if lottery_prices_list['lotteryPrice']['numberCorrect'] == '2' and lottery_prices_list['lotteryPrice']['numberPicks'] == '2':
                self.__class__.bonus_double_ball = float(lottery_prices_list['lotteryPrice']['priceNum'])/float(lottery_prices_list['lotteryPrice']['priceDen'])
        # verifying lotto page is disable or not in cms
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle').upper() == "LOTTO" and sport_category.get('disabled'):
                raise CmsClientException('"LOTTO" Page is not configured')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        self.site.login(username=tests.settings.betplacement_user)

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
                        msg='choose numbers button is not present in lotto page')
        self.site.lotto.tab_content.choose_numbers.click()

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to choose numbers and could able to add the line and navigated to Line Summary page
        """
        # verifying whether select number dialogue popup is visible or not in lotto page
        dialog_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=5)
        self.assertIsNotNone(dialog_popup, msg='Choose Numbers dialogue popup is not opened')
        #  generating random numbers to select numbers in select numbers dialogue page
        self.__class__.lotto_numbers = self.generate_random_numbers()
        # getting ui numbers from select numbers dialogue page
        ui_lotto_numbers = dialog_popup.number_selectors_ordered_dict
        # selecting random five numbers in select number dialogue page
        for lotto_number in self.lotto_numbers:
            ui_lotto_numbers.get(str(lotto_number)).click()
            wait_for_haul(2)
        # checking whether add line button is visible or not in select numbers dialogue page
        self.assertTrue(dialog_popup.done_button.is_displayed(), msg='add line button is not visible in choose numbers dialogue')
        dialog_popup.done_button.click()
        # checking whether user is able to navigate "line summary" page
        self.assertEqual("LINE SUMMARY", self.site.lotto.header_line.page_title.text.upper(), msg='Not able to navigate to line summary page')

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
            first_day_name, first_item = next(
                ((first_day_name, first_item) for first_day_name, first_item in choose_your_draws.items()), (None, None))
            time_draws = first_item.items_as_ordered_dict
            first_time_draw_name, first_time_item = next(
                ((first_time_draw_name, first_item) for first_time_draw_name, first_item in time_draws.items()), (None, None))
            words = (first_time_draw_name.split())[:-1]
            self.__class__.draw_name = ' '.join(word.capitalize() for word in words)
            self.__class__.expected_day_and_time = f'{first_day_name} - {first_time_draw_name.split()[-1]}'
            first_time_item.click()
        else:
            raise SiteServeException('lucky buttons are not available under "choose your draws"')
        # verifying week buttons are available under "How Many Weeks"
        one_week = next((week for week_number, week in self.site.lotto.line_summary.how_many_weeks_section.week_selections_items.items() if week_number == '1') , None)
        self.assertIsNotNone(one_week, msg='week buttons are not available under "How Many Weeks"')
        one_week.click()

    def test_005_verify_adding_bonus_ball(self):
        """
        DESCRIPTION: Verify adding Bonus ball
        EXPECTED: user can able to add the bonus ball
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
                        msg='User is not able to click on "User Bonus Ball" check box')

    def test_006_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg='add To Betslip is not visible in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()

    def test_007_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        self.__class__.lottery_name = "49's 7 Ball Draw" if self.brand == "bma" else "49's 7 Ball"
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        self.__class__.lotto_bet = self.site.lotto_betslip.betslip_sections_list.items_as_ordered_dict.get(
            f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{self.numbers}")
        self.assertIsNotNone(self.lotto_bet, msg=f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{self.numbers} lotto bet is not displayed")
        # calculating estimations returns according to added selections
        # here we are getting use bonus ball odds from more info/lotto rules
        # Single bet verification
        self.lotto_bet.show_hide_multiples.click()
        selection1 = self.lotto_bet.items_as_ordered_dict.get('Single')
        selection1.amount_form.input.click()
        selection1.amount_form.input.value = self.stake
        single_bet_est_return_value = float(selection1.est_returns.replace(',', ''))
        actual_single_bet_est_return_value = "{:.2f}".format(single_bet_est_return_value)
        single_estimation_returns = round((1 + self.bonus_single_ball) * self.stake, 2) * 5
        expected_single_estimation_returns = "{:.2f}".format(single_estimation_returns)
        self.assertEqual(actual_single_bet_est_return_value, expected_single_estimation_returns,
                         msg=f'Actual single estimations returns {actual_single_bet_est_return_value} is not same as expected single estimations returns {expected_single_estimation_returns}')

        # Multiple bet verification
        selection2 = self.lotto_bet.items_as_ordered_dict.get('Double')
        selection2.amount_form.input.click()
        selection2.amount_form.input.value = self.stake
        double_bet_est_return_value = float(selection2.est_returns.replace(',', ''))
        actual_double_bet_est_return_value = "{:.2f}".format(double_bet_est_return_value)
        double_estimation_returns = round((1 + self.bonus_double_ball) * self.stake, 2) * 10
        expected_double_estimation_returns = "{:.2f}".format(double_estimation_returns)
        self.assertEqual(actual_double_bet_est_return_value, expected_double_estimation_returns,
                         msg=f'Actual double estimations returns {actual_double_bet_est_return_value} is not same as expected double estimations returns {expected_double_estimation_returns}')

    def test_008_verify_payout_at_estreturns_when_payout_is_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout is exceeds max payout
        EXPECTED: user can see the Payout limit exceeded message
        """
        # covered in test case id : C65950043

    def test_009_click_on_place_bet(self):
        """
        DESCRIPTION: Click on place bet
        EXPECTED: user unable to place bet-stake too high msg is displayed
        """
        self.site.lotto_betslip.bet_now_button.click()
        self.assertTrue(self.site.lotto_betslip.has_bet_now_button, msg='Betbutton is not present in Betslip')

    def test_010_verify_est_returns_after_betplacement_in_bet_receipt_and_my_bets(self):
        """
        DESCRIPTION: Verify est returns after betplacement in bet receipt and my bets
        EXPECTED: est returns should be the same as max payout in bet receipt and in my bets
        """
        # ************bet receipt estimation returns validation*************
        lotto_bet_receipt_list = self.site.lotto_bet_receipt.items_as_ordered_dict
        # verifying estimation returns for singles in bet receipt
        for number in self.expected_select_numbers:
            lotto_bet_receipt = lotto_bet_receipt_list.get(f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{number}")
            stake_value = float(lotto_bet_receipt.total_stake_value)
            single_stake_value = float("{:.2f}".format(stake_value))
            outer_stake_value = float(lotto_bet_receipt.outer_total_stake_value)
            outer_single_stake_value = float("{:.2f}".format(outer_stake_value))
            single_est_returns = float(lotto_bet_receipt.est_returns_value)
            act_single_est_returns = float("{:.2f}".format(single_est_returns))
            outer_single_est_returns = float(lotto_bet_receipt.outer_est_returns_value)
            act_outer_single_est_returns = float("{:.2f}".format(outer_single_est_returns))
            single_estimation_returns = (single_stake_value * 1) + (single_stake_value * self.bonus_single_ball)
            exp_single_estimation_returns = float("{:.2f}".format(single_estimation_returns))
            outer_single_estimation_returns = (outer_single_stake_value * 1) + (outer_single_stake_value * self.bonus_single_ball)
            outer_exp_single_estimation_returns = float("{:.2f}".format(outer_single_estimation_returns))
            self.assertEqual(act_single_est_returns, exp_single_estimation_returns, msg=f'Actual single estimation returns {act_single_est_returns} is not same as Expected single estimation returns {exp_single_estimation_returns}')
            self.assertEqual(act_outer_single_est_returns, outer_exp_single_estimation_returns, msg=f'Actual outer single estimation returns {act_outer_single_est_returns} is not same as Expected outer single estimation returns {outer_exp_single_estimation_returns}')
        # verifying estimation returns for doubles in bet receipt
        lotto_bet_receipt = lotto_bet_receipt_list.get(f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{self.numbers}")
        stake_value = float(lotto_bet_receipt.total_stake_value)
        double_stake_value = float("{:.2f}".format(stake_value))
        outer_stake_value = float(lotto_bet_receipt.outer_total_stake_value)
        outer_double_stake_value = float("{:.2f}".format(outer_stake_value))
        double_est_returns = float(lotto_bet_receipt.est_returns_value)
        act_double_est_returns = float("{:.2f}".format(double_est_returns))
        double_estimation_returns = (double_stake_value * 1) + (double_stake_value * self.bonus_double_ball)
        exp_double_estimation_returns = float("{:.2f}".format(double_estimation_returns))
        outer_double_est_returns = float(lotto_bet_receipt.outer_est_returns_value)
        act_outer_double_est_returns = float("{:.2f}".format(outer_double_est_returns))
        outer_double_estimation_returns = (outer_double_stake_value * 1) + (outer_double_stake_value * self.bonus_double_ball)
        exp_outer_double_estimation_returns = float("{:.2f}".format(double_estimation_returns))
        self.assertEqual(act_double_est_returns, exp_double_estimation_returns, msg=f'Actual double estimation returns {act_double_est_returns} is not same as Expected double estimation returns {exp_double_estimation_returns}')
        self.assertEqual(outer_double_estimation_returns, exp_outer_double_estimation_returns, msg=f'Actual outer double estimation returns {act_outer_double_est_returns} is not same as Expected outer double estimation returns {exp_outer_double_estimation_returns}')

        # ************lotto my bets estimation returns validation*************
        self.site.open_my_bets_open_bets()
        lotto_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')
        lott_open_bet_items = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        # verifying estimation returns for singles in open bet lotto bets
        for number in self.expected_select_numbers:
            lotto_open_bet_data = lott_open_bet_items.get(f"{self.lottery_name.lower()}-{self.draw_name.lower()}-{self.expected_day_and_time.lower()}-{number}")
            stake_value = float(lotto_open_bet_data.total_stake_value)
            ob_lotto_single_stake_value = float("{:.2f}".format(stake_value))
            single_est_returns = float(lotto_open_bet_data.potential_returns_value)
            ob_lotto_act_single_est_returns = float("{:.2f}".format(single_est_returns))
            single_estimation_returns = (ob_lotto_single_stake_value * 1) + (ob_lotto_single_stake_value * self.bonus_single_ball)
            ob_lotto_exp_single_estimation_returns = float("{:.2f}".format(single_estimation_returns))
            self.assertEqual(ob_lotto_act_single_est_returns, ob_lotto_exp_single_estimation_returns,
                             msg=f'Actual single estimation returns {ob_lotto_act_single_est_returns} is not same as Expected single estimation returns {ob_lotto_exp_single_estimation_returns}')
        # verifying estimation returns for doubles in open bet lotto bets
        lotto_open_bet_data = lott_open_bet_items.get(f"{self.lottery_name.lower()}-{self.draw_name.lower()}-{self.expected_day_and_time.lower()}-{self.numbers}")
        stake_value = float(lotto_open_bet_data.total_stake_value)
        ob_lotto_single_stake_value = float("{:.2f}".format(stake_value))
        single_est_returns = float(lotto_open_bet_data.potential_returns_value)
        ob_lotto_act_single_est_returns = float("{:.2f}".format(single_est_returns))
        single_estimation_returns = (ob_lotto_single_stake_value * 1) + (ob_lotto_single_stake_value * self.bonus_double_ball)
        ob_lotto_exp_single_estimation_returns = float("{:.2f}".format(single_estimation_returns))
        self.assertEqual(ob_lotto_act_single_est_returns, ob_lotto_exp_single_estimation_returns,
                         msg=f'Actual lotto open bet single estimation returns {ob_lotto_act_single_est_returns} is not same as Expected lotto open bet single estimation returns {ob_lotto_exp_single_estimation_returns}')


