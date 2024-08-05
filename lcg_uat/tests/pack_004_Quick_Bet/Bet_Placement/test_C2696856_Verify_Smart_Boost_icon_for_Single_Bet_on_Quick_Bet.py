import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@vtest
class Test_C2696856_Verify_Smart_Boost_icon_for_Single_Bet_on_Quick_Bet(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2696856
    NAME: Verify Smart Boost icon for Single Bet on Quick Bet
    DESCRIPTION: This test case verifies that the Smart Boost icon is displayed within Quick Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [Promo / Signposting: QuickBet for SmartBoost]
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-36230
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Smart Boost promo is available for event on Market lvl.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: preconditions
        """
        football_event1 = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True, cashout=False)
        self.__class__.event1_eventID = football_event1.event_id
        event_1 = football_event1.ss_response
        self.__class__.selection_name1 = football_event1.team1
        football_event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event2_eventID = football_event2.event_id
        self.__class__.selection_name2 = football_event2.team1
        football_event3 = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True)
        self.__class__.event3_eventID = football_event3.event_id
        self.__class__.selection_name3 = football_event3.team1

        market_name = next((market.get('market').get('name') for market in event_1['event']['children']
                            if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        self._logger.info(f'*** Using event "{self.eventID}" with market "{market_name}"')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_with_available_smart_boost_promo_on_market_level_to_the_quick_bet(self):
        """
        DESCRIPTION: Add selection with available Smart Boost promo on Market level to the Quick Bet
        EXPECTED: Quick Bet has shown up and Selection is successfully added
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_edp(event_id=self.event1_eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name1)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_002_verify_the_smart_boost_icon_for_the_bet_added_to_quick_bet(self):
        """
        DESCRIPTION: Verify the 'Smart Boost' icon for the bet added to Quick Bet
        EXPECTED: Smart Boost icon is displayed below the bet
        EXPECTED: ![](index.php?/attachments/get/53285793)
        EXPECTED: ![](index.php?/attachments/get/53285798)
        """
        quick_bet = self.site.quick_bet_panel
        self.assertTrue(quick_bet.selection.content.price_boost_label, msg='"Smart Boost" icon is not displayed')

    def test_003__enter_value_in_stake_field_and_place_a_bet_verify_smart_boost_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Enter value in 'Stake' field and place a bet
        DESCRIPTION: * Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * 'Smart Boost' icon is displayed below market name/event name section
        EXPECTED: ![](index.php?/attachments/get/53285795)
        EXPECTED: ![](index.php?/attachments/get/53285797)
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet.place_bet.click()
        self.assertEqual(quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Bet placement not successful')
        price_boost_label = quick_bet.bet_receipt.has_price_boost_label()
        self.assertTrue(price_boost_label, msg='"Smart Boost" is not displayed')

    def test_004_add_selection_with_no_promo_available_to_quick_bet_and_check_the_icon(self):
        """
        DESCRIPTION: Add selection with no promo available to Quick Bet and check the icon
        EXPECTED: No icon is displayed for bet without promo available
        """
        self.navigate_to_edp(event_id=self.event2_eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name2)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        quick_bet = self.site.quick_bet_panel
        self.assertFalse(quick_bet.selection.content.price_boost_label, msg='"Smart Boost" icon is displayed')

    def test_005__enter_value_in_stake_field_and_place_a_bet_verify_smart_boost_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Enter value in 'Stake' field and place a bet
        DESCRIPTION: * Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * 'Smart Boost' icon is NOT displayed
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet.place_bet.click()
        self.assertEqual(quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Bet placement not successful')
        price_boost_label = quick_bet.bet_receipt.has_price_boost_label()
        self.assertFalse(price_boost_label, msg='"Smart Boost" is displayed')

    def test_006_add_selection_with_smart_boost_and_cashout_promo_available_to_the_quick_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection with Smart Boost and Cashout promo available to the Quick Bet and place a bet
        EXPECTED: * Smart Boost and Cashout icons are displayed for the bet one by one in one line
        EXPECTED: * 'Cashout' icon is placed first, 'Smart Boost' is second one
        EXPECTED: ![](index.php?/attachments/get/53285794)
        EXPECTED: ![](index.php?/attachments/get/53285796)
        """
        self.navigate_to_edp(event_id=self.event3_eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name3)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        quick_bet = self.site.quick_bet_panel
        self.assertTrue(quick_bet.selection.content.price_boost_label, msg='"Smart Boost" icon is not displayed')
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet.place_bet.click()
        self.assertEqual(quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Bet placement not successful')
        price_boost_label = quick_bet.bet_receipt.has_price_boost_label()
        self.assertTrue(price_boost_label, msg='"Smart Boost" is not displayed')
        cashout_label = quick_bet.bet_receipt.has_cashout_label()
        self.assertTrue(cashout_label, msg='"Cashout" label is not displayed')
        x_location_cashout = quick_bet.bet_receipt.cashout_label.location['x']
        x_location_price_boost = quick_bet.bet_receipt.price_boost_label.location['x']
        self.assertGreater(x_location_price_boost, x_location_cashout, msg='"Cashout" icon is not placed before '
                                                                           '"Smart Boost" icon')
