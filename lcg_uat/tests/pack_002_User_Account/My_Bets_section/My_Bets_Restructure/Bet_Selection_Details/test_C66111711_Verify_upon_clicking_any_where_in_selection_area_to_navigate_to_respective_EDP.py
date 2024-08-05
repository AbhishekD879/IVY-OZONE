import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@vtest
class Test_C66111711_Verify_upon_clicking_any_where_in_selection_area_to_navigate_to_respective_EDP(BaseBetSlipTest):
    """
    TR_ID: C66111711
    NAME: Verify upon clicking any where in selection area to navigate to respective EDP
    DESCRIPTION: This testcase verifies upon clicking any where in selection area to navigate to respective EDP
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def verify_navigation_upon_clicking_any_where_in_selection_area(self, bet=[], tab_name=None):
        bet[0].selection.click()
        wait_for_result(lambda: self.event_id in self.device.get_current_url(), timeout=15,
                        name=f"{self.event_id} event id displayed in current url {self.device.get_current_url()}",
                        expected_result=True)

        event_url = self.device.get_current_url()
        self.assertIn(self.event_id, event_url,
                      msg=f'Not navaigted to {self.event_id} event deatils page upon clicking any where in selection area under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place bet
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        fb_event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=1)[0]
        self.__class__.event_id = fb_event['event']['id']
        outcomes = next(((market['market']['children']) for market in fb_event['event']['children'] if
                         market['market'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(selection_ids.values())[0]

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
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        self.site.open_my_bets_open_bets()

    def test_004_verify_clicking_anywhere_in_the_selection_area_fo_the_bets_showing_in_open_tab(self):
        """
        DESCRIPTION: Verify clicking anywhere in the selection area fo the bets showing in open tab
        EXPECTED: Should navigate to respective EDP
        """
        open_tab_bet = [list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_navigation_upon_clicking_any_where_in_selection_area(bet=open_tab_bet, tab_name='Open tab')

    def test_005_repeat_step_4_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat step 4 in cashout tab
        EXPECTED: Result should be same
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')
        self.site.open_my_bets_cashout()
        bet = list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_bet = [list(bet.items_as_ordered_dict.values())[0]]
        # cash_out_bet = [
        #     list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_navigation_upon_clicking_any_where_in_selection_area(bet=cash_out_bet, tab_name='Cash Out tab')

        self.site.open_my_bets_cashout()
        bet = list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_bet = [list(bet.items_as_ordered_dict.values())[0]]
        # cash_out_bet = [
        #     list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

    def test_006_repeat_step_4_in_settled_tab(self):
        """
        DESCRIPTION: Repeat step 4 in Settled tab
        EXPECTED: Result should be same
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')
        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_navigation_upon_clicking_any_where_in_selection_area(bet=settled_bet, tab_name='Settled tab')
