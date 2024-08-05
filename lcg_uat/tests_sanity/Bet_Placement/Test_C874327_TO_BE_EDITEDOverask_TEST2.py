import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.slow
@pytest.mark.overask
@pytest.mark.sanity
@pytest.mark.desktop
# @pytest.mark.prod #cant create events in PROD
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C874327_TO_BE_EDITEDOverask_TEST2(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C874327
    NAME: [TO BE EDITED]Overask [TEST2]
    DESCRIPTION: This test case should be edited according to the latest changes including Vanilla
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - Accepting/rejecting/offering a bet by a trader for a user with enabled overask functionality
    DESCRIPTION: - Maximum Stake functionality for a user with disabled overask
    DESCRIPTION: AUTOTEST [C9690088] [C9690089] [C9690090] [C9690091] [C9690086] [C9690081]
    PRECONDITIONS: How to disable/enable Overask functionality for User or Event Type https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: - User has an account with enabled overask
    PRECONDITIONS: - User has an account with disabled overask
    PRECONDITIONS: - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    """
    keep_browser_open = True
    max_bet = bet_amount = 3.55
    stake_part1 = price_part1 = 1.50
    stake_part2 = price_part2 = 0.50
    prices = {0: '1/12'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        self.__class__.username = tests.settings.betplacement_user
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.eventID, selection_ids, self.__class__.event_name = event_params.event_id, event_params.selection_ids, event_params.ss_response['event']['name']
        self.__class__.selection_id = list(selection_ids.values())[0]

    def test_001_log_in_with_account_with_enabled_overask(self):
        """
        DESCRIPTION: Log in with account with enabled overask
        EXPECTED: User is logged in
        """
        self.site.login(username=self.username)

    def test_002_add_selections_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip > Open Betslip
        EXPECTED: Added selection(s) are available within the Betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_003_enter_any_stake_amount_that_exceeds_maximum_allowed_bet_limit__tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter any Stake amount that exceeds maximum allowed bet limit > Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: - Overask is triggered
        EXPECTED: - 'Stake', 'Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
        EXPECTED: - "Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute." message is displayed on yellow background above the Betslip footer
        EXPECTED: - Loading spinner is shown on 'Bet Now' button
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_in_ti_accept_bet(self):
        """
        DESCRIPTION: In TI: Accept bet
        EXPECTED: Bet is accepted
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

    def test_005_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - Balance is reduced accordingly
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        EXPECTED: * Bet is placed successfully with the original amount
        EXPECTED: * Bet Receipt is displayed for a user
        EXPECTED: * Balance is reduced accordingly
        EXPECTED: * Bet is listed in 'Bet History' and 'My Account' pages
        """
        self.check_bet_receipt_is_displayed()
        expected_user_balance = float(self.user_balance) - float(self.bet_amount)
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        stake = self.site.bet_receipt.footer.total_stake
        self.assertEqual(str(stake).strip().replace(".00", ""), str(self.bet_amount),
                         msg=f'Actual stake "{stake}" is not same as '
                             + f'Expected stake "{self.bet_amount}"')
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)

    def test_006_tap_donego_bettingfrom_ox_99(self):
        """
        DESCRIPTION: Tap 'Done'/'Go Betting'(From OX 99)
        EXPECTED: Betslip is closed
        """
        # covered in step step 5
        self.navigate_to_page('homepage')

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        """
        self.test_002_add_selections_to_the_betslip__open_betslip()
        self.test_003_enter_any_stake_amount_that_exceeds_maximum_allowed_bet_limit__tap_bet_nowplace_bet_from_ox_99_button()

    def test_008_in_ti_decline_bet(self):
        """
        DESCRIPTION: In TI: Decline bet
        EXPECTED: Bet is declined
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
            username=self.username, event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        expected_user_balance = float(self.user_balance)
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.site.wait_content_state_changed(timeout=15)

    def test_009_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Bet is not placed and 'One or more of your bets have been declined' message is shown above 'Continue' button
        EXPECTED: - Balance is not reduced
        EXPECTED: - All selections are shown expanded
        EXPECTED: - 'Stake' field, 'Clear Betslip' buttons remain disabled and greyed out
        EXPECTED: - 'Continue' button is available and enabled
        EXPECTED: **From OX 99**
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_010_tap_continuego_bettingfrom_ox_99(self):
        """
        DESCRIPTION: Tap 'Continue'/'Go Betting'(From OX 99)
        EXPECTED: Betslip is closed
        """
        self.site.bet_receipt.footer.click_done()
        self.navigate_to_page('homepage')

    def test_011_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        """
        self.test_002_add_selections_to_the_betslip__open_betslip()
        self.test_003_enter_any_stake_amount_that_exceeds_maximum_allowed_bet_limit__tap_bet_nowplace_bet_from_ox_99_button()

    def test_012_in_ti_offer_max_stakeleg_type_for_racesoddsprice_type_for_racessplitlink_splitted_parts(self):
        """
        DESCRIPTION: In TI: Offer Max Stake/Leg Type (for Races)/Odds/Price Type (for Races)/Split/Link splitted parts
        EXPECTED: Max Stake/Leg Type (for Races)/Odds/Price Type (for Races)/Split/Link splitted parts are offered
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
            username=self.username, event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                     bet_id=bet_id, betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2, linked=True)
        self.__class__.overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)

        self.assertTrue(self.overask_trader_message, msg=f'Overask trader message has not appeared')
        is_selection_splitted = wait_for_result(lambda: len(self.get_betslip_sections().Singles) == 2,
                                                timeout=5,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')

    def test_013_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - All selections are shown expanded
        EXPECTED: - Modified Max Stake/Leg Type (for Races)/Odds/Price Type (for Races) are displayed in green
        EXPECTED: - 'Est. Returns' value is updated accordingly and displayed in green
        EXPECTED: - Enabled pre-ticked checkbox with a green icon is shown next to selection with an offer instead of '+'/'-' icon
        EXPECTED: - The linked bet parts are linked with 'link' symbol
        EXPECTED: - 'Bin' button is disabled
        EXPECTED: - 'Accept & Bet (# of accepting selections)' button is enabled
        EXPECTED: - 'Cancel' button is enabled (will empty and close the Betslip)
        EXPECTED: - Unchecking offered selections will decrease # on 'Accept & Bet' button
        EXPECTED: - If unchecking/checking back one of linked selections, its linked part is unchecked/checked as well
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """

        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')
        stake_name1, stake1 = list(singles_section.items())[0]
        expected_stake_value1 = float(stake1.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value1, self.stake_part1,
                         msg=f'Changed amount should be present, get "{expected_stake_value1}" instead')
        self.assertFalse(stake1.has_remove_button(expected_result=False),
                         msg=f'Remove button is present for "{stake_name1}"')
        self.__class__.stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        expected_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value2, self.stake_part2,
                         msg=f'Changed amount should be present, get "{expected_stake_value2}" instead')
        self.assertTrue(self.stake2.has_remove_button(), msg=f'Remove button is not present for "{self.stake_name2}"')
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(self.overask_trader_message.strip(), cms_overask_trader_message.strip(),
                         msg=f'Actual overask message: "{self.overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')
        betslip_section = self.get_betslip_content()
        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        cancel_button = betslip_section.cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')
        returns = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=returns, odds=self.prices[0], bet_amount=(self.stake_part1 + self.stake_part2))

    def test_014_tap_on_accept__bet__of_accepting_selections_place_a_bet_from_ox_99(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet (# of accepting selections)'/ 'Place a bet (From OX 99)
        EXPECTED: Bet is successfully placed
        """
        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()
        expected_user_balance = float(self.user_balance) - float(self.stake_part1 + self.stake_part2)
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.site.logout()
        self.site.wait_content_state('Homepage')

    def test_015_log_in_with_account_with_disabled_overask(self):
        """
        DESCRIPTION: Log in with account with disabled overask
        EXPECTED: User is logged in
        """
        self.__class__.username = tests.settings.disabled_overask_user
        self.site.login(username=self.username)

    def test_016_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: - 'Sorry, the maximum stake for this bet is X.XX' message is displayed right below the selection
        EXPECTED: - Bet is not placed
        """
        self.test_002_add_selections_to_the_betslip__open_betslip()
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=2)
        self.assertFalse(overask, msg='Overask is triggered for the User')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        error = stake.wait_for_error_message()
        expected_max_bet_msg = vec.betslip.MAX_STAKE.format(self.max_bet)
        self.assertEqual(error, expected_max_bet_msg,
                         msg=f'Actual message "{error}" is not same as Expected "{expected_max_bet_msg}"')
