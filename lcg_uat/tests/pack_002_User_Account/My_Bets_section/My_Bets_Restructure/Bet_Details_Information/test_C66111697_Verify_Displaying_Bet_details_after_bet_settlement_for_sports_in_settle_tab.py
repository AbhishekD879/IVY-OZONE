import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from datetime import datetime
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone
from voltron.utils.bpp_config import BPPConfig
from voltron.utils.helpers import get_matching_response_url, do_request


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
class Test_C66111697_Verify_Displaying_Bet_details_after_bet_settlement_for_sports_in_settle_tab(BaseBetSlipTest):
    """
    TR_ID: C66111697
    NAME: Verify Displaying Bet details after bet settlement  for sports in settle tab
    DESCRIPTION: This test case verify Displaying Bet details after bet settlement  for sports in settle tab
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True
    bet_amount = 0.05
    timezone = str(get_localzone())
    bpp_config = BPPConfig()

    def get_settled_bets_for_user(self, bpp_user_token: str, url):
        import urllib.parse
        """
        Retrieve data with available settled bets for specified user
        :param bpp_user_token: Unique user BPP token
        :url: URL to which we need to send the request
        :return: Tuple containing the updated URL if a paging token exists, and the response
        """
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'https:{tests.HOSTNAME}',
            'token': bpp_user_token
        }
        self._logger.debug(f'*** Request url {url}')
        r = do_request(method='GET', url=url, headers=headers)

        updated_url = None

        if "paging" in r['response']['model'] and r['response']['model']["paging"].get("token"):
            # Parse the provided URL
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # Parameters to update
            new_params = {
                "blockSize": query_params.get("blockSize", ["20"])[0],  # Default to 20 if not present
                "pagingToken": r['response']['model']["paging"]["token"]
            }

            # Remove unwanted parameters
            for param in ["fromDate", "toDate", "group", "settled", "pagingBlockSize", "ev_category_id", "bet_type"]:
                query_params.pop(param, None)

            # Update the parameters with new values
            query_params.update(new_params)

            # Construct the new query string
            new_query_string = urllib.parse.urlencode(query_params, doseq=True)

            # Construct the updated URL
            updated_url = urllib.parse.urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query_string,
                parsed_url.fragment
            ))

        return updated_url, r

    def get_all_settled_bets_for_user(self, url, bpp_user_token):
        """
        Retrieve all settled bets for the specified user, handling pagination.
        :param url: Initial URL for retrieving settled bets
        :param bpp_user_token: Unique user BPP token
        :return: List of all settled bets
        """
        all_bets = []
        all_pool_bets = []
        all_lotto_bets = []
        current_url = url

        while current_url:
            updated_url, response = self.get_settled_bets_for_user(url=current_url, bpp_user_token=bpp_user_token)
            try:
                bets = response['response']["model"]["bet"]
                all_bets.extend(bets)
            except KeyError:
                pass
            if 'poolBet' in response['response']['model']:
                pool_bets = response['response']["model"]['poolBet']
                all_pool_bets.extend(pool_bets)
            if 'lottoBetResponse' in response['response']['model']:
                lotto_bets = response['response']["model"]['lottoBetResponse']
                all_lotto_bets.extend(lotto_bets)
            current_url = updated_url
        combined_bets = []
        combined_bets.extend(all_bets)
        combined_bets.extend(all_pool_bets)
        combined_bets.extend(all_lotto_bets)
        return combined_bets

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
        actual_bet_settled = bet.bet_details.bet_settled.replace('\n', '').upper()
        actual_bet_number_of_winning_lines = bet.bet_details.bet_number_of_winning_lines.replace('\n', '').upper()
        actual_bet_number_of_losing_lines = bet.bet_details.bet_number_of_losing_lines.replace('\n', '').upper()
        actual_bet_potential_returns = bet.bet_details.bet_potential_returns.replace('\n', '').upper()

        actual_url = get_matching_response_url(self, urls=['/accountHistory'])
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        all_bets = self.get_all_settled_bets_for_user(
            url=actual_url, bpp_user_token=bpp_token)
        for bet in all_bets:
            if bet['receipt'].upper() == self.expected_bet_receipt_id.upper():
                expected_bet_number_of_winning_lines = bet['numLinesWin']
                expected_bet_number_of_losing_lines = bet['numLinesLose']
                break

        self.assertEqual(f'BET RECEIPT:  {self.expected_bet_receipt_id.upper()}', actual_bet_receipt_id)
        self.assertEqual(f'BET PLACED:  {self.expected_bet_datetime.upper()}', actual_bet_datetime)
        self.assertEqual(f'{expected_bet_type}', actual_bet_type)
        self.assertEqual(f'NUMBER OF LINES: {self.num_of_selections}', actual_bet_number_of_lines)
        self.assertEqual(f'STAKE PER LINE:  £{self.bet_amount}', actual_bet_stake_per_line)
        self.assertEqual(f'TOTAL STAKE:  £{(self.bet_amount * self.num_of_selections)}', actual_bet_total_stake)
        self.assertEqual(f'SETTLED:  Y', actual_bet_settled)
        self.assertEqual(f'NO. OF WINNING LINES:  {expected_bet_number_of_winning_lines}', actual_bet_number_of_winning_lines)
        self.assertEqual(f'NO. OF LOSING LINES:  {expected_bet_number_of_losing_lines}', actual_bet_number_of_losing_lines)
        self.exp_bet_potential_returns = f'RETURNS: N/A' if self.expected_bet_potential_returns == 'N/A' else f'RETURNS: £{self.expected_bet_potential_returns}'
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

    def test_004_place_singlemutiple_bets__from_sports_for_in_play_events(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports for In-play events
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

    def test_005_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Betslip widget is opened
        """
        # Covered in below step

    def test_006_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        # Covered in below step

    def test_007_check_the_bets_placed_for_singlemultiples(self):
        """
        DESCRIPTION: Check the bets placed for single/multiples
        EXPECTED: Bets should be available in open tab
        """
        # Covered in below step

    def test_008_click_on_settle_tab_after_the_above_bets_are_settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above bets are settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        # Covered in below step

    def test_009_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        # Covered in below step

    def test_010_check_the_bet_detail_information_for_sports_singlesmultiples_for_settled(self):
        """
        DESCRIPTION: Check the bet detail information for sports singles/multiples for settled
        EXPECTED: Bet detail information should be as per Figma in settle tab
        EXPECTED: SS:
        EXPECTED: ![](index.php?/attachments/get/369b0f97-ada8-46fa-94f9-ab21841d4b52)
        """
        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.__class__.expected_bet_potential_returns = cash_out_bet.you_cashed_out_message.name.split('£')[1]
        parts = str(self.expected_bet_potential_returns).split('.')
        if len(parts) > 1 and len(parts[1]) == 1:
            self.__class__.expected_bet_potential_returns = f"{parts[0]}.{parts[1]}0"

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
                           None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_bet_details_section_content(bet=settled_bet, tab_name='Settled tab')