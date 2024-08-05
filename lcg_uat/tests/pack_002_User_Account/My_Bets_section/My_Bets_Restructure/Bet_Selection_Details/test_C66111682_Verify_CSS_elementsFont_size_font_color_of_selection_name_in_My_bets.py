import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.exceptions import SiteServeException

from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@vtest
@pytest.mark.timeout(1000)
# This test covering C66111704, C66111705, C66111706 tests
class Test_C66111682_Verify_CSS_elementsFont_size_font_color_of_selection_name_in_My_bets(BaseBetSlipTest):
    """
    TR_ID: C66111682
    NAME: Verify CSS elements(Font size, font color )of selection name in My bets
    DESCRIPTION: This testcase verifies CSS elements(Font size, color) of selection name in my bets
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def verify_my_bets_elements_font_color_size(self, bets=[], tab_name=None, item=None):

        test_data = {'selection': {'font size': '13px', 'color': 'rgba(51, 51, 51, 1)',
                                   'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'market': {'font size': '11px', 'color': 'rgba(43, 43, 43, 1)',
                                'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'event': {'font size': '11px', 'color': 'rgba(43, 43, 43, 1)',
                               'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'odds': {'font size': '13px', 'color': 'rgba(51, 51, 51, 1)',
                              'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'potential returns label': {'font size': '12px', 'color': 'rgba(51, 51, 51, 1)',
                                                 'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif',
                                                 'font weight': '400'},
                     'potential returns value': {'font size': '12px', 'color': 'rgba(51, 51, 51, 1)',
                                                 'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif',
                                                 'font weight': '700'}
                     }
        for i in range(len(bets)):
            element = None
            if item == 'selection':
                element = bets[i].selection
            elif item == 'market':
                element = bets[i].market
            elif item == 'event':
                element = bets[i].event
            elif item == 'odds':
                element = bets[i].odds
            elif item == 'potential returns label':
                element = bets[i].potential_returns_label
            elif item == 'potential returns value':
                element = bets[i].potential_returns_value

            actual_font_size = element.css_property_value('font-size')
            actual_color = element.css_property_value('color')
            actual_font = element.css_property_value('font-family')

            expected_font_size = test_data[item]['font size']
            expected_color = test_data[item]['color']
            expected_font = test_data[item]['font']

            if item == 'potential returns label' or item == 'potential returns value':
                expected_font_weight = test_data[item]['font weight']
                actual_font_weight = element.css_property_value('font-weight')
                self.assertEqual(expected_font_weight, actual_font_weight, msg=f'Expected My bets >> {tab_name} {item} '
                                                                   f'font weight is '
                                                                   f'{expected_font_weight} but Actual '
                                                                   f'{item} font weight is '
                                                                   f'{actual_font_weight}')

            self.assertEqual(expected_font_size, actual_font_size,
                             msg=f'Expected My bets >> {tab_name} {item} font size is {expected_font_size} but '
                                 f'Actual {item} '
                                 f'font size is {actual_font_size}')
            self.assertEqual(expected_color, actual_color, msg=f'Expected My bets >> {tab_name} {item}'                                                                                        
                                                                                        f' color is '
                                                                                        f'{expected_color} but Actual '
                                                                                        f'{item} color is '
                                                                                        f'{actual_color}')
            self.assertEqual(expected_font, actual_font,
                             msg=f'Expected My bets >> {tab_name} {item} font is {expected_font} but Actual '
                                 f'{item} font is {actual_font}')

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 3
        self.__class__.selection_ids = []

        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        fb_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=self.number_of_events)
        for fb_event in fb_events:
            match_result_market = next((market['market'] for market in fb_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            fb_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            fb_selection_id = list(fb_all_selection_ids.values())[0]
            self.selection_ids.append(fb_selection_id)

        if len(self.selection_ids) < 3:
            raise SiteServeException('Atleast 3 selections are not available in Football')

        self.__class__.table_tennis_selection_id = list(self.get_active_event_selections_for_category(
            category_id=59, additional_filters=cashout_filter).values())[0]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        # Covered in below step

    def test_004_verify_selection_name_of_bets_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify selection name of bets displayed in Open tab
        EXPECTED: Font size ,font colour should be as per figma
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab', item='selection')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab', item='market')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab', item='event')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab', item='odds')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab',
                                                     item='potential returns label')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_bet, tab_name='Open tab',
                                                     item='potential returns value')

    def test_005_verify_selection_names_of_bets_displayed_in_cashout_tab(self):
        """
        DESCRIPTION: Verify selection names of bets displayed in Cashout tab
        EXPECTED: Font size,font color should be as per figma
        EXPECTED: ![](index.php?/attachments/get/05d5fb2b-b82d-45a0-8c8b-0798b92ffc64)
        """
        self.site.open_my_bets_cashout()
        bet = list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_bet = [list(bet.items_as_ordered_dict.values())[0]]
        # cash_out_bet = [
        #     list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_elements_font_color_size(bets=list(cash_out_bet), tab_name='Cash Out tab', item='selection')
        self.verify_my_bets_elements_font_color_size(bets=list(cash_out_bet), tab_name='Cash Out tab', item='market')
        self.verify_my_bets_elements_font_color_size(bets=list(cash_out_bet), tab_name='Cash Out tab', item='event')
        self.verify_my_bets_elements_font_color_size(bets=list(cash_out_bet), tab_name='Cash Out tab', item='odds')

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

    def test_006_verify_selection_names_of_bets_displayed_in_settled_tab(self):
        """
        DESCRIPTION: Verify selection names of bets displayed in Settled tab
        EXPECTED: Font size,font color should be as per figma
        """
        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_elements_font_color_size(bets=list(settled_bet), tab_name='Settled tab', item='selection')
        self.verify_my_bets_elements_font_color_size(bets=list(settled_bet), tab_name='Settled tab', item='market')
        self.verify_my_bets_elements_font_color_size(bets=list(settled_bet), tab_name='Settled tab', item='event')
        self.verify_my_bets_elements_font_color_size(bets=list(settled_bet), tab_name='Settled tab', item='odds')

    def test_007_repeat_step_4_6__by_placing_bets_for_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat step 4-6  by placing bets for tier1 and tier2 Sports
        EXPECTED: Result should be same
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.table_tennis_selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.test_004_verify_selection_name_of_bets_displayed_in_open_tab()
        self.test_005_verify_selection_names_of_bets_displayed_in_cashout_tab()
        self.test_006_verify_selection_names_of_bets_displayed_in_settled_tab()

    def test_008_repeat_step_4_6_by_placing_multiple_bets_and_complex_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 by placing multiple bets and complex bets
        EXPECTED: Result should be same
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_bet = \
        list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        open_tab_double_bets = list(open_bet.items_as_ordered_dict.values())
        self.verify_my_bets_elements_font_color_size(bets=open_tab_double_bets, tab_name='Open tab', item='selection')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_double_bets, tab_name='Open tab', item='market')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_double_bets, tab_name='Open tab', item='event')
        self.verify_my_bets_elements_font_color_size(bets=open_tab_double_bets, tab_name='Open tab', item='odds')

        self.site.open_my_bets_cashout()
        cash_out_bet = \
        list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_tab_double_bets = list(cash_out_bet.items_as_ordered_dict.values())
        self.verify_my_bets_elements_font_color_size(bets=cash_out_tab_double_bets, tab_name='Cash Out tab',
                                                     item='selection')
        self.verify_my_bets_elements_font_color_size(bets=cash_out_tab_double_bets, tab_name='Cash Out tab',
                                                     item='market')
        self.verify_my_bets_elements_font_color_size(bets=cash_out_tab_double_bets, tab_name='Cash Out tab',
                                                     item='event')
        self.verify_my_bets_elements_font_color_size(bets=cash_out_tab_double_bets, tab_name='Cash Out tab',
                                                     item='odds')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')
        self.site.open_my_bets_settled_bets()

        settled_bet = \
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        settled_tab_double_bets = list(settled_bet.items_as_ordered_dict.values())
        self.verify_my_bets_elements_font_color_size(bets=settled_tab_double_bets, tab_name='Settled tab',
                                                     item='selection')
        self.verify_my_bets_elements_font_color_size(bets=settled_tab_double_bets, tab_name='Settled tab',
                                                     item='market')
        self.verify_my_bets_elements_font_color_size(bets=settled_tab_double_bets, tab_name='Settled tab',
                                                     item='event')
        self.verify_my_bets_elements_font_color_size(bets=settled_tab_double_bets, tab_name='Settled tab',
                                                     item='odds')

    def test_009_repeat_step_4_6_for_lotto_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 for lotto bets
        EXPECTED: Result should be same
        """
        # Need to verify for Lotto bets

    def test_010_repeat_step_4_6_for_pools(self):
        """
        DESCRIPTION: Repeat step 4-6 for pools
        EXPECTED: Result should be same
        """
        # Covered in C66111704 test
