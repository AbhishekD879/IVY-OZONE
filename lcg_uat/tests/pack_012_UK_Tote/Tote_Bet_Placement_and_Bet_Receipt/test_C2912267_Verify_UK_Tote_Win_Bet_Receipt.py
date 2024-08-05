
import voltron.environments.constants as vec
import pytest
import tests
import time
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.uk_tote
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.races
# @pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3699')
@pytest.mark.login
@vtest
class Test_C2912267_Verify_UK_Tote_Win_Bet_Receipt(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2912267
    NAME: Verify UK Tote Win Bet Receipt
    DESCRIPTION: This test case verifies Win bet receipt, which appears in betslip after the user has placed an Win Tote bet
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Win pool type is available for HR Event
    PRECONDITIONS: * **User should have placed an Win Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    selection_name = 'Win Totepool'
    bet_receipt = None
    runner_number = runner_name = None
    bet_receipt_info = bet_receipt_footer = None
    win_tote_stake = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find HR event with available Win pool type and place Win Tote bet
        """
        event = self.get_uk_tote_event(uk_tote_win=True)
        self.__class__.bet_amount = '{0:.2f}'.format(event.min_total_stake)
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')
        self.site.login(async_close_dialogs=False)

        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        win_tab_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.win)
        self.assertTrue(win_tab_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.win}" tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        outcome_name, outcome = list(outcomes.items())[0]
        self.__class__.runner_number = outcome.runner_number if outcome.runner_number else None
        self.__class__.runner_name = outcome_name
        cells = outcome.items
        self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
        cell = cells[0]
        cell.click()
        self.assertTrue(cell.is_selected(timeout=2),
                        msg=f'Win cell is not selected for "{outcome_name}" runner')
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        time.sleep(0.5)  # necessary spike in order to click "ADD TO BETSLIP" button
        bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(bet_builder.is_displayed(expected_result=False, timeout=3),
                         msg='Bet builder still shown on the screen')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, singles_section, msg='Tote Win bet is not added to BetSlip')
        win_tote_stake = singles_section[self.selection_name]

        self.enter_stake_amount(stake=(win_tote_stake.name, win_tote_stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_001_verify_win_tote_bet_receipt_for_win_bet(self):
        """
        DESCRIPTION: Verify Win Tote Bet Receipt for Win Bet
        EXPECTED: The following information is displayed on the Bet Receipt:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Win Totepool" label
        EXPECTED: * "1 Win selection" bet type name
        EXPECTED: * "x Win selections" bet type name (in case when a couple of Win selections were selected)
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

        singles_section_selections = bet_receipt_singles_section.items_as_ordered_dict
        self.assertIn(self.selection_name, singles_section_selections,
                      msg=f'"{self.selection_name}" selection is not available on Bet Receipt')

        self.__class__.bet_receipt_info = singles_section_selections[self.selection_name]

        self.assertEqual(self.bet_receipt_info.name, self.selection_name,
                         msg=f'Bet Receipt selection name: "{self.bet_receipt_info.name}",'
                             f'expected: "{self.selection_name}"')

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
        self.assertTrue(self.bet_receipt_info.bet_id, msg='Bet ID is not shown')

    def test_003_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        self.assertEqual(self.bet_receipt_info.total_stake, self.bet_amount,
                         msg=f'Total Stake: "{self.bet_receipt_info.total_stake}", expected: "{self.bet_amount}"')

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

        self.assertEqual(self.bet_receipt_footer.total_stake, self.bet_amount,
                         msg=f'Total Stake: "{self.bet_receipt_footer.total_stake}", expected: "{self.bet_amount}"')

        self.assertEqual(self.bet_receipt_footer.total_est_returns_raw, 'N/A',
                         msg=f'Total Est. Returns: "{self.bet_receipt_footer.total_est_returns_raw}", expected: "N/A"')

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Win" bet appears in the BetSlip again
        """
        self.bet_receipt_footer.reuse_selection_button.click()

        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.selection_name, singles_section, msg='Win Tote bet is not added to BetSlip')
        self.__class__.win_tote_stake = singles_section[self.selection_name]

    def test_007_place_a_win_bet_again(self):
        """
        DESCRIPTION: Place a Win bet again
        EXPECTED: * Win bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.enter_stake_amount(stake=(self.win_tote_stake.name, self.win_tote_stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_008_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        """
        self.site.bet_receipt.footer.done_button.click()

        if tests.settings.device_type == "mobile":
            result = self.site.has_betslip_opened(expected_result=False)
            self.assertFalse(result, msg='Betslip should not be displayed')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_message,
                                     name='Waiting for "You have no selections in the slip" message in Betslip',
                                     timeout=5)
            self.assertTrue(result, msg="'You have no selections in the slip' message is not shown")
