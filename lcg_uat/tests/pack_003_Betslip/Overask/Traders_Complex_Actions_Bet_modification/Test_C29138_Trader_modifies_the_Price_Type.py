import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C29138_Trader_modifies_the_Price_Type(BaseBetSlipTest):
    """
    TR_ID: C29138
    NAME: Trader modifies the Price Type
    DESCRIPTION:
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Price Type can be changed for Racing selections
    """
    keep_browser_open = True
    max_bet = None
    max_mult_bet = 0.3
    prices = {0: '1/20', 1: '2/20'}
    new_price = 'SP'
    min_bet = 0.03

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices,
                                                          max_bet=self.max_bet,
                                                          max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id_1 = list(selection_ids.values())[0]
        self.__class__.selection_id_2 = list(selection_ids.values())[1]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_selection_from_racing_events_to_the_betslip(self, num_of_selection=1):
        """
        DESCRIPTION: Add selection from Racing events to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        if num_of_selection == 1:
            self.open_betslip_with_selections(selection_ids=self.selection_id_1)
        else:
            self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self, num_of_selection=1):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        if num_of_selection == 1:
            self.__class__.bet_amount = self.max_bet + 0.10
            self.place_single_bet(number_of_stakes=1)
        else:
            singles_section = self.get_betslip_sections().Singles

            stake = list(singles_section.values())[0]
            stake.amount_form.input.value = self.max_bet + 0.10

            stake = list(singles_section.values())[1]
            stake.amount_form.input.value = self.min_bet
            self.get_betslip_content().bet_now_button.click()

        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        # Covered in step-2

    def test_004_trigger_price_type_modification_by_trader_and_verify_new_price_type_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Price Type modification by Trader and verify new Price Type displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Confirm' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Selection is expanded
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to selection instead of '+'/'-' icon
        EXPECTED: *   The new Price Type is shown to the user on the Betslip (in green)
        EXPECTED: *   The Estimate returns are updated according to new Price Type (also highlighted in green)
        EXPECTED: *   "You're accepting this Trade Offer" message on the grey background is shown below the selection
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price Type is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Price Type
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31458)
        EXPECTED: ![](index.php?/attachments/get/31459)
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_price_type(account_id=account_id, bet_id=bet_id,
                                             betslip_id=betslip_id, bet_amount=self.bet_amount,
                                             price_type='S')
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask panel is not closed')
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

        sections = self.get_betslip_sections().Singles
        odd_value = sections.overask_trader_offer.stake_content.odd_value.value
        self.__class__.odd_value = odd_value.strip(' x')
        self.assertEqual(self.odd_value, self.new_price,
                         msg=f'Actual price :{self.odd_value} is not same as'
                             f'Expected price :{self.new_price}')
        self.assertEqual(sections.overask_trader_offer.stake_content.odd_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for stake is not highlighted in yellow')

        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.bet_amount, odds=self.new_price)

        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Place bet button is not displayed')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_tap_confirm_button(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: The bet is placed as per normal process
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed(timeout=10)

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(
            self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        """
        self.test_001_add_selection_from_racing_events_to_the_betslip(num_of_selection=2)
        self.test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(num_of_selection=2)
        self.test_004_trigger_price_type_modification_by_trader_and_verify_new_price_type_displaying_in_betslip(
            num_of_selection=2)
        self.test_005_tap_confirm_button()

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps 3-5
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        No_of_bets = len(self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict['Single'].items)
        self.assertEqual(No_of_bets, 2, msg='Bet is not placed for all added selection')
