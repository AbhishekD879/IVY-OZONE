import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


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
# This test covering C66111684, C66132044
class Test_C66111683_Verify_Bet_Details_area_to_contain_Collapsible__Expandable_Bet_Details_section(BaseBetSlipTest):
    """
    TR_ID: C66111683
    NAME: Verify Bet Details area to contain Collapsible / Expandable Bet Details section
    DESCRIPTION: This test case Verify Bet Details area to contain Collapsible / Expandable Bet Details section
    PRECONDITIONS: Bets should be available in open/cashout and settle tab
    """
    keep_browser_open = True

    def verify_bet_details_section(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.has_bet_details(expected_result=True),
                        msg=f'Bet Details section is not displayed under {tab_name}')
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                        msg=f'Bet Details section is not collapsed by default under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed after click on Bet Details chevron under {tab_name}')
        self.assertTrue(bet.has_stake(expected_result=True),
                        msg=f'Stake is not displayed after collapsing the Bet Details section under {tab_name}')
        self.assertTrue(bet.has_potential_returns(expected_result=True),
                        msg=f'Potential returns is not displayed after collapsing the Bet Details section under {tab_name}')
        bet.chevron_arrow.click()
        self.assertFalse(bet.is_expanded(expected_result=False),
                         msg=f'Bet is not collapsed after clicking on chevron arrow under {tab_name}')
        self.assertFalse(bet.has_bet_details(expected_result=False),
                         msg=f'Bet Details section is displayed under {tab_name}')
        bet.chevron_arrow.click()
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded after clicking on chevron arrow under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 3
        self.__class__.selection_ids = []
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        hr_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=self.number_of_events)
        for hr_event in hr_events:
            match_result_market = next((market['market'] for market in hr_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            outcomes = match_result_market['children']
            hr_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes if
                                    'Unnamed' not in i['outcome']['name']}
            hr_selection_id = list(hr_all_selection_ids.values())[0]
            self.selection_ids.append(hr_selection_id)

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

    def test_003_place_singlemutiple_bets__from_sportsraces(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports/Races
        EXPECTED: Bets should be placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        # Covered in below step

    def test_005_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        self.site.open_my_bets_open_bets()

    def test_006_check_new_section_with_bet_detail_area_available_with__chevron(self):
        """
        DESCRIPTION: Check new section with bet detail area available with  Chevron
        EXPECTED: Bet detail area is available with expand and collapse
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/acd51664-6164-4c4c-9c6e-932ba1f15097)    ![](index.php?/attachments/get/30d76c8e-0493-42df-85b2-b3340c1b03fe)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/2f5fbd21-010f-4fe0-9b59-7893bc9f6ba1)
        """
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_bet_details_section(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_bet_details_section(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
                           None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_bet_details_section(bet=settled_bet, tab_name='Settled tab')

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_bet_details_section(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_bet_details_section(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_bet_details_section(bet=settled_bet, tab_name='Settled tab')
