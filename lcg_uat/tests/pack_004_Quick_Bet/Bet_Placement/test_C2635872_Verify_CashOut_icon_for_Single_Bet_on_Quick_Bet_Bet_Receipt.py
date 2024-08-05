import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C2635872_Verify_CashOut_icon_for_Single_Bet_on_Quick_Bet_Bet_Receipt(BaseRacing, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2635872
    NAME: Verify CashOut icon for Single Bet on Quick Bet Bet Receipt
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Bet Receipt within Quick Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-35709 CLONE FOR QUICKBET - Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-35709
    DESCRIPTION: [BMA-36231 Promo / Signposting: Quick Ber for CashOut] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-36231
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for bet on all levels (category/type/event/market)
    """
    keep_browser_open = True
    prices = {0: '1/4'}

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
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=True, lp_prices=self.prices)
            self.__class__.eventID = event.event_id
        else:
            each_way_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            events = self.get_active_events_for_category(category_id=self.category_id,
                                                         additional_filters=each_way_filter,
                                                         all_available_events=True)
            event = self.get_event_win_e_w_market(events)
            self.__class__.eventID = event['event']['id']
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_001_add_selection_with_available_cashout_to_the_quick_bet(self):
        """
        DESCRIPTION: Add selection with available CashOut to the Quick Bet
        EXPECTED: * Selection is added to the Quick Bet
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        sections_nw = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        section_nw_name, section_nw = list(sections_nw.items())[0]
        if section_nw_name:
            outcomes = section_nw.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_nw_name)
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

    def test_003_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below market name/event name section
        EXPECTED: ![](index.php?/attachments/get/53285820)
        EXPECTED: ![](index.php?/attachments/get/53285822)
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        for section_name, section in bet_receipt_sections.items():
            receipts = section.items_as_ordered_dict
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                if receipt_type == 'ReceiptSingles':
                    if receipt.has_cash_out_label():
                        self.assertTrue(receipt.has_cash_out_label(), msg=f'"Cashout" label is not displayed')
