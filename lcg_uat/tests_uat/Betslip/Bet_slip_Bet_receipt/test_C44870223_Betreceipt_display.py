import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choices
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.p3
@vtest
class Test_C44870223_Betreceipt_display(BaseBetSlipTest):
    """
    TR_ID: C44870223
    NAME: Betreceipt display
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_log_in_on_desktop_siteapp(self):
        """
        DESCRIPTION: Log in on desktop site/App
        EXPECTED: User is logged in
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_add_a_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add a selections to the Bet slip
        EXPECTED: The selections are added to the Bet slip
        """
        selection_ids = []
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True,
                                                     additional_filters=cashout_filter, in_play_event=False)
        self.__class__.event1 = choices(events, k=1)
        for event in self.event1:
            market = next((market['market'] for market in event['event']['children'] if
                           market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = market['children']
            self.__class__.outcomes_name = outcomes[0]['outcome'].get('name')
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.values())[0]
            selection_ids.append(selection_id)
            self.__class__.market_name = market.get('name')
            self.__class__.event_name = event['event']['name']
        self.open_betslip_with_selections(selection_ids=selection_ids)

    def test_003_enter_a_stake(self):
        """
        DESCRIPTION: Enter a stake
        EXPECTED: The stakes are displayed on the Bet slip
        """
        # This step is covered in test step 4

    def test_004_click_on_place_bet(self):
        """
        DESCRIPTION: Click on Place Bet
        EXPECTED: The bet is placed successfully and the Receipt is displayed
        """
        if self.device_type == 'mobile':
            self.__class__.user_balance = self.site.betslip.header.user_balance_amount
        else:
            self.__class__.user_balance = self.site.header.user_balance
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_005_check_that_bet_details_are_correctly_displayed(self):
        """
        DESCRIPTION: Check that bet details are correctly displayed
        EXPECTED: User should see the bellow details
        EXPECTED: *bet id
        EXPECTED: *selection name
        EXPECTED: *market name / event name
        EXPECTED: *Cash out available icon when available
        EXPECTED: *Check display of estimated returns' / 'potential returns' for that individual bet
        EXPECTED: * Check display of'total stake' / 'stake for this bet' for that individual bet
        EXPECTED: * Check header balance update after placing bet
        EXPECTED: * Check my bets and bet history.
        """
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = section_items.get(self.outcomes_name)
        # BetReceipt
        outcome_bet_receipt_selection_name = bet_info.name
        outcome_bet_receipt_market_name = bet_info.event_market_name
        outcome_bet_receipt_event_name = bet_info.event_name
        outcome_bet_receipt_est_returns = bet_info.estimate_returns
        outcome_bet_receipt_total_stake = bet_info.total_stake
        self.assertTrue(bet_info.bet_id, msg="Bet Id not found")
        self.assertEqual(self.outcomes_name, outcome_bet_receipt_selection_name, msg=f'selection placed "{self.outcomes_name}" does not match with bet receipt"{outcome_bet_receipt_selection_name}"')
        self.assertIn(self.market_name, outcome_bet_receipt_market_name, msg=f'Market placed "{self.market_name}" does not match with bet receipt"{outcome_bet_receipt_market_name}"')
        self.assertEqual(self.event_name, outcome_bet_receipt_event_name, msg=f'Event placed "{self.event_name}" does not match with bet receipt"{outcome_bet_receipt_event_name}"')
        self.assertTrue(self.site.bet_receipt.cash_out_label, msg=f'label "{vec.bet_history.CASHOUT_NOT_AVAILABLE}"')
        self.assertTrue(outcome_bet_receipt_est_returns, msg=f'"{vec.bet_history.CASHOUT_NOT_AVAILABLE}"')
        self.assertTrue(outcome_bet_receipt_total_stake, msg=f'"{vec.SB.TOTAL_STAKE}" not found')
        if self.device_type == 'mobile':
            new_user_balance = self.site.bet_receipt.user_header.user_balance
        else:
            new_user_balance = self.site.header.user_balance
        self.assertGreater(self.user_balance, new_user_balance, msg=f'Actual amount '
                                                                    f'"{new_user_balance}" does not match expected '
                                                                    f'"{self.user_balance}"')
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_cashout()
        bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=1)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'betleg was not displayed for bet: "{bet_name}"')

        # Stake and Returns
        self.assertEqual(single_bet.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg=f'Total Stake amount "{single_bet.stake.value}" is not equal to expected '
                             f'"{outcome_bet_receipt_total_stake}" for bet "{single_bet.name}"')

        self.assertEqual(single_bet.est_returns.stake_value, outcome_bet_receipt_est_returns,
                         msg=f'Estimated returns: "{single_bet.est_returns.stake_value}" '
                             f'does not match with required: "{outcome_bet_receipt_est_returns}"')
        for betleg_name, betleg in bet_legs.items():
            name = f'{self.outcomes_name}'
            self.assertIn(name, betleg_name, msg=f'"{name}" not found in "{betleg_name}"')
            self.assertEqual(betleg.market_name, self.market_name,
                             msg=f'"{betleg.market_name}" not same as "{self.market_name}"')
