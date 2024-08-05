import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant freebets
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@vtest
class Test_C14742507_Verify_Quick_Bet_receipt_after_bet_placement_using_FreeBet_bonuses(BaseSportTest, BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C14742507
    NAME: Verify Quick Bet receipt after bet placement using FreeBet bonuses
    DESCRIPTION: This test case verifies Quick Bet receipt after bet placement using FreeBet bonuses
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. User should have Free Bets available on their account
    PRECONDITIONS: 4. Make bet placement for selection using only free bet bonuses
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    """
    keep_browser_open = True
    free_bet_value = 1.03

    def test_000_preconditions(self):
        """
        DESCRIPTION: Pre-conditions
        DESCRIPTION: Load the app
        DESCRIPTION: Make sure the user is logged into their account
        DESCRIPTION: User should have Free Bets available on their account
        DESCRIPTION: Make bet placement for selection using only free bet bonuses
        DESCRIPTION: Make sure Bet is placed successfully
        """
        event = self.ob_config.add_autotest_premier_league_football_event(price_boost=True,
                                                                          market_price_boost=True,
                                                                          cashout=True)
        self.__class__.eventID = event.event_id
        self.__class__.selection_id = event.selection_ids[vec.sb.DRAW.title()]
        expected_market = normalize_name(
            self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.free_bet_value, level='selection',
                                     id=self.selection_id)
        self.site.login(username=self.username, async_close_dialogs=False)
        self.__class__.free_bet_name = self.get_freebet_name(value=self.free_bet_value,
                                                             redemption_name=self.get_freebet_redemption_name(
                                                                 level='selection'))
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.quick_bet.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.free_bet_name)
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet receipt is not displayed')

    def test_001_verify_bet_receipt_after_bet_placement_using_only_for_example_500_freebet_bonuses(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using only, for example, £5.00 FreeBet bonuses
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: £5.00 ('Total Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        EXPECTED: *[From OX100]*
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: FB £5.00 ('Stake' for Coral)
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        """
        self.__class__.potential_returns_label = vec.betslip.ESTIMATED_RESULTS if self.brand == 'bma' else vec.betslip.POTENTIAL_RESULTS
        quick_bet = self.site.quick_bet_panel
        self.assertEqual(quick_bet.header.title.upper(), vec.quickbet.BET_RECEIPT_TITLE.upper(),
                         msg=f'Actual title "{quick_bet.header.title}" '
                             f'Expected Title "{vec.quickbet.BET_RECEIPT_TITLE}')
        self.assertTrue(quick_bet.header.has_close_button(), msg='Close Button "X" not present')
        self.assertEqual(quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Quick stake not working correctly')
        self.assertTrue(quick_bet.bet_receipt.header.receipt_datetime, msg='Bet Receipt Date/Time not displayed')
        self.assertEqual(quick_bet.bet_receipt.selection_type.upper(),
                         vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE.upper(),
                         msg=f'Actual Bet Type "{quick_bet.bet_receipt.selection_type}" '
                             f'Expected Bet Type "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertTrue(quick_bet.bet_receipt.odds_value is not None, msg='Selection price is not displayed')
        self.assertTrue(quick_bet.bet_receipt.bet_id_label is not None, msg='Bet ID label is not displayed')
        self.assertTrue(quick_bet.bet_receipt.bet_id_value is not None, msg='Bet ID Value is not displayed')
        self.assertTrue(quick_bet.bet_receipt.selection_name is not None, msg='Selection Name is not displayed')
        self.assertTrue(quick_bet.bet_receipt.market_name is not None, msg='Market Name is not displayed')
        self.assertTrue(quick_bet.bet_receipt.event_name is not None, msg='Event Name is not displayed')
        price_boost_label = quick_bet.bet_receipt.has_price_boost_label()
        self.assertTrue(price_boost_label, msg='"Smart Boost" is not displayed')
        cashout_label = quick_bet.bet_receipt.has_cashout_label()
        self.assertTrue(cashout_label, msg='"Cashout" label is not displayed')
        self.assertEqual(quick_bet.bet_receipt.stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg='Stake label on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.free_bet_stake, msg='Stake Value on the bet receipt is not displayed')
        self.assertEqual(quick_bet.bet_receipt.potential_return_label, self.potential_returns_label,
                         msg='Stake label on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.potential_return_value,
                        msg='Stake Value on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.has_free_bet_icon(),
                        msg='"Freebet" icon not displayed on Quickbet receipt')

    def test_002_verify_bet_receipt_after_bet_placement_using_for_example_500_freebet_bonuses_plus_500_cash_stake(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using, for example, £5.00 FreeBet bonuses + £5.00 Cash stake
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: £10.00 ('Total Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        EXPECTED: *[From OX100]*
        EXPECTED: The following info is displayed:
        EXPECTED: - 'Bet receipt' header with 'X'
        EXPECTED: - 'Bet Placed Successfully' and time when bet was placed in the format '11/07.2019, 16:25'
        EXPECTED: - bet type name e.g. Single
        EXPECTED: - price of selection bet was struck at e.g. '@ 8/11'
        EXPECTED: - bet id (Coral): receipt no (Ladbrokes)
        EXPECTED: - selection name
        EXPECTED: - market name / event name
        EXPECTED: - promo icons (if available)
        EXPECTED: - Cashout icon (if available)
        EXPECTED: Stake for this bet: FB £5.00 + £5.00 ('Stake' for Coral)
        EXPECTED: Potential Returns: £xx.xx ('Est. Returns' for Coral)
        """
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.free_bet_value, level='selection',
                                     id=self.selection_id)
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)
        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.quick_bet.amount_form.input.value = self.bet_amount
        self.quick_bet.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.free_bet_name)
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet receipt is not displayed')
        quick_bet = self.site.quick_bet_panel
        self.assertEqual(quick_bet.header.title.upper(), vec.quickbet.BET_RECEIPT_TITLE.upper(),
                         msg=f'Actual title "{quick_bet.header.title}" '
                             f'Expected Title "{vec.quickbet.BET_RECEIPT_TITLE}')
        self.assertTrue(quick_bet.header.has_close_button(), msg='Close Button "X" not present')
        self.assertEqual(quick_bet.bet_receipt.header.bet_placed_text, vec.Betslip.SUCCESS_BET,
                         msg='Quick stake not working correctly')
        self.assertTrue(quick_bet.bet_receipt.header.receipt_datetime, msg='Bet Receipt Date/Time not displayed')
        self.assertEqual(quick_bet.bet_receipt.selection_type.upper(),
                         vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE.upper(),
                         msg=f'Actual Bet Type "{quick_bet.bet_receipt.selection_type}" '
                             f'Expected Bet Type "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertTrue(quick_bet.bet_receipt.odds_value is not None, msg='Selection price is not displayed')
        self.assertTrue(quick_bet.bet_receipt.bet_id_label is not None, msg='Bet ID label is not displayed')
        self.assertTrue(quick_bet.bet_receipt.bet_id_value is not None, msg='Bet ID Value is not displayed')
        self.assertTrue(quick_bet.bet_receipt.selection_name is not None, msg='Selection Name is not displayed')
        self.assertTrue(quick_bet.bet_receipt.market_name is not None, msg='Market Name is not displayed')
        self.assertTrue(quick_bet.bet_receipt.event_name is not None, msg='Event Name is not displayed')
        price_boost_label = quick_bet.bet_receipt.has_price_boost_label()
        self.assertTrue(price_boost_label, msg='"Smart Boost" is not displayed')
        cashout_label = quick_bet.bet_receipt.has_cashout_label()
        self.assertTrue(cashout_label, msg='"Cashout" label is not displayed')
        self.assertEqual(quick_bet.bet_receipt.stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg='Stake label on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.stake_value, msg='Stake Value on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.free_bet_stake, msg='Stake Value on the bet receipt is not displayed')
        self.assertEqual(quick_bet.bet_receipt.potential_return_label, self.potential_returns_label,
                         msg='Stake label on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.potential_return_value,
                        msg='Stake Value on the bet receipt is not displayed')
        self.assertTrue(quick_bet.bet_receipt.has_free_bet_icon(),
                        msg='"Freebet" icon not displayed on Quickbet receipt')
