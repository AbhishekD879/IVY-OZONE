import pytest
from fractions import Fraction
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod--->can't trigger overask for prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C16408233_Accepting_split_multiple_bets_without_linked_parts(BaseBetSlipTest):
    """
    TR_ID: C16408233
    NAME: Accepting split multiple bets without linked parts
    DESCRIPTION: This test case verifies splitting and bet placement for multiple bets
    PRECONDITIONS: * For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: * User is logged in to the application
    """
    keep_browser_open = True
    prices = {0: '1/2'}
    stake_part1 = 0.50
    stake_part2 = 0.50
    eventIDs = []
    selectionIDs = []

    def verify_est_returns(self, est_returns, odd1, odd2, odd3, bet_amount):
        S1 = (float(Fraction(odd1)) * float(bet_amount)) + float(bet_amount)
        S2 = (float(Fraction(odd2)) + 1) * S1
        S3 = (float(Fraction(odd3)) + 1) * S2
        expected_est_returns = round(float(2 * S3), 2)
        self.assertAlmostEqual(float(est_returns), expected_est_returns,
                               msg=f'Actual estimated returns "{est_returns}" doesn\'t match expected '
                                   f'"{expected_est_returns}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 3):
            event = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet, lp_prices=self.prices)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
        self.site.login()
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol

    def test_001_add_3_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 3 selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_002__enter_stake_value_into_treble_field_which_is_higher_than_the_maximum_limit_for_added_selection_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stake value into 'Treble' field which is higher than the maximum limit for added selection
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_003_trigger_bet_split_and_stakeoddsprice_type_modification_by_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Bet is split according to design for multiple selections
        EXPECTED: * The changed bet is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to the new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: **Design from OX 99**
        EXPECTED: ![](index.php?/attachments/get/34123)  ![](index.php?/attachments/get/34124)
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.eventIDs)
        account_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        bet_id = list(bets_details.keys())[0]
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventIDs, bet_id=[bet_id],
                                     betslip_id=betslip_id,
                                     stake_part1=self.stake_part1,
                                     stake_part2=self.stake_part2)

        sleep(2)
        self.__class__.sections = self.get_betslip_content().overask_trader_section.items
        is_selection_splitted = wait_for_result(lambda: len(self.sections) == 8,
                                                timeout=30,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        for section in range(len(self.sections)):
            if section in [3, 7]:
                price_color = self.sections[section].stake_value.background_color_value
                self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'"Modified price" is not highlighted in yellow')
                odds = float(self.sections[section].stake_value.text.replace(self.user_currency, ""))
                self.assertEqual(odds, self.stake_part1,
                                 msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.stake_part1}"')

                self.assertTrue(self.sections[section].has_remove_button(),
                                msg='Remove button is not present for "{self.sections[section].name}"')
        betslip_section = self.get_betslip_content()
        actual_est_returns = round(float(self.get_betslip_content().total_estimate_returns), 2)
        self.verify_est_returns(est_returns=actual_est_returns, bet_amount=self.stake_part1,
                                odd1=self.prices[0], odd2=self.prices[0], odd3=self.prices[0])

        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')

        cancel_button = betslip_section.cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')

    def test_004_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        treble_name = vec.bet_history.BET_TYPES.TBL
        self.assertEqual(len(betreceipt_sections), 2,
                         msg=f'Bet receipt section should have 2 placed bets found: "{treble_name}"')
        for section in range(len(betreceipt_sections)):
            self.assertEqual(betreceipt_sections[section].name, treble_name,
                             msg=f'Found section "{betreceipt_sections[section]}" is not same as expected section "{treble_name}"')
