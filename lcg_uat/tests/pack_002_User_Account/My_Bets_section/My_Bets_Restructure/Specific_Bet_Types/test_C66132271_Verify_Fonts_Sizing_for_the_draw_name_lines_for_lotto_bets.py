import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
import random


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.specific_bet_types
@pytest.mark.insprint_auto
@vtest
class Test_C66132271_Verify_Fonts_Sizing_for_the_draw_name_lines_for_lotto_bets(BaseBetSlipTest):
    """
    TR_ID: C66132271
    NAME: Verify Fonts, Sizing  for the  draw name ,lines for lotto bets
    DESCRIPTION: This test case verify Fonts, Sizing  for the  draw name ,lines for lotto bets
    PRECONDITIONS: User should login successfully with valid credentials
    PRECONDITIONS: Lottos data should be available
    """
    keep_browser_open = True
    bet_amount = 0.1

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

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: Lotto' page is opened with following New elements:
        """
        # Covered in below step

    def test_002_choose_your_lucky_dip(self):
        """
        DESCRIPTION: Choose Your Lucky Dip
        EXPECTED: Lucky dip pop up display with numbers
        """
        # Covered in below step

    def test_003_lucky3lucky4lucky5(self):
        """
        DESCRIPTION: Lucky3/Lucky4/Lucky5
        EXPECTED: 
        """
        # Covered in below step

    def test_004_click_on_any_of_number(self):
        """
        DESCRIPTION: Click on any of Number
        EXPECTED: User should able to select number and click on Add to line CTA
        """
        # Covered in below step

    def test_005_check_the_data_added_to_the_line(self):
        """
        DESCRIPTION: Check the data added to the line
        EXPECTED: Selected numbers should be shown with line summary
        """
        # Covered in below step

    def test_006_choose_your_draws_section(self):
        """
        DESCRIPTION: Choose your draws Section
        EXPECTED: User should able to select single draw
        """
        # Covered in below step

    def test_007_select_number_week_from_weeks_section(self):
        """
        DESCRIPTION: Select number week from weeks section
        EXPECTED: User should able to select 1 week
        """
        # Covered in below step

    def test_008_click_on_add_to_bet_slip(self):
        """
        DESCRIPTION: Click on add to bet slip
        EXPECTED: Selections are added to bet slip
        """
        # Covered in below step

    def test_009_enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter stake and click on place bet
        EXPECTED: Bet should be placed successfully
        """
        self.place_lotto_bet()

    def test_010_navigate_to_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Navigate to 'My Bets' item on Top Menu
        EXPECTED: My Bets' page/'Bet Slip' widget is opened
        """
        # Covered in below step

    def test_011_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: Check for the Lotto bets placed
        """
        # Covered in below step

    def test_012_check_the_font_size_color_of_the_lines(self):
        """
        DESCRIPTION: Check the font ,size, color of the lines
        EXPECTED: Font and size color should be as per Figma deign
        """
        self.site.open_my_bets_open_bets()
        lotto_tab_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_tab_opened, msg='Lotto tab is not opened under Open tab')
        lotto_bet = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.get(
            f"{self.lottery_name.lower()}-{self.draw_name.lower()}-{self.expected_day_and_time.lower()}-{self.lotto_numbers_str[-1]}")

        actual_font_size = lotto_bet.ball.css_property_value('font-size')
        actual_font_weight = lotto_bet.ball.css_property_value('font-weight')
        actual_color = lotto_bet.ball.css_property_value('color')
        actual_font_name = lotto_bet.ball.css_property_value('font-family').replace('"',"")

        expected_font_size = '18px'
        expected_font_weight = '700' if self.brand != 'bma' else '900'
        expected_color = 'rgba(43, 43, 43, 1)' if self.brand != 'bma' else 'rgba(65, 73, 78, 1)'
        expected_font_name = "Roboto Condensed" if self.brand != 'bma' else 'Lato, Arial, Helvetica Neue, Helvetica, sans-serif'
        expected_line_alignment = 'left'

        self.assertEqual(expected_font_size, actual_font_size)
        self.assertEqual(expected_font_weight, actual_font_weight)
        self.assertEqual(expected_color, actual_color)
        self.assertEqual(expected_font_name, actual_font_name)
        self.assertEqual(expected_line_alignment, lotto_bet.draw_name_alignment)

    def test_013_tab_on_settle__tab(self):
        """
        DESCRIPTION: Tab on 'Settle ' tab
        EXPECTED: Check Lotto bets available in settle tab
        """
        # Can't wait till Lotto bet got settled

    def test_014_check_the_font_size_color_of_the_lines(self):
        """
        DESCRIPTION: Check the font ,size, color of the lines
        EXPECTED: Font and size color should be as per Figma deign
        """
        # Can't wait till Lotto bet got settled
