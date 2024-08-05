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
class Test_C66132033_Verify_Cash_Out_Successful__Partial_Cash_Out_Successful_message_display_under_open__Cash_out_tabs(BaseBetSlipTest):
    """
    TR_ID: C66132033
    NAME: Verify Cash Out Successful / Partial Cash Out Successful message display under open / Cash out tabs
    DESCRIPTION: This test case is to verify Cash Out Successful / Partial Cash Out Successful message display under open / Cash out tabs after performing CO actions
    PRECONDITIONS: Cash out available events data should be there
    """
    keep_browser_open = True
    bet_amount = 1

    def verify_cash_out_and_partial_cash_out_messages(self, bet=None, tab_name=None):
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.wait_for_cashout_slider()
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.cashout_button.click()

        actual_partial_cash_out_success_message = bet.cash_out_successful_message
        expected_partial_cash_out_success_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertEqual(actual_partial_cash_out_success_message, expected_partial_cash_out_success_message,
                         msg=f'Partial Cash Out Success message "{actual_partial_cash_out_success_message}" is not the same as expected: "{expected_partial_cash_out_success_message}" under {tab_name}')

        cash_out_button_y_value = bet.buttons_panel.full_cashout_button.location['y']
        partial_cash_out_message_y_value = bet.cash_out_successful_icon.location['y']
        bet_details_y_value = bet.bet_details.location['y']
        self.assertTrue(bet_details_y_value > partial_cash_out_message_y_value > cash_out_button_y_value,
                        msg=f'Partial Cash Out Successful message is not in between Cashout button and Bet Detail section under {tab_name}')

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.cash_out_successful_message is not None, msg=f'Cash Out is not successful under {tab_name}')

        actual_full_cash_out_success_message = bet.cash_out_successful_message
        expected_full_cash_out_success_message = vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertEqual(actual_partial_cash_out_success_message, expected_partial_cash_out_success_message,
                         msg=f'Full Cash Out Success message "{actual_full_cash_out_success_message}" is not the same as expected: "{expected_full_cash_out_success_message}" under {tab_name}')

        full_cash_out_message_y_value = bet.cash_out_successful_icon.location['y']
        bet_details_y_value = bet.bet_details.location['y']
        self.assertTrue(bet_details_y_value > full_cash_out_message_y_value,
                        msg=f'Cash Out Successful message is not above the Bet Detail section under {tab_name}')

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

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should launch succesfully
        """
        self.site.login()

    def test_002_login_to_the_application_with_valid_credentaials_and_go_to_any_slp_from_sports_ribbon__a_z_menu(self):
        """
        DESCRIPTION: Login to the application with valid credentaials and Go to any SLP from sports ribbon / A-Z menu
        EXPECTED: User should be able to login and should be navigate to SLP
        """
        # Covered in above step

    def test_003_place_single_and_multiple_bets_then_navigate_to_my_bets_and_verify(self):
        """
        DESCRIPTION: Place single and multiple bets then navigate to my bets and verify
        EXPECTED: User should be able to place single and multiple bets and Open tab will be selected by default post navigation to MY Bets
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_verify_bets_under_open(self):
        """
        DESCRIPTION: Verify bets under Open
        EXPECTED: Recently placed bets should be displayed under open along with cashout button
        EXPECTED: Note: Cashout CTA button won't show if event doesnt have cashout availability
        """
        # Covered in below step

    def test_005_perform_cashout_partial_cashout_and_then_verify_the_successful_message(self):
        """
        DESCRIPTION: Perform cashout/ Partial cashout and then verify the successful message
        EXPECTED: User should be able to perform cashout and partial cashout under open by displaying message as "Cash Out Successful" / "Partial Cash Out Successful"
        """
        # Covered in below step

    def test_006_verify_the_location_of_cash_out_successful__partial_cash_out_successful_messages(self):
        """
        DESCRIPTION: Verify the location of Cash Out Successful / Partial Cash Out Successful messages
        EXPECTED: "Partial Cash Out Successful" message should be displayed above Bet details and below Cashout CTA button after performing partial cashout
        EXPECTED: "Cash Out Successful" message should be displayed above Bet details after performing Cashout
        EXPECTED: Note: message should be centre aligned
        EXPECTED: ![](index.php?/attachments/get/431e6d8e-d455-4f03-929c-2630850a025a)
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(open_tab_bet, msg='Bet is not available under Open tab')
        self.verify_cash_out_and_partial_cash_out_messages(bet=open_tab_bet, tab_name='Open tab')

    def test_007_repeat_step_3_to_step_6_under_cashout_and_verify(self):
        """
        DESCRIPTION: Repeat step 3 to step 6 under cashout and verify
        EXPECTED: Result should be same as above
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_cash_out_and_partial_cash_out_messages(bet=cash_out_bet, tab_name='Cash Out tab')

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
        self.verify_cash_out_and_partial_cash_out_messages(bet=open_tab_bet, tab_name='Open tab')

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')
        self.verify_cash_out_and_partial_cash_out_messages(bet=cash_out_bet, tab_name='Cash Out tab')