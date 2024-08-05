import time
import re
import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
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
class Test_C65950027_Verify_whether_the_payouts_can_easily_be_changed(Common):
    """
    TR_ID: C65950027
    NAME: Verify whether the payouts can easily be changed
    DESCRIPTION: This testcase verifies whether the payouts can easily be changed
    PRECONDITIONS: 1.Lotto Menu Item should be created from CMS EDIT Menu
    PRECONDITIONS: 2.SVG ID should be configured in CMS-> Image Manager.
    """
    keep_browser_open = True
    stake = 0.1

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        get_lotto_main_page_config = cms_config.get_lotto_main_page_configuration()
        lotteries = get_lotto_main_page_config['lottoConfig']
        for lotto in lotteries:
            lotto_name = lotto['label']
            if lotto_name == cls.lottery_type:
                cms_config.update_lotto_lottery_cnfig(lottery_id=lotto['id'], maxPayOut=cls.before_max_payout)

    def verifying_max_payout_limit_updation_FE(self):
        self.site.login()
        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        self.site.lotto.lotto_carousel.click_item(self.lottery_type)
        # reading potential returns odds values
        potential_returns = self.site.lotto.tab_content.potential_returns.items_as_ordered_dict
        main_winning_amount = potential_returns.get(3)
        # selecting Lucky 4
        lucky_buttons = list(self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict.values())
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons[0].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                            timeout=5)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers Below" pop up is not found')
        lotto_selections = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(lotto_selections, msg='There is no lotto buttons')
        available_selections = len(lotto_selections)
        self._logger.debug('Number of available selections is: %s' % available_selections)
        choose_lucky_num_dialog.done_button.click()
        choose_lucky_num_dialog.wait_dialog_closed()
        lines = self.site.lotto.line_summary.line_section.items_as_ordered_dict
        line = lines.get('Line 1')
        # verifying Line summary
        selected_numbers_ui = line.selected_numbers
        url = self.device.get_current_url()
        self.assertIn('linesummary', url, msg='Line summary page is not open')
        # reading draws
        draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        self.assertIsNotNone(draws, msg="Draws are not present below choose your draws section")
        first_day_name, first_item = next(
            ((first_day_name, first_item) for first_day_name, first_item in draws.items()), None)
        time_draws = first_item.items_as_ordered_dict
        self.assertIsNotNone(time_draws, msg="Time draws are not available")
        first_time_draw_name, first_time_item = next(
            ((first_time_draw_name, first_item) for first_time_draw_name, first_item in time_draws.items()), None)
        first_time_item.click()
        # Time and date splitting based for bet slip
        time_from_st1 = first_time_draw_name.split()[-1]
        expected_time = ' '.join(first_time_draw_name.split()[:-1])
        expected_day = first_day_name[:-1] + ')' + ' ' + '-' + ' ' + time_from_st1
        # add to bet slip
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_enabled(),
                        msg="Add to Betslip button not enabled")
        self.site.lotto.line_summary.add_to_betslip.click()
        # verifying betslip
        lottery_name = f'{self.lottery_type.title()} 6 Ball Draw' if self.brand == "bma" else f'{self.lottery_type.title()} Lotto 6 Ball'
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")

        def format_string(input_string):
            words = input_string.split()
            formatted_words = []
            for word in words:
                if re.match(r'^\d', word):
                    # If the word starts with a number, convert it to lowercase
                    formatted_word = word.lower()
                else:
                    # Otherwise, convert it to title case
                    formatted_word = word.title()
                formatted_words.append(formatted_word)
            formatted_string = ' '.join(formatted_words)
            return formatted_string

        lotto_bestslip_name = self.site.lotto_betslip
        self.__class__.lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(
            format_string(f"{lottery_name}-{expected_time.lower()}-{expected_day}-{' '.join(selected_numbers_ui)}"))
        self.lotto_bet.amount_form.input.click()
        self.lotto_bet.amount_form.input.value = self.stake
        bet_slip_line_numbers = self.lotto_bet.betslip_selected_numbers
        # verifying Lucky 3 numbers
        self.assertListEqual(bet_slip_line_numbers, selected_numbers_ui,
                             msg=f'Actual numbers from FE : {bet_slip_line_numbers} is not same expected numbers:{selected_numbers_ui}')
        betslip_day = self.lotto_bet.draw_date.replace(', ', '')
        # verifying Draw Day in betslip
        self.assertEqual(betslip_day, expected_day,
                         msg=f'Actual Day from Betslip: {betslip_day} is not equal to expected day from Line summary:{expected_day}')
        betslip_time = self.lotto_bet.draw_heading
        # verifying Draw Time  in betslip
        self.assertEqual(betslip_time, format_string(expected_time),
                         msg=f'Actual time from Betslip: {betslip_time} is not equal to expected time from Line summary:{expected_time.title()}')
        stakes = [self.stake]
        for stake in stakes:
            # verifying Potential returns and max payout limit verifications
            est_return_value = round((stake * 1) + (main_winning_amount * stake), 2)
            if est_return_value > self.after_max_payout:
                self.site.lotto_betslip.max_payout_link.scroll_to_we()
                time.sleep(2)
                self.assertTrue(self.site.lotto_betslip.has_max_payout_info(),
                                msg="Max Payout limit message  is not display")
            else:
                self.assertFalse(self.site.lotto_betslip.has_max_payout_info(),
                                 msg="Max Payout limit message  is not display")
                self.lotto_bet.amount_form.input.click()
                self.lotto_bet.amount_form.input.value = stake + 1
                stakes.append(float(self.lotto_bet.amount_form.input.value))

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Verifying LOTTO is enabled or not
        """
        self.__class__.lottery_type = 'DAILY MILLIONS' if self.brand == 'ladbrokes' else 'DAILY MILLION'
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled'):
                raise CmsClientException('LOTTO Page is not configured')
        get_lotto_main_page_config = self.cms_config.get_lotto_main_page_configuration()
        lotteries = get_lotto_main_page_config['lottoConfig']
        for lotto in lotteries:
            lotto_name = lotto['label']
            expected_lottery_name = 'Daily Million' if self.brand == 'ladbrokes' else 'Daily Millions Lottery'
            if lotto_name == expected_lottery_name:
                self.__class__.before_max_payout = lotto['maxPayOut']
                expected_max_payout = 10.0
                after_change_lotto = self.cms_config.update_lotto_lottery_cnfig(lottery_id=lotto['id'],
                                                                                maxPayOut=expected_max_payout)
                self.__class__.after_max_payout = after_change_lotto['maxPayOut']
                self.assertEqual(self.after_max_payout, expected_max_payout,
                                 msg=f'Max payout amount: {self.after_max_payout} did not change in CMS'
                                     f' to the expected changed value: {expected_max_payout}')
                break

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should able to login successfully
        """
        # Covered in Preconditions

    def test_002_click_on_lotto_item_from_cms_main_navigation(self):
        """
        DESCRIPTION: Click on Lotto Item from CMS Main Navigation
        EXPECTED: Lotto Page should open with the existing details
        """
        # Covered in Preconditions

    def test_003_click_on_lottery_type_49s__irish_or_daily_million(self):
        """
        DESCRIPTION: Click on Lottery type (49's , Irish or Daily Million)
        EXPECTED: Lottery type is opened with all the details
        """
        # Covered in Preconditions

    def test_004_verify_max_payout_field(self):
        """
        DESCRIPTION: Verify Max payout field
        EXPECTED: Able to enter and alter the amounts from dropdown
        """
        # Covered in Preconditions

    def test_005_verify_whether_the_payouts_can_be_changed_easily_for_each_lottery_type_in_cms_49s_irish_and_daily_million(self):
        """
        DESCRIPTION: Verify whether the payouts can be changed easily for each Lottery type in CMS (49's, Irish and Daily million)
        EXPECTED: Able to change the payout from maximum payout feild given
        """
        # Covered in Preconditions

    def test_006_click_on_save_changes(self):
        """
        DESCRIPTION: Click on Save changes
        EXPECTED: Able to see the message- Are you sure you want to save this Lotto?
        """
        # Covered in Preconditions

    def test_007_click_on_yes(self):
        """
        DESCRIPTION: Click on Yes
        EXPECTED: Changes have been saved successfully message is displayed
        """
        self.verifying_max_payout_limit_updation_FE()
