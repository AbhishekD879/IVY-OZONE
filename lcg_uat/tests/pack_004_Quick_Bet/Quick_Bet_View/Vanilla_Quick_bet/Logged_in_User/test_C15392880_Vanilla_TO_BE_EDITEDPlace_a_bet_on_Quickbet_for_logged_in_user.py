import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C15392880_Vanilla_TO_BE_EDITEDPlace_a_bet_on_Quickbet_for_logged_in_user(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C15392880
    NAME: [Vanilla] [TO BE EDITED]Place a bet on Quickbet for logged in user
    DESCRIPTION: Verify that logged in user is able to place a bet from QuickBet
    PRECONDITIONS: *Quickbet should be enabled in CMS
    PRECONDITIONS: *User should be logged in
    """
    keep_browser_open = True
    outcomes = None
    selection_name, selection_name_2 = None, None
    bet_amount = 0.05

    def verify_bet_receipt_and_close_dialog(self, event_name, market_name, selection_name, odd_value):
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        actual_date_time = bet_receipt.header.receipt_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        self.assertTrue(bet_receipt.bet_id, msg='Bet Receipt number is not shown')
        self.assertEqual(bet_receipt.name, selection_name,
                         msg=f'Actual Selection Name "{bet_receipt.name}" does not match '
                             f'expected "{selection_name}"')
        event_name = event_name.replace(',', '')
        self.assertEqual(bet_receipt.event_name, event_name,
                         msg=f'Actual Event Name "{bet_receipt.event_name}" does not match '
                             f'expected "{event_name}"')
        self.assertEqual(bet_receipt.event_market, market_name,
                         msg=f'Actual market name: "{bet_receipt.event_market}" '
                             f'is not as expected: "{market_name}"')
        actual_total_stake = bet_receipt.total_stake
        expected_total_stake = f'{self.bet_amount :.2f}'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual total stake value: "{actual_total_stake}" doesn\'t match '
                             f'with expected: "{expected_total_stake}"')
        actual_estimate_returns = bet_receipt.estimate_returns
        self.verify_estimated_returns(est_returns=actual_estimate_returns, odds=odd_value, bet_amount=self.bet_amount)

        self.site.close_all_dialogs(async_close=False)
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: *Quickbet should be enabled in CMS
        PRECONDITIONS: *Make sure that that user is logged out
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is not logged off')

        event_1 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]

        match_result_market_1 = next((market['market'] for market in event_1['event']['children'] if
                                      market.get('market').get('templateMarketName') == 'Match Betting'), None)
        self.__class__.eventID_1 = event_1['event']['id']
        self.__class__.event_name_1 = normalize_name(event_1['event']['name'])
        self.__class__.market_name_1 = 'Match Betting'
        outcomes_resp_1 = match_result_market_1['children']
        all_selection_ids_1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_resp_1 if
                               'Unnamed' not in i['outcome']['name']}
        selection_ids_1 = dict(list(all_selection_ids_1.items())[:2])
        self.__class__.selection_name_1 = [key for key in selection_ids_1.keys() if 'Unnamed' not in key][:2]

        event_2 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        match_result_market_2 = next((market['market'] for market in event_2['event']['children'] if
                                      market.get('market').get('templateMarketName') == 'Match Betting'), None)
        self.__class__.eventID_2 = event_2['event']['id']
        self.__class__.event_name_2 = normalize_name(event_2['event']['name'])
        self.__class__.market_name_2 = 'Match Betting'
        outcomes_resp_2 = match_result_market_2['children']
        all_selection_ids_1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_resp_2 if
                               'Unnamed' not in i['outcome']['name']}
        selection_ids_2 = dict(list(all_selection_ids_1.items())[:2])
        self.__class__.selection_name_2 = [key for key in selection_ids_2.keys() if 'Unnamed' not in key][:1]

    def test_001_open_vanilla(self):
        """
        DESCRIPTION: Open Vanilla
        EXPECTED: The application should be successfully loaded
        """
        self.site.login()
        self.site.wait_content_state('homepage')

    def test_002_go_to_any_sport_eg_football___select_ant_odd(self):
        """
        DESCRIPTION: Go to any Sport (e.g Football)--> Select ant odd
        EXPECTED: QuickBet should appear in the bottom of the screen
        EXPECTED: "Place Bet" button should be disabled by default
        EXPECTED: ![](index.php?/attachments/get/31345)
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name_1[0], market_name=self.market_name_1)
        quick_bet = wait_for_result(lambda: self.site.quick_bet_panel, timeout=60)
        self.__class__.odd_value_1 = self.site.quick_bet_panel.selection.content.odds
        self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='The button "Login & Place Bet" is active')

    def test_003_specify_any_quickstake_eg_5_(self):
        """
        DESCRIPTION: Specify any QuickStake (e.g. 5 )
        EXPECTED: "Place Bet" button should become enabled
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='The button "Login & Place Bet" is not active')

    def test_004_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on "Place Bet" button
        EXPECTED: Bet Receipt with all betting details should appear
        EXPECTED: Bet Receipt should contain "Reuse selection" and "Done" button
        EXPECTED: ![](index.php?/attachments/get/31346)
        """
        self.site.quick_bet_panel.place_bet.click()
        self.verify_bet_receipt_and_close_dialog(event_name=self.event_name_1, market_name=self.market_name_1,
                                                 selection_name=str(self.selection_name_1[0]), odd_value=self.odd_value_1)

    def test_005_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on "Reuse selection button"
        EXPECTED: The quick bet should be opened with the same bet but with empty stacked field and disabled "Place Bet" button
        """
        # "Reuse selection" and "Done" button functionality is no longer applicable.

    def test_006_specify_any_another_stake_eg_2_(self):
        """
        DESCRIPTION: Specify any Another Stake (e.g. 2 )
        EXPECTED: "Place Bet" button should become enabled
        """
        self.navigate_to_edp(event_id=self.eventID_2)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name_2[0], market_name=self.market_name_2)
        quick_bet = wait_for_result(lambda: self.site.quick_bet_panel, timeout=60)
        self.assertTrue(quick_bet, msg="Quick bet is not displayed")
        self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='The button "Login & Place Bet" is active')
        self.__class__.odd_value_2 = self.site.quick_bet_panel.selection.content.odds

        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='The button "Place Bet" is not active')
        self.site.quick_bet_panel.place_bet.click()

    def test_007_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on "Place Bet" button
        EXPECTED: Bet Receipt with all betting details should appear
        EXPECTED: Bet Receipt should contain "Reuse selection" and "Done" button
        """
        self.verify_bet_receipt_and_close_dialog(event_name=self.event_name_2, market_name=self.market_name_2,
                                                 selection_name=self.selection_name_2[0], odd_value=self.odd_value_2)

    def test_008_click_on_done_button(self):
        """
        DESCRIPTION: Click on "Done" button
        EXPECTED: Quick bet should disappear
        """
        # Covered into step 7

    def test_009_open_mybets(self):
        """
        DESCRIPTION: Open "MyBets"
        EXPECTED: Bets from step#4 and step#7 should be present.
        """
        self.device.refresh_page()
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list
        self.assertTrue(bets.items_as_ordered_dict, msg='No bets found on openbets page')
        single_bet_1 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_1)
        self.assertTrue(single_bet_1, msg=f'Bet not found for "{self.event_name_1}"')

        single_bet_2 = bets.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_2)
        self.assertTrue(single_bet_2, msg=f'Bet not found for "{self.event_name_2}"')
