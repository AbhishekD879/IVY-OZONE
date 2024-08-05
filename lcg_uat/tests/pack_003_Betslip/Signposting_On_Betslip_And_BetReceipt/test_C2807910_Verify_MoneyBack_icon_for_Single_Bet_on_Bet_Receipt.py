import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod # can not create event on Market level with MoneyBack promo icon
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2807910_Verify_MoneyBack_icon_for_Single_Bet_on_Bet_Receipt(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2807910
    NAME: Verify MoneyBack icon for Single Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the MoneyBack icon is displayed on the Bet Receipt within BetSlip/Quickbet (for mobile)
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-36252]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * MoneyBack promo is available for event on Market level
    """
    keep_browser_open = True

    def add_selection_to_bet_slip(self, event_id, team):
        self.navigate_to_edp(event_id=event_id)
        selection_name = team.upper() if self.brand == 'ladbrokes' else team
        bet_button = self.get_selection_bet_button(selection_name=selection_name, market_name=None)
        self.device.driver.implicitly_wait(1)
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
        self.site.open_betslip()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events and login
        """
        event = self.ob_config.add_autotest_premier_league_football_event(market_money_back=True)
        self.__class__.expected_event_name = event.team1 + ' v ' + event.team2
        self.__class__.team1 = event.team1
        self.__class__.eventID = event.event_id
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID2 = event2.event_id
        self.__class__.expected_event_name2 = event2.team1 + ' v ' + event.team2
        self.__class__.team2 = event2.team2

        self.site.login()

    def test_001_add_selection_with_available_moneyback_promo_on_market_level_to_betslipquickbet_for_mobile(self):
        """
        DESCRIPTION: Add selection with available MoneyBack promo on Market level to betslip/Quickbet (for mobile)
        EXPECTED: Selection is added to the BetSlip
        """
        self.add_selection_to_bet_slip(event_id=self.eventID, team=self.team1)

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_moneyback_icon_on_the_bet_receipt(self, expected_result=True):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Bet Receipt
        EXPECTED: * 'MoneyBack' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        if expected_result:
            self.assertTrue(first_section.has_promo_icon(expected_result=True),
                            msg='MoneyBack icon is not present on betreceipt')
        else:
            self.assertFalse(first_section.has_promo_icon(expected_result=False),
                             msg='MoneyBack icon is present on betreceipt')

    def test_004_add_selection_without_moneyback_promo_available_to_betslipquickbet_for_mobile_and_place_bet(self):
        """
        DESCRIPTION: Add selection without MoneyBack promo available to betslip/Quickbet (for mobile) and place bet
        EXPECTED: There is no 'MoneyBack' icon displayed on bet slip/Quickbet (for mobile).
        """
        self.site.bet_receipt.close_button.click()
        self.add_selection_to_bet_slip(event_id=self.eventID2, team=self.team2)
        self.test_002_enter_value_in_stake_field_and_place_a_bet()
        self.test_003_verify_moneyback_icon_on_the_bet_receipt(expected_result=False)
