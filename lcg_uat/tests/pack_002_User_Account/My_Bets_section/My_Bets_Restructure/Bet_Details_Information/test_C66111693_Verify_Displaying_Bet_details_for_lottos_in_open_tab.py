import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
import random
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_betsn
@pytest.mark.bet_details_information
@vtest
# This test is covering C66114116, C66114120, C66114121, C66132278
class Test_C66111693_Verify_Displaying_Bet_details_for_lottos_in_open_tab(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C66111693
    NAME: Verify Displaying Bet details for lotto's  in open tab
    DESCRIPTION: This test case verify Displaying Bet details for lotto's  in open tab
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True
    bet_amount = 0.1
    timezone = str(get_localzone())

    def get_expected_data_layer_reponce(self, action=None, tab_name='Open tab'):
        data_layer_responce = {
            "event": "Event.Tracking",
            "component.categoryevent": "betslip",
            "component.LabelEvent": "bet details",
            "component.ActionEvent": action,
            "component.PositionEvent": tab_name,
            "component.LocationEvent": "mybets",
            "component.EventDetails": "Lottos",
            "component.URLClicked": "not applicable",
            "component.contentPosition": 1
        }
        return data_layer_responce

    def place_lotto_bet(self):
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled') == True:
                raise CmsClientException('"LOTTO" Page is not configured')

        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        self.assertTrue(self.site.lotto.tab_content.choose_numbers.is_displayed(),
                        msg='choose numbers button is not present in lotto page')
        self.site.lotto.tab_content.choose_numbers.click()
        dialog_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=5)
        self.assertIsNotNone(dialog_popup, msg='Choose Numbers dialogue popup is not opened')
        lotto_numbers = sorted(random.sample(range(1, 50), 5))
        self.__class__.lotto_numbers_str = [str(element) for element in lotto_numbers]
        fe_lotto_numbers = dialog_popup.number_selectors_ordered_dict
        for lotto_number in self.lotto_numbers_str:
            fe_lotto_numbers.get(lotto_number).click()
        self.assertTrue(dialog_popup.done_button.is_displayed(),
                        msg='ADD LINE    button is not visible in Choose Numbers dialogue')
        dialog_popup.done_button.click()

        current_url = self.device.get_current_url()
        self.assertIn("linesummary", current_url,
                      msg='Not navigated to Line Summary page after clickng on ADD LINE button in Choose Numbers dialog')

        actual_selected_lotto_numbers = self.site.lotto.line_summary.line_section.items_as_ordered_dict.get(
            'Line 1').selected_numbers
        self.assertListEqual(actual_selected_lotto_numbers, self.lotto_numbers_str,
                             msg=f'Actual selected lotto numbers : {actual_selected_lotto_numbers} is not same expected lotto numbers :{self.lotto_numbers_str}')

        choose_your_draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        length_choose_your_draws = len(choose_your_draws)
        if length_choose_your_draws > 0:
            date_name = random.sample(list(choose_your_draws), 1)[0]
            time_draw = choose_your_draws[date_name].items_as_ordered_dict
            time_draw_name = random.sample(list(time_draw), 1)[0]
            words = (time_draw_name.split())[:-1]
            self.__class__.draw_name = ' '.join(word.capitalize() for word in words)
            self.__class__.expected_day_and_time = f'{date_name} - {time_draw_name.split()[-1]}'
            time_draw[time_draw_name].click()
        else:
            raise VoltronException('Draw buttons are not available under "choose your draws"')

        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg='ADD TO BETSLIP button is not displayed in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()
        # try:
        #     self.site.header.bet_slip_counter.click()
        # except VoltronException:
        #     self.site.betslip_notifcation.click()
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        lotto_betslip = self.site.lotto_betslip
        numbers = ' '.join(item for item in self.lotto_numbers_str)
        self.__class__.lottery_name = "49's 6 Ball Draw" if self.brand == "bma" else "49's 6 Ball"
        lotto_bet = lotto_betslip.betslip_sections_list.items_as_ordered_dict.get(
            f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{numbers}"
        )
        lotto_bet.show_hide_multiples.click()

        single_selection = lotto_bet.items_as_ordered_dict.get('Single')
        single_selection.amount_form.input.click()
        single_selection.amount_form.input.value = self.bet_amount

        self.site.lotto_betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        bet_receipt = self.site.lotto_bet_receipt
        bet_datetime = bet_receipt.receipt_header.bet_datetime
        time_obj = datetime.strptime(bet_datetime, '%d/%m/%Y, %H:%M')
        self.__class__.expected_bet_datetime = get_date_time_as_string(date_time_obj=time_obj, tz_region='UTC',
                                                                       time_format='%H:%M - %d %b')
        current_time = get_date_time_as_string(time_format='%H:%M', url_encode=False)
        current_time = datetime.strptime(current_time, '%H:%M')
        # If the timezone is UTC, adjust the current time by 60 minutes
        europe_london = get_date_time_as_string(time_format='%H:%M', url_encode=False, tz_region='EUROPE/LONDON')
        europe_london = datetime.strptime(europe_london, '%H:%M')
        time_difference = abs(current_time - europe_london)
        if time_difference.total_seconds() / 3600 >= 1:
            self.__class__.expected_bet_datetime = get_date_time_as_string(date_time_obj=time_obj, tz_region='UTC',
                                                                           time_format='%H:%M - %d %b', hours=1)
        lotto_bet = bet_receipt.items_as_ordered_dict.get(f"{self.lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{self.lotto_numbers_str[-1]}")
        self.__class__.expected_bet_receipt_id = lotto_bet.bet_id.split(': ')[1]
        self.__class__.expected_bet_stake = lotto_bet.outer_total_stake_value.replace(' ', '')
        self.__class__.expected_bet_potential_returns = lotto_bet.outer_est_returns_value.replace(' ', '')

    def verify_bet_details_section_for_lotto_bet(self, bet=None, tab_name='Lotto tab'):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        if self.device_type == 'mobile':
            self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                            msg=f'Share button is not displayed under {tab_name}')
            bet.bet_details.chevron_arrow.click()
            self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                            msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')
            self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                            msg=f'Share button is not displayed under {tab_name} after expanded the Bet Details')
            bet.bet_details.chevron_arrow.click()
            self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                             msg=f'Bet Details is not collapsed after click on Bet Details chevron under {tab_name}')
            self.assertTrue(bet.bet_details.has_share_button(expected_result=True),
                            msg=f'Share button is not displayed under {tab_name} after collapsing the Bet Details')
            potential_returns_y_value = bet.potential_returns.location['y']
            share_button_y_value = bet.bet_details.share_button.location['y']
            self.assertTrue(potential_returns_y_value < share_button_y_value,
                            msg=f'potential returns are not above the share button under {tab_name}')
        bet.chevron_arrow.click()
        self.assertFalse(bet.is_expanded(expected_result=False),
                         msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')

        self.assertFalse(bet.has_bet_details(expected_result=False),
                         msg=f'Bet Details section is displayed under {tab_name}')
        bet.chevron_arrow.click()
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded after clicking on chevron arrow under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='expand')
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

        bet.bet_details.chevron_arrow.click()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed after clicking on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                         object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='collapse')
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)
        
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details is not expanded after click on Bet Details chevron under {tab_name}')

        expected_bet_type = f"DRAW TYPE:  {self.lottery_name.upper()}"

        actual_bet_receipt_id = bet.bet_details.bet_receipt.text.replace('\n', '').upper()
        actual_bet_datetime = bet.bet_details.bet_date_time.replace('\n', '').upper()
        actual_bet_type = bet.bet_details.bet_type.replace('\n', '').upper()
        actual_bet_number_of_lines = bet.bet_details.bet_number_of_lines.replace('\n', '').upper()
        actual_bet_stake_per_line = bet.bet_details.bet_stake_per_line.replace('\n', '').upper()
        actual_bet_total_stake = bet.bet_details.bet_total_stake.replace('\n', '').upper()
        actual_bet_potential_returns = bet.bet_details.bet_potential_returns.replace('\n', '').upper()

        self.assertEqual(f'BET RECEIPT:  {self.expected_bet_receipt_id.upper()}', actual_bet_receipt_id)
        # self.assertEqual(f'BET PLACED:  {self.expected_bet_datetime.upper()}', actual_bet_datetime)
        self.assertEqual(f'{expected_bet_type}', actual_bet_type)
        self.assertEqual(f'NUMBER OF LINES: 1', actual_bet_number_of_lines)
        self.assertEqual(f'STAKE PER LINE:  £{self.expected_bet_stake}', actual_bet_stake_per_line)
        self.assertEqual(f'TOTAL STAKE:  £{self.expected_bet_stake}', actual_bet_total_stake)
        self.exp_bet_potential_returns = f'POTENTIAL RETURNS: N/A' if self.expected_bet_potential_returns == 'N/A' else f'POTENTIAL RETURNS: £{self.expected_bet_potential_returns}'
        self.assertEqual(f'{self.exp_bet_potential_returns}', actual_bet_potential_returns)

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_001_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_002_navigate_lotto__page(self):
        """
        DESCRIPTION: Navigate Lotto  page
        EXPECTED: Lotto page should be opened
        """
        # Covered in below step

    def test_003_place_bets__on_lotto(self):
        """
        DESCRIPTION: Place bets  on Lotto
        EXPECTED: Bets should be placed successfully
        """
        self.place_lotto_bet()

    def test_004_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        pass

    def test_005_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_006_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        pass

    def test_007_check_the_bet_detail_information__for_lotto__bets_placed(self):
        """
        DESCRIPTION: Check the bet detail information  for lotto  bets placed
        EXPECTED: Bet detail information should be as per Figma for lotto bets
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/76f88ece-5a18-4741-868b-a9111ee62442)
        """
        self.site.open_my_bets_open_bets()
        lotto_tab_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_tab_opened, msg='Lotto tab is not opened under Open tab')

        lotto_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.get(
            f"{self.lottery_name.lower()}-{self.draw_name.lower()}-{self.expected_day_and_time.lower()}-{self.lotto_numbers_str[-1]}")

        self.verify_bet_details_section_for_lotto_bet(bet=lotto_bet)
