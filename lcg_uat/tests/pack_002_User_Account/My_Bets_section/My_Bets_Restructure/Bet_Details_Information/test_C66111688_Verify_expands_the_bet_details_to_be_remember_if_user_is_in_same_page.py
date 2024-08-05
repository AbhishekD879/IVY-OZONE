import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter


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
# This test is covering C66111687, C66111689
class Test_C66111688_Verify_expands_the_bet_details_to_be_remember_if_user_is_in_same_page(BaseBetSlipTest):
    """
    TR_ID: C66111688
    NAME: Verify expands the bet details to be remember if user is in same page
    DESCRIPTION: This test case verify expands the bet details to be remember if user is in same page
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True

    def verify_bet_details_state(self, bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        self.assertTrue(bet.has_bet_details(expected_result=True),
                        msg=f'Bet Details section is not displayed under {tab_name}')
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed by default under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under {tab_name}')

        self.site.open_my_bets_settled_bets()
        if tab_name == "Open tab":
            self.site.open_my_bets_open_bets()
            bet = next(
                iter(list(
                    self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
                None)
            self.assertIsNotNone(bet, msg='Bet is not available under Open tab')
        elif tab_name == "Cash Out tab":
            self.site.open_my_bets_cashout()
            bet = next(
                iter(list(
                    self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
                None)
            self.assertIsNotNone(bet, msg='Bet is not available under Cash Out tab')

        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is expanded under {tab_name} after navigating to other page')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under {tab_name}')

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
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_bet_details_state(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_bet_details_state(bet=cash_out_bet, tab_name='Cash Out tab')

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
        self.verify_bet_details_state(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_bet_details_state(bet=cash_out_bet, tab_name='Cash Out tab')

    def test_006_check_new_section_with_bet_detail_area_available(self):
        """
        DESCRIPTION: Check new section with bet detail area available
        EXPECTED: Bet detail area is available with expand and collapse
        """
        # Covered in above step

    def test_007_expand_the_bet_details_and_check_the_state_if_user_is_on_the_same_page(self):
        """
        DESCRIPTION: Expand the bet details and check the state if user is on the same page
        EXPECTED: Bet details area  state if to be remembered if  user is on the same page
        EXPECTED: ![](index.php?/attachments/get/7ede3c7b-c9d5-4d33-895f-c138edb435d3)
        """
        # Covered in above step

    def test_008_repeat_the_above_steps_for_cashout_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cashout tab
        EXPECTED: 
        """
        # Covered in above step
