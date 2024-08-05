import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C91378_Trader_modifies_the_Leg_Type_Each_Way(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C91378
    NAME: Trader modifies the Leg Type (Each Way)
    DESCRIPTION: This test case verifies offers displaying in Betslip when Leg Type was changed by Trader
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Leg Type (Each Way) is available for Racing selections (Each way terms are shown if isEachWayAvailable='true'):
    PRECONDITIONS: For verifying specific event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    max_bet = None
    bet_amount = 3.00
    prices = {0: '1/2', 1: '2/3'}
    suggested_max_bet = 0.25
    min_bet = 1.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event for HR and login
        EXPECTED: Event Created and user is logged In
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id_1 = list(selection_ids.values())[0]
        self.__class__.selection_id_2 = list(selection_ids.values())[1]
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selectionfrom_racing_event_to_betslip(self, num_of_selection=1):
        """
        DESCRIPTION: Add selection from Racing event to Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        if num_of_selection == 1:
            self.open_betslip_with_selections(selection_ids=self.selection_id_1)
        else:
            self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(
            self, each_way=False, num_of_selection=1):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit for added selection
        DESCRIPTION: * 'Each Way' checkbox is unchecked
        """
        if num_of_selection == 1:
            self.__class__.bet_amount = self.max_bet + 0.1
            self.place_single_bet(number_of_stakes=1, each_way=each_way)
        else:
            singles_section = self.get_betslip_sections().Singles

            stake = list(singles_section.values())[0]
            stake.each_way_checkbox.click()
            stake.amount_form.input.value = self.max_bet + 0.10

            stake = list(singles_section.values())[1]
            stake.amount_form.input.value = self.min_bet
            self.get_betslip_content().bet_now_button.click()

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')

    def test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self,
                                                                                                          win_only=False,
                                                                                                          each_way=True,
                                                                                                          number_of_selection=1):
        """
        DESCRIPTION: Trigger Leg Type and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Selection is expanded
        EXPECTED: *   The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to selection instead of '+'/'-' icon
        EXPECTED: *   'Each Way' checkbox is selected and highlighted in green
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  Selection is expanded
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *  'E/W' with a tick is displayed below the new stake
        EXPECTED: *  Values in 'Stake' and 'Est. Returns' fields are shown
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31453)
        EXPECTED: ![](index.php?/attachments/get/31454)
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)

        if win_only:
            self.bet_intercept.change_bet_to_each_way_or_win(account_id=account_id, bet_id=bet_id,
                                                             betslip_id=betslip_id, bet_amount=self.suggested_max_bet,
                                                             leg_type='W')
        else:
            self.bet_intercept.change_bet_to_each_way_or_win(account_id=account_id, bet_id=bet_id,
                                                             betslip_id=betslip_id, bet_amount=self.suggested_max_bet,
                                                             leg_type='E')

        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=30)
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

        self.__class__.section = self.get_betslip_sections().Singles
        stake_name, stake = list(self.section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        if each_way:
            each_way_text = self.section.overask_trader_offer.stake_content.each_way.name
            self.assertEqual(each_way_text, 'E/W',
                             msg=f'Actual Stake mark: "{each_way_text}" '
                                 f'is not as expected: "E/W"')
            each_way_tick = self.section.overask_trader_offer.stake_content.each_way.has_tick
            self.assertTrue(each_way_tick, msg='"E/W" mark is not displayed')

            stake = self.section.overask_trader_offer.stake_content.stake_value
            self.assertTrue(stake, msg='Stake value is not appearing')

            est_returns = self.get_betslip_content().total_estimate_returns
            self.assertTrue(est_returns, msg='estimated returns is not appearing')

        if win_only:
            self.assertEqual(self.section.overask_trader_offer.stake_content.win_only_sign_post, vec.betslip.WIN_ONLY,
                             msg=f'Actual signposting: {self.section.overask_trader_offer.stake_content.win_only_sign_post} is not same as '
                                 f'Expected signposting: {vec.betslip.WIN_ONLY}')
            est_returns_ui = self.get_betslip_content().total_estimate_returns
            if number_of_selection == 2:
                est_returns_stake_1 = self.calculate_estimated_returns(odds=[self.prices[0]],
                                                                       bet_amount=self.suggested_max_bet)
                est_returns_stake_2 = self.calculate_estimated_returns(odds=[self.prices[1]], bet_amount=self.min_bet)

                self.assertAlmostEqual((float(est_returns_stake_1) + float(est_returns_stake_2)), float(est_returns_ui),
                                       delta=0.04,
                                       msg=f'Actual estimated returns "{(float(est_returns_stake_1) + float(est_returns_stake_2))}" doesn\'t match expected '
                                           f'"{float(est_returns_ui)}" within "{0.04}" delta')
            else:
                self.verify_estimated_returns(est_returns=est_returns_ui, bet_amount=self.suggested_max_bet,
                                              odds=self.prices[0])

        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg="Cancel button is disabled")
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg=f'"{self.get_betslip_content().confirm_overask_offer_button.name}" button is disabled')

    def test_005_tap_on_accept__bet_number_of_accepted_bets_place_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet ([number of accepted bets])'/ 'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: * Tapping 'Accept & Bet ([number of accepted bets])' / 'Place bet' (From OX 99) button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed(timeout=15)
        self.site.bet_receipt.footer.click_done()

    def test_006_repeat_steps_1_4_with_enabled__each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-4 with enabled  'Each Way' checkbox
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: 'Please, consider our trader's alternative Offer', highlighted in green
        EXPECTED: *    The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   'Each Way' checkbox is unselected
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative'. 'Offer expires: X:XX' is shown and anchored to the Betslip header
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: ![](index.php?/attachments/get/36199)
        """
        self.test_001_add_selectionfrom_racing_event_to_betslip(num_of_selection=1)
        self.test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(
            each_way=True, num_of_selection=1)
        self.test_003_tap_bet_now_place_bet_from_ox_99_button()
        self.test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(
            win_only=True, each_way=False, number_of_selection=1)

    def test_007_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        """
        self.test_005_tap_on_accept__bet_number_of_accepted_bets_place_bet_from_ox_99_or_cancel_buttons()

    def test_008__add_few_selections_to_the_betslipand_for_few_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection_enable_each_way_for_one_selection(
            self):
        """
        DESCRIPTION: * Add few selections to the Betslip and for few of them enter stake value which will trigger Overask for the selection
        DESCRIPTION: * Enable 'Each Way' for one selection
        EXPECTED:
        """
        self.test_001_add_selectionfrom_racing_event_to_betslip(num_of_selection=2)
        self.test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(
            each_way=True, num_of_selection=2)

    def test_009_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/ 'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        self.test_003_tap_bet_now_place_bet_from_ox_99_button()

    def test_010_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Leg Type and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: * Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel'  buttons with text: 'Please, consider our trader's alternative Offer' highlighted in yellow
        EXPECTED: * The new stake is shown to the user on the Betslip (in green)
        EXPECTED: * 'Each Way' checkbox is updated according to Trader's changes
        EXPECTED: * The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative'. 'Offer expires: X:XX' is shown and anchored to the Betslip header
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        """
        self.test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(
            win_only=True, each_way=False, number_of_selection=2)

    def test_011_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step #5
        """
        self.test_005_tap_on_accept__bet_number_of_accepted_bets_place_bet_from_ox_99_or_cancel_buttons()
