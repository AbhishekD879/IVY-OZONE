import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot grant freebet
# @pytest.mark.hl    # cannot grant freebet
@pytest.mark.medium
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.soc
@vtest
class Test_C16379447_Place_a_bet_using_Free_Bet(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C16379447
    NAME: Place a bet using Free Bet
    DESCRIPTION: This test case verifies Free Bet Placement
    PRECONDITIONS: Instructions how to add Freebet tokens for TEST2/STAGE users
    PRECONDITIONS: or existing PROD users with already granted tokens can be found here:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has Free Bets available on his account
    PRECONDITIONS: 3. User has at least one selection added to the Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event, grant freebet to user
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids
        self.__class__.event_name = f'{self.team1} v {self.team2}'
        self._logger.info(f'*** Football event with name "{self.event_name}" and ID: "{eventID}"')
        username = self.gvc_wallet_user_client.register_new_user().username
        # We Can not place a free bet with zero account balance
        self.add_card_and_deposit(username=username, amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.visa_card)
        self.__class__.freebet_value = 3.14
        self.__class__.bet_amount = 0
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)
        self.site.login(username=username)

    def test_001_load_application_and_go_to_the_betslip(self):
        """
        DESCRIPTION: Load application and go to the Betslip
        EXPECTED: Betslip is open
        """
        self.open_betslip_with_selections(self.selection_ids[self.team1])
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened')

    def test_002_verify_use_free_bet_link_is_present_under_selection_and_press_on_it(self):
        """
        DESCRIPTION: Verify "Use Free Bet" link is present under selection and press on it
        EXPECTED: Free Bet Pop up is shown with list of Free Bets available
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.selection = singles_section.get(self.team1, None)
        self.assertTrue(self.selection, msg=f'Selection "{self.team1}" not found in the Betslip')
        self.assertTrue(self.selection.has_use_free_bet_link(), msg='"Use Free Bet" link not found')
        self.selection.freebet_tooltip.click()
        self.selection.use_free_bet_link.click()

    def test_003_select_one_of_available_free_bets_from_free_bet_pop_up(self):
        """
        DESCRIPTION: Select one of available Free Bets from Free Bet pop up
        EXPECTED: * Selected Free Bet has radio button marked as selected
        EXPECTED: * 'Add' button is shown
        """
        freebet_stake = self.select_free_bet(self.get_freebet_name(value=self.freebet_value))
        self.assertTrue(freebet_stake, msg='No Free Bet stake available')

    def test_004_tap_add_button(self):
        """
        DESCRIPTION: Tap 'Add' button
        EXPECTED: * Pop up is closed
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * Free bet value is shown under 'Stake' field and in 'Total Stake'
        """
        self.assertTrue(self.selection.has_remove_free_bet_link(), msg=f'"- Remove Free Bet" link was not found')
        self.__class__.remove_free_bet_link = self.selection.remove_free_bet_link
        total_stake, freebet_value = self.get_betslip_content().total_stake, self.selection.free_bet_stake
        self.assertEqual(total_stake, freebet_value,
                         msg=f'Free Bet value: "{freebet_value}" '
                             f'does not match Total Stake value: "{total_stake}"')

    def test_005_verify_estimated_returns_value_when_free_bet_is_selected(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value when free bet is selected
        EXPECTED: 'Estimated Returns' is calculated based on formula:
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        odds, est_returns = self.selection.odds, self.selection.est_returns
        self.verify_estimated_returns(est_returns, odds, self.bet_amount, self.freebet_value)

    def test_006_press_on_remove_free_bet_link(self):
        """
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        self.remove_free_bet_link.click()
        self.assertTrue(self.selection.has_use_free_bet_link(), msg='"Use Free Bet" link not found')
        self.__class__.use_free_bet_link = self.selection.use_free_bet_link
        actual_est_returns, expected_est_returns = self.selection.est_returns, '0.00'
        self.assertEqual(self.selection.est_returns, expected_est_returns,
                         msg=f'Actual Estimated Returns: "{actual_est_returns}" '
                             f'is not as expected: "{expected_est_returns}"')

    def test_007_tap_on_use_free_bet_link_one_more_time_and_select_one_of_available_free_bet_in_the_list(self):
        """
        DESCRIPTION: Tap on "Use Free Bet" link one more time and select one of available free bet in the list
        EXPECTED: * Selected Free Bet has radio button marked as selected
        EXPECTED: * 'Add' button is shown
        """
        self.use_free_bet_link.click()
        freebet_stake = self.select_free_bet(self.get_freebet_name(value=self.freebet_value))
        self.assertTrue(freebet_stake, msg='No Free Bet stake available')

    def test_008_tap_add_button(self):
        """
        DESCRIPTION: Tap 'Add' button
        EXPECTED: * Pop up is closed
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * 'Estimated Returns' is calculated
        """
        self.assertTrue(self.selection.has_remove_free_bet_link(), msg='"- Remove Free Bet" link was not found')
        self.test_005_verify_estimated_returns_value_when_free_bet_is_selected()

    def test_009_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * Free bet value is shown in 'Stake' and 'Total Stake' on Bet receipt
        EXPECTED: * User balance is NOT changed
        """
        user_balance = self.site.header.user_balance
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt = self.site.bet_receipt
        total_stake = bet_receipt.footer.total_stake
        self.assertEqual(total_stake, str(self.freebet_value),
                         msg=f'"Actual Free Bet stake: "{total_stake}" '
                             f'is not as expected: "{str(self.freebet_value)}"')
        bet_receipt_sections = bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No Bet Receipt sections found')
        _, section = list(bet_receipt_sections.items())[0]
        receipts = section.items_as_ordered_dict
        self.assertTrue(receipts, msg='No Bet Receipt section found')
        _, receipt = list(receipts.items())[0]
        free_bet_stake = receipt.free_bet_stake
        self.assertEqual(free_bet_stake, str(self.freebet_value),
                         msg=f'"Actual Free Bet stake: "{free_bet_stake}" '
                             f'is not as expected: "{str(self.freebet_value)}"')
        self.verify_user_balance(expected_user_balance=user_balance)
        self.site.bet_receipt.footer.click_done()

    def test_010_verify_that_bet_is_shown_with_appropriate_stake_value(self):
        """
        DESCRIPTION: Go to My Bets > Open Bets/Cash out
        DESCRIPTION: Go to the bet that was just placed
        DESCRIPTION: Verify that bet is shown with appropriate Stake Value
        EXPECTED: Placed bet is shown:
        EXPECTED: * Stake value = Free bet value which was selected while placing bet
        EXPECTED: * Appropriate Est. Returns. is shown
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        actual_stake_value, expected_stake_value = bet.stake.stake_value, str(self.freebet_value)
        self.assertEqual(actual_stake_value, expected_stake_value,
                         msg=f'Actual Stake value: "{actual_stake_value}" '
                             f'is not as expected: "{expected_stake_value}"')
        odds, est_returns = bet.odds_value, bet.est_returns.stake_value
        self.verify_estimated_returns(est_returns, odds, self.bet_amount, self.freebet_value)
