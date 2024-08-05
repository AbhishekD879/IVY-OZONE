
import voltron.environments.constants as vec
import time
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.uk_tote
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.races
# @pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3699')
@pytest.mark.login
@vtest
class Test_C2912269_Verify_UK_Tote_Place_Bet_Receipt(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2912269
    NAME: Verify UK Tote Place Bet Receipt
    DESCRIPTION: This test case verifies Place bet receipt, which appears in betslip after the user has placed an Place Tote bet
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Place pool type is available for HR Event
    PRECONDITIONS: * **User should have placed an Place Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    bet_amount = 2.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with user which account balance is sufficient to cover the bet
        DESCRIPTION: * UK Tote feature is enabled in CMS
        DESCRIPTION: * Place pool type is available for HR Event
        DESCRIPTION: * User have placed an Place Tote bet
        """
        event = self.get_uk_tote_event(uk_tote_place=True)
        self.__class__.eventID = event.event_id
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        totepool_tab_opened = \
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
                vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(totepool_tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        place_tab_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.place)
        self.assertTrue(place_tab_opened, msg=f'{vec.uk_tote.UK_TOTE_TABS.place}" tab is not opened')
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')
        outcome_name, outcome = list(outcomes.items())[0]
        cells = outcome.items
        self.assertTrue(cells, msg=f'No cells found for "{outcome_name}"')
        cell = cells[0]
        cell.click()
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.is_displayed(timeout=3), msg='Bet builder is not shown')
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        time.sleep(0.5)  # necessary spike in order to click "ADD TO BETSLIP" button
        bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(bet_builder.is_displayed(expected_result=False, timeout=3),
                         msg='Bet builder still shown on the screen')

        self.verify_betslip_counter_change(expected_value=1)

        self.site.open_betslip()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(self.singles_section.items())[0]
        self.assertIn(f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}', self.singles_section,
                      msg='Tote Place bet is not added to BetSlip')
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
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
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No Bet Receipt sections found')
        self.__class__.singles_section = betreceipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertEqual(self.singles_section.bet_type, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Actual Bet label: {self.singles_section.bet_type} '
                         f'is not the same as expected: {vec.betslip.BETSLIP_SINGLES_NAME,}')
        self.__class__.single = self.singles_section.items_as_ordered_dict[f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}']
        self.assertEqual(self.single.name, f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}',
                         msg=f'Actual Totepool label: {self.single.name} '
                         f'is not the same as expected: \'{f"{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}"}\'')

    def test_002_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        self.assertTrue(self.single.bet_id, msg='Bet ID is not shown in the Bet Receipt')

    def test_003_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        expected_total_stake = '{0:.2f}'.format(self.bet_amount)
        self.assertEqual(self.single.total_stake, expected_total_stake,
                         msg=f'Total stake: "{self.single.total_stake}" '
                         f'is not the same as expected: "{expected_total_stake}"')

    def test_004_verify_est_returns(self):
        """
        DESCRIPTION: Verify Est. Returns
        EXPECTED: Est. Returns value is "N/A"
        """
        self.assertEqual(self.single.est_returns_raw, 'N/A',
                         msg=f'Est. Returns: "{self.single.est_returns_raw}" '
                         f'is not the same as expected: "N/A"')

    def test_005_verify_total_stake_and_total_est_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Total Est. Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        expected_total_stake = '{0:.2f}'.format(self.bet_amount)
        self.assertEqual(self.site.bet_receipt.footer.total_stake, expected_total_stake,
                         msg=f'Total Stake: "{self.site.bet_receipt.footer.total_stake}" '
                         f'is not the same as expected: "{expected_total_stake}"')
        self.assertEqual(self.site.bet_receipt.footer.total_estimate_returns, 'N/A',
                         msg=f'Total Est. Returns: "{self.site.bet_receipt.footer.total_estimate_returns}" '
                         f'is not the same as expected: "N/A"')

    def test_006_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Place" bet appears in the BetSlip again
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section.items(), msg='*** No stakes found')
        stake_name, stake = list(self.singles_section.items())[0]
        self.assertEqual(stake.outcome_name, f'{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}',
                         msg=f'Outcome name: {stake.outcome_name} '
                         f'is not the same as expected: \'{f"{vec.uk_tote.PL} {vec.uk_tote.TOTEPOOL.title()}"}\'')

    def test_007_place_a_place_bet_again(self):
        """
        DESCRIPTION: Place a 'Place' bet again
        EXPECTED: * Place bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_008_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        """
        self.site.bet_receipt.footer.done_button.click()
        if tests.settings.device_type in ['mobile', 'tablet']:
            self.assertFalse(self.site.has_betslip_opened(), msg='Bet Slip is not closed')
        else:
            self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False))
            actual_msg = self.get_betslip_content().no_selections_title
            self.assertEqual(actual_msg, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Actual message "{actual_msg}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.site.wait_content_state(state_name='RacingEventDetails')
