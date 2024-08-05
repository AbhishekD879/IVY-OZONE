import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from datetime import datetime
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@vtest
# This test covering C66111702
class Test_C66111691_Verify_Displaying_Bet_details_in_Pre_play_for_sports_in_open_tab(BaseBetSlipTest):
    """
    TR_ID: C66111691
    NAME: Verify Displaying Bet details in Pre-play for sports in open tab
    DESCRIPTION: This test case verify Displaying Bet details in Pre-play for sports in open tab
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True
    bet_amount = 0.05
    timezone = str(get_localzone())

    def verify_bet_details_section_content(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.has_bet_details(expected_result=True),
                        msg=f'Bet Details section is not displayed under {tab_name}')
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed by default under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under {tab_name}')
        expected_bet_type = 'BET TYPE:  SINGLE'
        actual_bet_receipt_id = bet.bet_details.bet_receipt.text.replace('\n', '').upper()
        actual_bet_datetime = bet.bet_details.bet_date_time.replace('\n', '').upper()
        actual_bet_type = bet.bet_details.bet_type.replace('\n', '').upper()
        actual_bet_number_of_lines = bet.bet_details.bet_number_of_lines.replace('\n', '').upper()
        actual_bet_stake_per_line = bet.bet_details.bet_stake_per_line.replace('\n', '').upper()
        actual_bet_total_stake = bet.bet_details.bet_total_stake.replace('\n', '').upper()
        actual_bet_potential_returns = bet.bet_details.bet_potential_returns.replace('\n', '').upper()
        self.assertEqual(f'BET RECEIPT:  {self.expected_bet_receipt_id.upper()}', actual_bet_receipt_id)
        self.assertEqual(f'BET PLACED:  {self.expected_bet_datetime.upper()}', actual_bet_datetime)
        self.assertEqual(f'{expected_bet_type}', actual_bet_type)
        self.assertEqual(f'NUMBER OF LINES: {self.num_of_selections}', actual_bet_number_of_lines)
        self.assertEqual(f'STAKE PER LINE:  £{self.bet_amount}', actual_bet_stake_per_line)
        self.assertEqual(f'TOTAL STAKE:  £{(self.bet_amount * self.num_of_selections)}', actual_bet_total_stake)
        self.exp_bet_potential_returns = f'POTENTIAL RETURNS: N/A' if self.expected_bet_potential_returns == 'N/A' else f'POTENTIAL RETURNS: £{self.expected_bet_potential_returns}'
        self.assertEqual(f'{self.exp_bet_potential_returns}', actual_bet_potential_returns)

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 1
        self.__class__.num_of_selections = 1
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=cashout_filter,
                                                    number_of_events=1)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_003_navigate_to_any_sports_page(self):
        """
        DESCRIPTION: Navigate to any sports page
        EXPECTED: Sports page should be opened
        """
        # Covered in below step

    def test_004_place_singlemutiple_bets__from_sports_for_pre_play_events(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports for pre-play events
        EXPECTED: Bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        bet_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        bet_receipt = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict.get('Single')
        self.__class__.expected_bet_receipt_id = bet_receipt.bet_id
        bet_datetime = self.site.bet_receipt.receipt_header.bet_datetime
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

        self.__class__.expected_bet_total_stake = bet_info.get('total_stake')
        self.__class__.expected_bet_potential_returns = bet_info.get('total_estimate_returns')
        parts = str(self.expected_bet_potential_returns).split('.')
        if len(parts) > 1 and len(parts[1]) == 1:
            self.__class__.expected_bet_potential_returns = f"{parts[0]}.{parts[1]}0"

    def test_005_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: ** My bets page/Bet slip widget is opened
        EXPECTED: ** Open'  tab is selected by default
        EXPECTED: ** Placed bet is displayed
        """
        # Covered in below step

    def test_006_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        # Covered in below step

    def test_007_check_the_bet_detail_information_for_sports_singlesmultiples_for__bets_placed_for_pre_play_events(self):
        """
        DESCRIPTION: Check the bet detail information for sports singles/multiples for  bets placed for pre play events
        EXPECTED: Bet detail information should be as per Figma for pre play events
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/9428e33c-6e1e-4b36-835b-a04a5147a80b)
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_bet_details_section_content(bet=open_tab_bet, tab_name='Open tab')
        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_bet_details_section_content(bet=cash_out_bet, tab_name='Cash Out tab')

    def test_008_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED:
        """
        # Covered in above step