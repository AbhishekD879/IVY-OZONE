import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2635878_Need_to_be_updatedVerify_CashOut_icon_for_Single_Bet_on_BetSlip_and_Bet_Receipt(BaseRacing, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2635878
    NAME: [Need to be updated]Verify CashOut icon for Single Bet on BetSlip and Bet Receipt
    DESCRIPTION: [Need to be updated step 1]
    DESCRIPTION: [10:17 AM] Amit Bhardwaj
    DESCRIPTION: Hi mate, I think we took out Cashout icons
    DESCRIPTION: ?[10:17 AM] Amit Bhardwaj
    DESCRIPTION: As we offer Cashout on everything and all customers are aware about it
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Betslip and Bet Receipt within BetSlip for Single Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33418 Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33418
    DESCRIPTION: [BMA-33416 / Promo / Signposting : Cashout : Bet Slip] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-33416
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for bet on all levels (category/type/event/market)
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/7'}

    def get_event_win_e_w_market(self, events):
        for event in events:
            if next((market.get('market') for market in event['event']['children']
                     if market.get('market', {}).get('isEachWayAvailable') == 'true' and market.get('market', {}).get('templateMarketName') == 'Win or Each Way'), None):
                return event

        raise SiteServeException('No events with "Win or Each Way" market and "isEachWayAvailable"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * User is logged in and has positive balance
        PRECONDITIONS: * CashOut should be available for bet
        """
        if tests.settings.backend_env != 'prod':
            event1 = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=True, lp_prices=self.prices,
                                                        each_way=True)
            self.__class__.eventID1 = event1.event_id

            event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=True, lp_prices=self.prices,)
            self.__class__.event_id2 = event2.event_id

            event3 = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=False, lp_prices=self.prices, )
            self.__class__.event_id3 = event3.event_id
        else:
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            event = self.get_active_events_for_category(category_id=self.category_id,
                                                        additional_filters=cashout_filter,
                                                        all_available_events=True)
            event1 = self.get_event_win_e_w_market(event)
            self.__class__.eventID1 = event1['event']['id']

            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event2 = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=cashout_filter)[0]
            self.__class__.event_id2 = event2.get('event').get('id')

            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.NOT_EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.NOT_EQUALS, 'Y')
            event3 = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=cashout_filter)[0]
            self.__class__.event_id3 = event3.get('event').get('id')

        self.site.login()
        self.navigate_to_edp(event_id=self.event_id2, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_001_add_selection_with_available_cashout_to_the_betslipquickbet_for_mobile(self):
        """
        DESCRIPTION: Add selection with available CashOut to the BetSlip/Quickbet (for mobile)
        EXPECTED: * Selection is added to the BetSlip/Quickbet (for mobile)
        EXPECTED: * CashOut icon is displayed between event name and Stake section
        EXPECTED: * CashOut icon stays displayed at all times even when selection details are minimized/maximized
        """
        current_market_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        if current_market_tab != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if vec.racing.RACING_EDP_MARKET_TABS.win_or_ew in market_tabs.keys():
                market_tabs[vec.racing.RACING_EDP_MARKET_TABS.win_or_ew].click()
                self.site.wait_content_state_changed(timeout=5)

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.open_betslip()

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_cashout_icon_on_the_bet_receipt(self, expected_result=True):
        """
        DESCRIPTION: Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Market name/Event name section
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        for section_name, section in bet_receipt_sections.items():
            receipts = section.items_as_ordered_dict
            for receipt_name, receipt in receipts.items():
                if expected_result:
                    self.assertTrue(receipt.has_cash_out_label(expected_result=True),
                                    msg=f'"Cashout" label is not displayed')
                else:
                    self.assertFalse(receipt.has_cash_out_label(expected_result=False),
                                     msg=f'"Cashout" label is displayed')

    def test_004__place_bet_on_horse_racing_selection_that_has_both_cash_out_and_eachway_odds_available_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Place bet on Horse Racing selection that has both cash out and Each/Way Odds available
        DESCRIPTION: * Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Each/Way Odds
        """
        self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.test_001_add_selection_with_available_cashout_to_the_betslipquickbet_for_mobile()
        self.place_single_bet(each_way=True)
        self.check_bet_receipt_is_displayed()
        self.test_003_verify_cashout_icon_on_the_bet_receipt(True)

    def test_005_repeat_steps_1_4_with_multiple_selections_with_cashout_disabled_at_eventselection_level(self):
        """
        DESCRIPTION: Repeat steps 1-4 with multiple selections with CashOut disabled at event/selection level
        EXPECTED: * Cashout icon is not displayed on Betslip/Quickbet (for mobile)
        EXPECTED: * Cashout icon is not displayed on Bet Receipt
        """
        self.navigate_to_edp(event_id=self.event_id3, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.test_001_add_selection_with_available_cashout_to_the_betslipquickbet_for_mobile()
        self.test_002_enter_value_in_stake_field_and_place_a_bet()
        self.test_003_verify_cashout_icon_on_the_bet_receipt(expected_result=False)
