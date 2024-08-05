import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import perform_offset_mouse_click


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C82410_Trader_modifies_the_PriceOdds_for_Multiples(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C82410
    NAME: Trader modifies the Price/Odds for Multiples
    DESCRIPTION: This test case verifies additional information displaying for any multiple bet that has been  price/odds modified  by the trader.
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-16714 Overask Improvement - Show leg offers for multiples
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    PRECONDITIONS: 4. Price/Odds is displayed for Multiples if **payout.potential**>=2 from 'readBet' response
    """
    keep_browser_open = True
    bet_amount = 4
    username = None
    new_price_1 = '1/7'
    new_price_2 = '3/17'
    new_price_3 = '13/100'
    new_overask_prices = [new_price_1, new_price_2, new_price_3]
    expected_overask_messages = []
    account_id = None
    betslip_id = None
    selection_ids = []
    prices = {0: '1/12'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events
        PRECONDITIONS: User is logged in to application
        """
        for i in range(0, 3):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=3, max_mult_bet=3,
                                                              lp_prices=self.prices)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self._logger.info(f'*** Created event with id: {self.eventID}, selection ids: {selection_ids.values()}')
            self.__class__.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_few_selections_to_betslip(self):
        """
        DESCRIPTION: Add few selections to betslip
        EXPECTED: Multiples are available in betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_stake_value_which_is_higher_than_maximum_limit_for_multiples(self):
        """
        DESCRIPTION: Enter stake value which is higher than maximum limit for Multiples
        """
        self.place_multiple_bet(number_of_stakes=1, sp=True)
        self.__class__.expected_betslip_counter_value = 0

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' button
        EXPECTED: CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer
        EXPECTED: Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: Background is disabled and not clickable
        """
        self.__class__.account_id, self.__class__.bet_id, self.__class__.betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)

        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

        self.get_betslip_content().overask.overask_title.click()
        perform_offset_mouse_click()
        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_004_trigger_price_odds_modification_by_trader_and_check_message_displaying_in_betslip(self):
        """
        EXPECTED: CMS configurable 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: 'Cancel' and 'Place a bet' buttons enabled
        """
        self.bet_intercept.offer_multiple_prices(account_id=self.account_id, bet_id=self.bet_id,
                                                 betslip_id=self.betslip_id,
                                                 price_1=self.new_price_1, price_2=self.new_price_2,
                                                 price_3=self.new_price_3, max_bet=self.bet_amount)

        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_005_verify_new_price_displaying(self):
        """
        DESCRIPTION: Verify additional information displaying for multiples
        EXPECTED: New price = new modified price by Trader highlighted in green/yellow
        """
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.multiples_section = sections.Multiples
        stakes = self.multiples_section.overask_trader_offer.items_as_ordered_dict
        self.assertTrue(stakes, msg='Cannot find any stakes for Trade Offer')
        for stake_name, stake in stakes.items():
            self.assertEqual(stake.stake_odds.value_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

    def test_006_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        """
        est_returns = self.multiples_section.overask_trader_offer.stake_content.est_returns
        self.assertTrue(est_returns.value, msg='"Est. returns" value is not shown on Trader Offer')
        text = est_returns.value
        self.assertNotEquals(text[1:], 'N/A', msg='The "Est. returns" value is equal "N/A" but should not')

    def test_007_tap_confirm_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: The bet is placed as per normal process
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_008_repeat_step_1_6(self):
        """
        DESCRIPTION: Repeat step #1-6
        """
        self.test_001_add_few_selections_to_betslip()
        self.test_002_enter_stake_value_which_is_higher_than_maximum_limit_for_multiples()
        self.test_003_tap_bet_now_button()
        self.test_004_trigger_price_odds_modification_by_trader_and_check_message_displaying_in_betslip()
        self.test_005_verify_new_price_displaying()
        self.test_006_verify_new_est_returns_value()

    def test_009_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: * Bet is not placed
        EXPECTED: * Betslip is cleared and closed
        """
        cancel_btn = self.get_betslip_content().cancel_button
        cancel_btn.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        if self.device_type != 'desktop':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=3),
                             msg='Betslip widget was not closed')
        else:
            actual_message = self.get_betslip_content().no_selections_title
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Actual title message "{actual_message}" '
                                 f'is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
