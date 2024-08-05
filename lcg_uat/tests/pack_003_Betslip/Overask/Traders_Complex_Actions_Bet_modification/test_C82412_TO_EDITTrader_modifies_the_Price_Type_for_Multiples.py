import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import perform_offset_mouse_click


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Cannot trigger offer in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.overask
@vtest
class Test_C82412_TO_EDITTrader_modifies_the_Price_Type_for_Multiples(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C82412
    NAME: [TO-EDIT]Trader modifies the Price Type for Multiples
    DESCRIPTION: [TO EDIT] step 6 is outdated
    DESCRIPTION: This test case verifies additional information displaying for any multiple bet that has been modified (price type changed) by the trader.
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Price Type can be changed for Racing selections
    PRECONDITIONS: 4. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True
    new_price_1 = '1/7'
    new_price_2 = '3/17'
    new_price_3 = '13/100'
    prices = {0: '1/12'}
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events
        PRECONDITIONS: User is logged in to application
        """
        for i in range(0, 3):
            self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(self.eventID)
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)

    def test_001_add_few_selectionsfrom_different_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add few selections from different Racing events to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_multiples(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for Multiples
        """
        self.__class__.bet_amount = self.max_bet + 1
        self.place_multiple_bet(number_of_stakes=1, sp=True)

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown: 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' over 'Bet Now' button
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
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

    def test_004_enable_checkbox_present_next_to_selection_with_offer(self):
        """
        DESCRIPTION: Enable checkbox present next to Selection with Offer
        EXPECTED: 'Confirm' button becomes enable automatically
        EXPECTED: **From OX 99**
        EXPECTED: not available
        """
        # Out of scope

    def test_005_trigger_price_type_modification_by_trader_and_verify_message_displaying(self):
        """
        DESCRIPTION: Trigger Price Type modification by Trader and verify message displaying
        EXPECTED: *   Info message is displayed over 'Confirm' and 'Cancel' buttons: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_ids[0])
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price_1, price_2=self.new_price_2,
                                                 price_3=self.new_price_3, max_bet=self.bet_amount)

        self.site.wait_content_state_changed()
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

    def test_006_verify_new_price_type_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify new Price Type displaying in Betslip
        EXPECTED: * Selection name + @ symbol + Price + Offer + New Price
        EXPECTED: Event Name
        EXPECTED: where Price=old price ( e.g. 'SP')
        EXPECTED: New price = new modified price by Trader highlighted in green/yellow (From OX 99)
        EXPECTED: * Stake remains the same in the stake box
        EXPECTED: **NOTE** currently when price type is changed from SP to LP together with Price Odds, additional info is NOT returned from Openbet and NOT displayed on FE
        """
        sections = self.get_betslip_sections(multiples=True)
        self.__class__.multiples_section = sections.Multiples
        stakes = self.multiples_section.overask_trader_offer.items_as_ordered_dict
        self.assertTrue(stakes, msg='Cannot find any stakes for Trade Offer')
        for stake_name, stake in stakes.items():
            self.assertEqual(stake.stake_odds.value_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

    def test_007_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        EXPECTED: * The 'Est. return' value is highlighted in green/yellow (From OX 99)
        """
        est_returns = self.multiples_section.overask_trader_offer.stake_content.est_returns
        self.assertTrue(est_returns.value, msg='"Est. returns" value is not shown on Trader Offer')
        text = est_returns.value
        self.assertNotEquals(text[1:], 'N/A', msg='The "Est. returns" value is equal "N/A" but should not')

    def test_008_tap_confirm_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: The bet is placed as per normal process
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_009_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps #1-7
        """
        self.test_001_add_few_selectionsfrom_different_racing_events_to_the_betslip()
        self.test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_multiples()
        self.test_003_tap_bet_now_place_bet_from_ox_99_button()
        self.test_005_trigger_price_type_modification_by_trader_and_verify_message_displaying()
        self.test_006_verify_new_price_type_displaying_in_betslip()
        self.test_007_verify_new_est_returns_value()

    def test_010_tap_cancel_button_then_cancel_offer_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button/ then 'Cancel offer' (From OX 99) button
        EXPECTED: * Bet is not placed
        EXPECTED: * Selections are cleaned from betslip
        EXPECTED: * User stays on the previously opened page
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
