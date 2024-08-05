import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_011_RACES_Specifics.Horse_Racing_Specifics.Horse_Racing_Event_Details_Page.Tote_Pool_tab.BaseInternationalTote import \
    BaseInternationalTote
import voltron.environments.constants as vec
from voltron.utils.bpp_config import BPPConfig
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot place bet on International Tote on production
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.international_tote
@pytest.mark.tote
@pytest.mark.login
@vtest
class Test_C2912433_Verify_International_Tote_Place_Bet_Receipt(BaseInternationalTote, BaseBetSlipTest):
    """
    TR_ID: C2912433
    NAME: Verify International Tote Place Bet Receipt
    DESCRIPTION: This test case verifies Place bet receipt, which appears in betslip after the user has placed an Place Tote bet
    DESCRIPTION: Please note that we are **NOT** **ALLOWED** to Place a Tote bets on HL and PROD environments!
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * International Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool type is available for International HR Event
    PRECONDITIONS: * **User should have placed an Place Tote bet**
    """
    keep_browser_open = True
    selection_name = f'{vec.tote.PL} {vec.tote.TOTEPOOL}'
    bpp_config = BPPConfig()
    exchange_rates = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Racing event with International tote Place pool
        DESCRIPTION: Login
        """
        event = self.get_int_tote_event(int_tote_place=True)
        self._logger.info(f'*** Found event with parameters "{event}"')
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.currency_code = event.currency_code
        self.site.login()

        self.__class__.bet_amount = f'{event.min_total_stake:.2f}'
        self.__class__.exchange_rates = self.bpp_config.get_currency_exchange_rates()
        self._logger.info(f'*** Exchange rates: "{self.exchange_rates}"')
        exchange_rate = self.exchange_rates[self.currency_code]
        self.__class__.expected_converted_total_stake_amount = f'{(float(self.bet_amount) / exchange_rate ):.2f}'

        outcomes = self.get_single_leg_outcomes(event_id=self.eventID, tab_name=vec.tote.TOTE_TABS.place)
        first_outcome_name, first_outcome_value = outcomes[0]
        first_outcome_value.items[0].click()
        self.__class__.runner_number = first_outcome_value.runner_number if first_outcome_value.runner_number else None
        self.__class__.runner_name = first_outcome_name
        self.assertTrue(first_outcome_value.items[0].is_selected(timeout=2),
                        msg=f'Place cell is not selected for "{first_outcome_name}" runner')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        bet_builder.summary.add_to_betslip_button.click()
        self.__class__.expected_betslip_counter_value += 1
        self.assertFalse(bet_builder.is_displayed(expected_result=False, timeout=3),
                         msg='Bet builder still shown on the screen')

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.site.open_betslip()

        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, self.singles_section, msg='Tote Place bet is not added to BetSlip')

        self.__class__.place_tote_stake = self.singles_section[self.selection_name]
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))

        self.get_betslip_content().bet_now_button.click()

        self.check_bet_receipt_is_displayed()

    def test_001_verify_place_tote_bet_receipt_for_place_bet_with_1_selection_in_the_betslip(self):
        """
        DESCRIPTION: Verify Place Tote bet receipt for Place Bet with 1 selection in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Place Totepool" label
        EXPECTED: * "1 Place selection" bet type name
        EXPECTED: * "x Place selections" bet type name (in case when a couple of Place selections were selected)
        EXPECTED: * Corresponding selections with race card numbers next to them
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        bet_receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertIn(vec.betslip.BETSLIP_SINGLES_NAME.title(), bet_receipt_sections,
                      msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME} section is not present on Bet Receipt"')

        bet_receipt_singles_section = bet_receipt_sections[vec.betslip.BETSLIP_SINGLES_NAME.title()]
        self.assertEqual(bet_receipt_singles_section.bet_type, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section header label: "{bet_receipt_singles_section.bet_type}",'
                             f'expected: "{vec.betslip.BETSLIP_SINGLES_NAME}"')
        self.assertEqual(bet_receipt_singles_section.selections_count, '(1)',
                         msg=f'Bet Receipt selections count: "{bet_receipt_singles_section.selections_count}",'
                             f'expected: "(1)"')

        singles_section_selections = bet_receipt_singles_section.items_as_ordered_dict
        self.assertIn(self.selection_name, singles_section_selections,
                      msg=f'"{self.selection_name}" selection is not available on Bet Receipt')

        self.__class__.bet_receipt_info = singles_section_selections[self.selection_name]

        self.assertEqual(self.bet_receipt_info.name, self.selection_name,
                         msg=f'Bet Receipt selection name: "{self.bet_receipt_info.name}",'
                             f'expected: "{self.selection_name}"')

        self.assertEqual(self.bet_receipt_info.event_market, vec.uk_tote.ONE_SELECTION_PLACE_BET,
                         msg=f'Actual bet type "{self.bet_receipt_info.event_market}",'
                             f'expected "{vec.uk_tote.ONE_SELECTION_PLACE_BET}"')

        self.assertEqual(self.bet_receipt_info.runners_numbers[0], self.runner_number,
                         msg=f'Runner number: "{self.bet_receipt_info.runners_numbers[0]}",'
                             f'expected: "{self.runner_number}""')

        self.assertEqual(self.bet_receipt_info.runners_names[0], self.runner_name,
                         msg=f'Runner name: "{self.bet_receipt_info.runners_names[0]}", expected: "{self.runner_name}"')

    def test_002_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        # TODO VOL-1815 can verify for now that it is shown
        self.assertTrue(self.bet_receipt_info.bet_id, msg='Bet ID is not shown')

    def test_003_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        self.assertEqual(self.bet_receipt_info.total_stake, self.expected_converted_total_stake_amount,
                         msg=f'Total Stake: "{self.bet_receipt_info.total_stake}", expected: "{self.expected_converted_total_stake_amount}"')

    def test_004_verify_est_returns(self):
        """
        DESCRIPTION: Verify Est. Returns
        EXPECTED: Est. Returns value is "N/A"
        """
        self.assertEqual(self.bet_receipt_info.est_returns_raw, 'N/A',
                         msg=f'Est. Returns: "{self.bet_receipt_info.est_returns_raw}", expected: "N/A"')

    def test_005_verify_total_stake_and_total_est_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Total Est. Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        self.__class__.bet_receipt_footer = self.bet_receipt.footer

        self.assertEqual(self.bet_receipt_footer.total_stake, self.expected_converted_total_stake_amount,
                         msg=f'Total Stake: "{self.bet_receipt_footer.total_stake}", '
                             f'expected: "{self.expected_converted_total_stake_amount}"')

        self.assertEqual(self.bet_receipt_footer.total_est_returns_raw, 'N/A',
                         msg=f'Total Est. Returns: "{self.bet_receipt_footer.total_est_returns_raw}", expected: "N/A"')

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Place" bet appears in the BetSlip again
        """
        self.bet_receipt_footer.reuse_selection_button.click()

        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, singles_section, msg='Win Tote bet is not added to BetSlip')
        self.__class__.place_tote_stake = singles_section[self.selection_name]

    def test_007_place_a_place_bet_again(self):
        """
        DESCRIPTION: Place a 'Place' bet again
        EXPECTED: * Place bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.enter_stake_amount(stake=(self.place_tote_stake.name, self.place_tote_stake))

        self.get_betslip_content().bet_now_button.click()

        self.check_bet_receipt_is_displayed()

    def test_008_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        """
        self.site.bet_receipt.footer.done_button.click()

        if self.device_type == "mobile":
            result = self.site.has_betslip_opened(expected_result=False)
            self.assertFalse(result, msg='Betslip should not be displayed')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_message,
                                     name='Waiting for "You have no selections in the slip" message in Betslip',
                                     timeout=5)
            self.assertTrue(result, msg="'You have no selections in the slip' message is not shown")
