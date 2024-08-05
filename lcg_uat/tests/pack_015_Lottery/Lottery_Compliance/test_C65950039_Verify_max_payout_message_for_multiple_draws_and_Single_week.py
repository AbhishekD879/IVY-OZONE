import pytest
import tests
import random
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul
from voltron.utils.exceptions.siteserve_exception import SiteServeException


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
class Test_C65950039_Verify_max_payout_message_for_multiple_draws_and_Single_week(Common):
    """
    TR_ID: C65950039
    NAME: Verify max payout message for multiple draws and Single week
    DESCRIPTION: This testcase verifies max payout message for multiple draws and Single week
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True
    line_name = 'Line 1'
    bet_amount = 0.10 if tests.settings.backend_env == 'prod' else 1
    is_first_time_draws_selection = True

    def generate_random_numbers(self):
        """
        DESCRIPTION :Generate 5 unique random numbers between 1 and 49
        """
        # Generate 5 unique random numbers between 1 and 49
        random_numbers = random.sample(range(1, 50), 5)
        return random_numbers

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

    def verify_betslip(self, draw_name, expected_day_and_time):
        lottery_name = "49's 6 Ball Draw" if self.brand == "bma" else "49's 6 Ball"

        # Common verification logic for both draws
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")

        lotto_bestslip_name = self.site.lotto_betslip
        numbers = ' '.join(item for item in self.lotto_numbers_str)

        lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(
            f"{lottery_name}-{draw_name}-{expected_day_and_time}-{numbers}"
        )

        lotto_bet.amount_form.input.click()
        lotto_bet.amount_form.input.value = self.bet_amount

        bet_slip_line_numbers = lotto_bet.betslip_selected_numbers
        self.assertListEqual(bet_slip_line_numbers, self.actual_selected_numbers,
                             msg=f'Actual numbers from FE: {bet_slip_line_numbers} is not the same as expected numbers: {self.actual_selected_numbers}')

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

        self.assertEqual(actual_est_return_value, expected_est_return_value,
                         msg=f'Actual total stake from FE: {actual_est_return_value} is not the same as '
                             f'expected total stake calculations: {expected_est_return_value}')

        if float(expected_est_return_value) <= self.max_payout:
            self.assertFalse(self.site.lotto_betslip.has_max_payout_info(),
                             msg=f'Max Payout limit message is display')
        else:
            self.site.lotto_betslip.max_payout_link.scroll_to_we()
            self.assertTrue(self.site.lotto_betslip.has_max_payout_info(),
                            msg="Max Payout limit message is not display")

        # Single bet verification
        lotto_bet.show_hide_multiples.click()

        single_selection = lotto_bet.items_as_ordered_dict.get('Single')
        single_selection.amount_form.input.click()
        single_selection.amount_form.input.value = self.bet_amount

        actual_single_bet_est_return_value = "{:.2f}".format(float(single_selection.est_returns.replace(',', '')))
        expected_single_bet_est_return_value = "{:.2f}".format(
            ((self.bet_amount * 1) + (self.single_ball_winning_amount * self.bet_amount)) * 5)

        self.assertEqual(actual_single_bet_est_return_value, expected_single_bet_est_return_value,
                         msg=f'Actual total stake from FE: {actual_single_bet_est_return_value} is not the same as expected total stake calculations: {expected_single_bet_est_return_value}')

        # Double bet verification
        double_selection = lotto_bet.items_as_ordered_dict.get('Double')
        double_selection.amount_form.input.click()
        double_selection.amount_form.input.value = self.bet_amount

        actual_double_bet_est_return_value = "{:.2f}".format(float(double_selection.est_returns.replace(',', '')))
        expected_double_bet_est_return_value = "{:.2f}".format(
            ((self.bet_amount * 1) + (self.double_ball_winning_amount * self.bet_amount)) * 10)

        self.assertEqual(actual_double_bet_est_return_value, expected_double_bet_est_return_value,
                         msg=f'Actual total stake from FE: {actual_double_bet_est_return_value} is not the same as expected total stake calculations: {expected_double_bet_est_return_value}')

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
        self.__class__.main_winning_amount = potential_returns.get(5)
        self.__class__.single_ball_winning_amount = potential_returns.get(1)
        self.__class__.double_ball_winning_amount = potential_returns.get(2)
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
        self.assertIsNotNone(dialog_popup, msg='Dialogue popup is not opened')
        #  generating random numbers to select numbers in select numbers dialogue page
        self.__class__.lotto_numbers = sorted(self.generate_random_numbers())
        self.__class__.lotto_numbers_str = [str(element) for element in self.lotto_numbers]
        # getting ui numbers from select numbers dialogue page
        ui_lotto_numbers = dialog_popup.number_selectors_ordered_dict
        # selecting random five numbers in select number dialogue page
        for lotto_number in self.lotto_numbers_str:
            ui_lotto_numbers.get(lotto_number).click()
            wait_for_haul(2)
        # checking whether add line button is visible or not in select numbers dialogue page
        self.assertTrue(dialog_popup.done_button.is_displayed(),
                        msg='add line button is not visible in select numbers dialogue')
        dialog_popup.done_button.click()
        # checking whether user is able to navigate "line summary" page
        current_url = self.device.get_current_url()
        self.assertIn("linesummary", current_url, msg='Not able to navigate to line summary page')

    def test_004_verify_the_line_summary_page(self):
        """
       DESCRIPTION: Verify the Line Summary Page
       EXPECTED: Able to see the Below Information
       EXPECTED: Added lines with chosen numbers
       EXPECTED: Available Draws Information
       EXPECTED: How Many weeks Information
       """
        # verifying "selection numbers" which user added from "choose number selection" dialogue popup page
        self.__class__.actual_selected_numbers = self.site.lotto.line_summary.line_section.items_as_ordered_dict.get(
            self.line_name).selected_numbers
        self.assertListEqual(self.actual_selected_numbers, self.lotto_numbers_str,
                             msg=f'Actual numbers from FE : {self.actual_selected_numbers} is not same expected numbers:{self.lotto_numbers_str}')

        # Verifying lucky buttons are available under "Choose Your Draws"
        choose_your_draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        length_choose_your_draws = len(choose_your_draws)

        if length_choose_your_draws > 0:
            # Selecting random draws for the first and second time
            self.__class__.first_draw_name, self.__class__.first_expected_day_and_time = self.select_random_draws(
                choose_your_draws)
            self.__class__.second_draw_name, self.__class__.second_expected_day_and_time = self.select_random_draws(
                choose_your_draws)

        else:
            raise SiteServeException('Draw buttons are not available under "Choose Your Draws"')

        # verifying week buttons are available under "How Many Weeks"
        weeks = self.site.lotto.line_summary.how_many_weeks_section.week_selections_items
        length_weeks = len(weeks)
        if length_weeks > 0:
            weeks['1'].click()
        else:
            raise SiteServeException('week buttons are not available under "How Many Weeks"')

    def test_005_choose_multiple_draws_and_single_week(self):
        """
        DESCRIPTION: Choose multiple draws and single week
        EXPECTED: Able to select multiple draws and single week
        """
        # covered in step 4

    def test_006_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg='add To Betslip is not visible in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()

    def test_007_enter_the_stake_and_verify_the_potential_returns_for_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for Multiple bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        self.verify_betslip(self.first_draw_name, self.first_expected_day_and_time)
        self.verify_betslip(self.second_draw_name, self.second_expected_day_and_time)

    def test_008_verify_payout_at_estreturns_when_payout_is_within_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout is within max payout
        EXPECTED: user could not see the Payout limit exceeded message
        """
        # covered in above steps
