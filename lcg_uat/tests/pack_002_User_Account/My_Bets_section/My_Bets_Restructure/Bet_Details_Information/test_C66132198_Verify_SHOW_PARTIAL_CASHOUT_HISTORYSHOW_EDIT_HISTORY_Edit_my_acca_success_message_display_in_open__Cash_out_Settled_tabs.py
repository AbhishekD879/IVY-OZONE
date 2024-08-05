import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_details_information
@vtest
@pytest.mark.timeout(2000)
class Test_C66132198_Verify_SHOW_PARTIAL_CASHOUT_HISTORYSHOW_EDIT_HISTORY_Edit_my_acca_success_message_display_in_open__Cash_out_Settled_tabs(BaseBetSlipTest):
    """
    TR_ID: C66132198
    NAME: Verify SHOW PARTIAL CASHOUT HISTORY,SHOW EDIT HISTORY, Edit my acca success message display in open / Cash out, Settled tabs
    DESCRIPTION: This testcase Verifies SHOW PARTIAL CASHOUT HISTORY,SHOW EDIT HISTORY, Edit my acca success message display in open / Cash out, Settled tabs
    PRECONDITIONS:
    """
    keep_browser_open = True
    bet_amount = 1
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User have placed a 4 fold accumulator bet.
        """
        edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
        self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     additional_filters=cashout_filter,
                                                     number_of_events=self.number_of_events)
        for event in events:
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.values())[0]
            self.selection_ids.append(selection_id)

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
        # Covered in above step

    def test_003_add_multiple_selections_from_different_events_to_betslip_and_place_acca4_bet(self):
        """
        DESCRIPTION: Add Multiple selections from different events to betslip and place ACCA(4) bet
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.ACC4, sections.keys(),
                      msg=f'No "{vec.betslip.ACC4}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.ACC4)
        self.check_bet_receipt_is_displayed()

    def test_004_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        self.site.open_my_bets_open_bets()

    def test_005_click_on_edit_my_acca_and_remove_any_one_selection_and_click_on_save_button(self):
        """
        DESCRIPTION: Click on EDIT MY ACCA and remove any one selection and click on SAVE Button
        EXPECTED: selections get removed and stake and potential returns updated accordingly
        """
        bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(bet, msg='Bet is not available under Open tab')

        potential_returns_before_edit = bet.est_returns.stake_value

        self.assertTrue(bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.assertTrue(bet.edit_my_acca_button.is_enabled(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not enabled')
        bet.edit_my_acca_button.click()
        wait_for_result(
            lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[
                        0].edit_my_acca_button.name == vec.ema.CANCEL.upper(),
            name='"CANCEL" text to be displayed', timeout=15)

        selections = list(bet.items_as_ordered_dict.values())
        selection = selections[0]
        selection.edit_my_acca_remove_icon.click()
        wait_for_result(lambda: bet.confirm_button.is_enabled(), expected_result=True, name='Save button enabled', timeout=15)
        self.assertTrue(bet.confirm_button.is_enabled(), msg='"Confirm" button is not clickable')
        bet.confirm_button.click()
        wait_for_result(lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[
                                    0].cash_out_successful_message == vec.ema.EDIT_SUCCESS.caption,
                        name='"Acca Edited Successfully" message to be displayed', timeout=20)

        bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        potential_returns_after_edit = bet.est_returns.stake_value
        self.assertNotEquals(potential_returns_before_edit, potential_returns_after_edit)

        self.assertFalse(bet.bet_details.is_expanded(expected_result=False),
                         msg=f'Bet Details section is not collapsed by default under Open tab')
        bet.bet_details.chevron_arrow.click()
        self.assertTrue(bet.bet_details.is_expanded(expected_result=True),
                        msg=f'Bet Details section is not expanded after click on Bet Details chevron under Open tab')
        bet_details_section_potential_returns = bet.bet_details.bet_potential_returns.split('£')[1]
        self.assertEqual(potential_returns_after_edit, bet_details_section_potential_returns)

    def test_006_verify_edit_my_acca_success_message(self):
        """
        DESCRIPTION: Verify Edit My Acca success message
        EXPECTED: Acca edited successfully message is displayed just above the bet details
        """
        # Covered in above step

    def test_007_refresh_the_page_now_and_verify_show_edit_history_link_displayed_in_open_tab(self):
        """
        DESCRIPTION: Refresh the page now and verify SHOW EDIT HISTORY link displayed in open tab
        EXPECTED: SHOW EDIT HISTORY hyperlink is displayed just above the bet details
        """
        self.device.refresh_page()
        self.site.open_my_bets_open_bets()
        self.__class__.bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(self.bet, msg='Bet is not available under Open tab')
        show_edit_history_link_y_value = self.bet.show_edit_history_button.location['y']
        bet_details_y_value = self.bet.bet_details.location['y']
        self.assertTrue(bet_details_y_value > show_edit_history_link_y_value, msg='SHOW EDIT HISTORY link is not above the Bet Details section')

    def test_008_perform_partial_cashout_for_any_of_the_bet_in_open_tab(self):
        """
        DESCRIPTION: Perform Partial cashout for any of the bet in open tab
        EXPECTED: User should be able to perform partial cashout in open tab and "Partial Cash Out Successful" message should be displayed
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message, timeout=30),
                        msg=f'Message "{expected_message}" is not shown')

    def test_009_refresh_the_page_and_verify_show_partial_cashout_history_hyperlink_displayed_in_open_tab(self):
        """
        DESCRIPTION: Refresh the page and verify SHOW PARTIAL CASHOUT HISTORY hyperlink displayed in open tab
        EXPECTED: SHOW PARTIAL CASHOUT HISTORY hyperlink is displayed just above the bet details
        """
        self.device.refresh_page()
        self.site.open_my_bets_open_bets()

        bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(bet, msg='Bet is not available under Open tab')
        show_partial_cash_out_history_y_value = bet.partial_cash_out_history.location['y']
        show_edit_history_link_y_value = bet.show_edit_history_button.location['y']
        bet_details_y_value = bet.bet_details.location['y']
        self.assertTrue(bet_details_y_value > show_edit_history_link_y_value > show_partial_cash_out_history_y_value,
                        msg='SHOW PARTIAL CASH OUT HISTORY link is not above the Bet Details section and SHOW EDIT HISTORY link')