import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2637329_Verify_CashOut_icon_for_Multiple_Bet_on_Bet_Receipt(BaseUserAccountTest, BaseCashOutTest):
    """
    TR_ID: C2637329
    NAME: Verify CashOut icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Bet Receipt for Multiple Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33418 Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33418
    DESCRIPTION: [BMA-33416 / Promo / Signposting : Cashout : Bet Slip] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-33416
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for all selections on all levels (category/type/event/market)
    """
    keep_browser_open = True
    number_of_events = 2
    co_selection_ids = []
    no_co_selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Create or retrieve the events with cashout available
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = [i['outcome']['id'] for i in outcomes]
                selection_id, selection_id1 = list(all_selection_ids)[0], list(all_selection_ids)[1]
                self.co_selection_ids.append(selection_id)

            no_cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                              'N'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                                  OPERATORS.EQUALS, 'N')
            no_cashout_events = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id,
                additional_filters=no_cashout_filter,
                number_of_events=self.number_of_events)

            for event in no_cashout_events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = [i['outcome']['id'] for i in outcomes]
                selection_id, selection_id1 = list(all_selection_ids)[0], list(all_selection_ids)[1]
                self.no_co_selection_ids.append(selection_id)
        else:
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.__class__.co_selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
            no_co_event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events,cashout=False)
            self.__class__.no_co_selection_ids = [list(event.selection_ids.values())[0] for event in no_co_event_params]
        self.site.login()
        self.__class__.expected_betslip_counter_value = 0

    def test_001_add_multiple_selection_with_available_cashout_to_the_betslip(self):
        """
        DESCRIPTION: Add multiple selection with available CashOut to the BetSlip
        EXPECTED: * Selection is added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        EXPECTED: * CashOut icon is displayed between event name and Stake section for each selection in the Singles section
        EXPECTED: * CashOut icon stays displayed at all times even when selection details are minimized/maximized
        EXPECTED: * CashOut icon is displayed under the Bet Type for each Bet type in the Multiples section
        """
        self.open_betslip_with_selections(selection_ids=self.co_selection_ids)

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple bet is displayed
        """
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=1)
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')

    def test_003_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Market name/Event name section (or below each/way odds if available)
        EXPECTED: * CashOut icon is displayed ONLY ONCE, below the last selection
        """
        self.assertTrue(self.site.bet_receipt.has_cashout_label(), msg='"Cashout" label not displayed')

    def test_004_repeat_steps_1_3_with_multiple_selections_with_cashout_disabled_at_eventselection_level(self):
        """
        DESCRIPTION: Repeat steps 1-3 with multiple selections with CashOut disabled at event/selection level
        EXPECTED: * Cashout icon is not displayed on Betslip
        EXPECTED: * Cashout icon is not displayed on Bet Receipt
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.no_co_selection_ids)
        self.test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet()
        self.assertFalse(self.site.bet_receipt.has_cashout_label(), msg='"Cashout" label not displayed')

