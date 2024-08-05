import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@vtest
class Test_C66132229_Verify_Ga_Tracking_for_betdetails_expand_and_collapse_state_in_opencashoutsettled_tabs(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C66132229
    NAME: Verify Ga Tracking for betdetails expand and collapse state in open,cashout,settled tabs
    DESCRIPTION: This test case Verify Ga Tracking for betdetails expand and collapse state in open,cashout,settled tabs
    PRECONDITIONS: Bets should be available in all the tabs
    """
    keep_browser_open = True

    def get_expected_data_layer_reponce(self, action=None, tab_name=None):
        data_layer_responce = {
            "event": "Event.Tracking",
            "component.categoryevent": "betslip",
            "component.LabelEvent": "bet details",
            "component.ActionEvent": action,
            "component.PositionEvent": tab_name,
            "component.LocationEvent": "mybets",
            "component.EventDetails": "Sports",
            "component.URLClicked": "not applicable",
            "component.contentPosition": 1
        }
        return data_layer_responce

    def verify_GA_tracking_for_bet_details_expand_and_collapse(self,  bet=None, tab_name=None):
        self.assertTrue(bet.is_expanded(expected_result=True),
                        msg=f'Bet is not expanded by default under {tab_name}')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after clicking on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                                                  object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='expand', tab_name=tab_name)
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

        bet.bet_details.chevron_arrow.click()
        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                        msg=f'Bet Details section is not collapsed after clicking on Bet Details chevron under {tab_name}')

        actual_data_layer_response = self.get_data_layer_specific_object(object_key='event',
                                                                                                  object_value='Event.Tracking')
        excepted_data_layer_responce = self.get_expected_data_layer_reponce(action='collapse', tab_name=tab_name)
        self.compare_json_response(excepted_data_layer_responce, actual_data_layer_response)

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        number_of_events = 1
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=cashout_filter,
                                                    number_of_events=number_of_events)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_load_oxygen_application_lads_and_coral(self):
        """
        DESCRIPTION: Load oxygen application lads and coral
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
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_place_bets_on_pools_and_lotto(self):
        """
        DESCRIPTION: Place bets on pools and lotto
        EXPECTED: Bets should be placed successfully on pools and lotto
        """
        # Covered in C66111693 and C66111694 tests

    def test_005_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        # Covered in below step

    def test_006_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        # Covered in below step

    def test_007_check_new_section_with_bet_detail_area_available_with__chevron(self):
        """
        DESCRIPTION: Check new section with bet detail area available with  Chevron
        EXPECTED: Bet detail area is available with expand and collapse
        """
        # Covered in below step

    def test_008_click_on_expand_on_bet_details_form_open_tab_for_any_of_the_bet_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on expand on bet details form open tab for any of the bet and check ga tracking
        EXPECTED: Bet details should be expanded
        EXPECTED: **Check the below tags in expand state for bet details:**
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betslip',
        EXPECTED: component.LabelEvent: 'bet details',
        EXPECTED: component.ActionEvent:{expand/collapse},
        EXPECTED: component.PositionEvent: {tab name} or MyBets in the EDP  // Build Your Racecard // EZnav ex: Open tab // Cash Out tab // Settled tab,
        EXPECTED: component.LocationEvent: {bet location} ex: mybets // MyBets in the EDP  // Build Your Racecard // EZnav,
        EXPECTED: component.EventDetails: {bet category type} ex: Sports // Lottos // Pools,
        EXPECTED: component.URLClicked: '{url/not applicable}' ,
        EXPECTED: component.contentPosition: {position of the bet} ex:1,2,3etc,
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_GA_tracking_for_bet_details_expand_and_collapse(bet=open_tab_bet, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_GA_tracking_for_bet_details_expand_and_collapse(bet=cash_out_bet, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')
        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
                           None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_GA_tracking_for_bet_details_expand_and_collapse(bet=settled_bet, tab_name='Settled tab')

    def test_009_click_on_collapse_on_the_bet_details_and_check_the_ga_tracking(self):
        """
        DESCRIPTION: Click on collapse on the bet details and check the Ga tracking
        EXPECTED: Check when the bet details gets collapsed
        EXPECTED: **Check the below tags in collapse state for bet details:**
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betslip',
        EXPECTED: component.LabelEvent: 'bet details',
        EXPECTED: component.ActionEvent:{expand/collapse},
        EXPECTED: component.PositionEvent: {tab name} or MyBets in the EDP  // Build Your Racecard // EZnav ex: Open tab // Cash Out tab // Settled tab,
        EXPECTED: component.LocationEvent: {bet location} ex: mybets // MyBets in the EDP  // Build Your Racecard // EZnav,
        EXPECTED: component.EventDetails: {bet category type} ex: Sports // Lottos // Pools,
        EXPECTED: component.URLClicked: '{url/not applicable}' ,
        EXPECTED: component.contentPosition: {position of the bet} ex:1,2,3etc,
        EXPECTED: }]
        EXPECTED: });
        """
        # Covered in above step

    def test_010_repeat_the_above_step_for_pools_and_lotto_in_open_tab(self):
        """
        DESCRIPTION: Repeat the above step for pools and lotto in open tab
        EXPECTED: 
        """
        # Covered in C66111693 and C66111694 tests

    def test_011_repeat_the_above_steps_for_cash_out_tab(self):
        """
        DESCRIPTION: Repeat the above steps for cash out tab
        EXPECTED: 
        """
        # Covered in above step

    def test_012_repeat_the_above_steps_for_settled_tab(self):
        """
        DESCRIPTION: Repeat the above steps for Settled tab
        EXPECTED: 
        """
        # Covered in above step
