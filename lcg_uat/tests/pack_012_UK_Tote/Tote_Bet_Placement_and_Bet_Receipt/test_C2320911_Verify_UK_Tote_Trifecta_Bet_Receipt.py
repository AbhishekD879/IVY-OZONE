
import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.bet_receipt
@pytest.mark.bet_placement
@pytest.mark.races
# @pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3699')
@pytest.mark.login
@vtest
class Test_C2320911_Verify_UK_Tote_Trifecta_Bet_Receipt(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2320911
    NAME: Verify UK Tote Trifecta Bet Receipt
    DESCRIPTION: This test case verifies Trifecta bet receipt, which appears in betslip after the user has placed an Trifecta Tote bet
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Trifecta pool types are available for HR Event
    PRECONDITIONS: * **User should have placed an Trifecta Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    bet_amount = 3
    expected_combinations = 24
    expected_total_stake = '{0:.2f}'.format(bet_amount * expected_combinations)

    def test_001_verify_trifecta_tote_bet_receipt_for_1_trifecta_bet_in_the_betslip(self):
        """
        DESCRIPTION: Verify Trifecta Tote bet receipt for **1 Trifecta Bet** in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Trifecta" bet type name
        EXPECTED: * Two selections with correct order according to the selected check boxes
        """
        event = self.get_uk_tote_event(uk_tote_trifecta=True)
        self.__class__.eventID = event.event_id

        self.site.login(username=tests.settings.betplacement_user)

        outcomes = self.get_single_leg_outcomes(event_id=self.eventID, tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        list_of_names = []
        list_of_numbers = ['1', '2', '3']
        for index, (outcome_name, outcome) in enumerate(outcomes[:3]):
            list_of_names.append(outcome.name)
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        _, section = list(sections.items())[0]
        self.assertTrue(section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        section.bet_builder.summary.add_to_betslip_button.click()

        self.site.open_betslip()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))

        self.get_betslip_content().bet_now_button.click()
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed')

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')

        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" not found in {list(receipt_sections.keys())}')

        bet_type = single_section.bet_type
        self.assertEqual(bet_type, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Bet type is not the same as expected. '
                             f'Expected: "{vec.betslip.BETSLIP_SINGLES_NAME}". Actual: {bet_type}')

        single_selections = single_section.items_as_ordered_dict
        self.assertTrue(single_selections, msg='No single selections found')
        name = f'{vec.uk_tote.UTRI} {vec.uk_tote.TOTEPOOL.title()}'
        single = single_selections.get(name)

        self.assertTrue(single, msg=f'"{name}" selection is not in Single sections {list(single_selections.keys())}')

        self.assertEqual(single.runners_names, list_of_names,
                         msg=f' List of runners is not the same as expected. '
                             f'Actual: {single.runners_names}. Expected: {list_of_names}')
        self.assertEqual(single.runners_numbers, list_of_numbers,
                         msg=f' List of runners numbers is not the same as expected. '
                             f'Actual: {single.runners_numbers}. Expected: {list_of_numbers}')

    def test_002_place_a_combination_trifecta_tote_bet_verify_trifecta_tote_bet_receipt_for_combination_trifecta_in_the_betslip(self):
        """
        DESCRIPTION: * Place a **Combination Trifecta** tote bet
        DESCRIPTION: * Verify Trifecta Tote bet receipt for **Combination Trifecta** in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Trifecta Totepool" label
        EXPECTED: * "x lines Combination Trifecta" bet type name
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: WHERE
        EXPECTED: '#' of lines in Combination Trifecta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        outcomes = self.get_single_leg_outcomes(event_id=self.eventID, tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)

        list_of_names = []
        list_of_numbers = []
        for index, (outcome_name, outcome) in enumerate(outcomes[:4]):
            list_of_numbers.append(outcome.runner_number)
            list_of_names.append(outcome.name)
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[3]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        _, section = list(sections.items())[0]
        self.assertTrue(section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        section.bet_builder.summary.add_to_betslip_button.click()

        self.site.open_betslip()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')

        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" not found in {list(receipt_sections.keys())}')

        bet_type = single_section.bet_type
        self.assertEqual(bet_type, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Bet type is not the same as expected. '
                             f'Expected: "{vec.betslip.BETSLIP_SINGLES_NAME}". Actual: {bet_type}')

        single_selections = single_section.items_as_ordered_dict
        self.assertTrue(single_selections, msg='No single selections found')
        name = f'{vec.uk_tote.UTRI} {vec.uk_tote.TOTEPOOL.title()}'
        self.__class__.single = single_selections.get(name)

        self.assertTrue(self.single, msg=f'"{name}" selection is not in Single sections {list(single_selections.keys())}')

        self.assertEqual(self.single.runners_names, list_of_names,
                         msg=f' List of runners is not the same as expected. '
                             f'Actual: {self.single.runners_names}. Expected: {list_of_names}')
        self.assertEqual(self.single.runners_numbers, list_of_numbers,
                         msg=f' List of runners numbers is not the same as expected. '
                             f'Actual: {self.single.runners_numbers}. Expected: {list_of_numbers}')

    def test_003_verify_bet_id(self):
        """
        DESCRIPTION: Verify Bet ID
        EXPECTED: Bet ID corresponds to the value, received from OpenBet
        """
        self.assertTrue(self.single.bet_id, "Bet id is not shown in the Bet Receipt")

    def test_004_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        self.assertEqual(self.single.total_stake, self.expected_total_stake,
                         msg=f'Total stake is not the same as expected. '
                             f'Actual: {self.single.total_stake} Expected: {self.expected_total_stake}')

    def test_005_verify_est_returns(self):
        """
        DESCRIPTION: Verify Est. Returns
        EXPECTED: Est. Returns value is "N/A"
        """
        self.assertEqual(self.single.est_returns_raw, 'N/A',
                         msg=f'Est. Returns is not the same as expected. '
                             f'Actual: {self.single.est_returns_raw} Expected: "N/A"')

    def test_006_verify_total_stake_and_total_est_returns_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify Total Stake and Total Est. Returns at the bottom of the betslip
        EXPECTED: * Total Stake value corresponds to the actual total stake based on the stake value entered
        EXPECTED: * Total Est. Returns value is "N/A"
        """
        bet_receipt = self.site.bet_receipt.footer
        total_stake = bet_receipt.total_stake
        self.assertEqual(total_stake, self.expected_total_stake,
                         msg=f'Footer total stake is not the same as expected. '
                             f'Actual: "{total_stake}" '
                             f'Expected: "{self.expected_total_stake}"')

        total_est_returns_raw = bet_receipt.total_est_returns_raw
        self.assertEqual(total_est_returns_raw, 'N/A',
                         msg=f'Footer Est. Returns is not the same as expected. '
                             f'Actual: "{total_est_returns_raw}" Expected: "N/A"')

    def test_007_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: "Trifecta" bet appears in the BetSlip again
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]

        self.assertEqual(stake.outcome_name, f'{vec.uk_tote.UTRI} {vec.uk_tote.TOTEPOOL.title()}',
                         msg=f'Outcome name is not the same as expected. '
                             f'Actual: "{stake.outcome_name}". Expected: \'{f"{vec.uk_tote.UTRI} {vec.uk_tote.TOTEPOOL.title()}"}\'')

        self.enter_stake_amount(stake=(stake_name, stake))
        self.get_betslip_content().bet_now_button.click()

    def test_008_place_a_trifecta_bet_again(self):
        """
        DESCRIPTION: Place a Trifecta bet again
        EXPECTED: * Trifecta bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.check_bet_receipt_is_displayed()

    def test_009_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        """
        self.site.bet_receipt.footer.done_button.click()

        if self.device_type in ['mobile', 'tablet']:
            self.assertFalse(self.site.has_betslip_opened(), msg='Bet Slip is not closed')
            self.site.wait_content_state(state_name='RacingEventDetails')
            self.site.open_betslip()
        else:
            self.site.is_bet_receipt_displayed(expected_result=False)
            self.site.wait_content_state(state_name='RacingEventDetails')

        self.assertEqual(self.get_betslip_content().no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'BetSlip was not cleared. Message {vec.betslip.NO_SELECTIONS_TITLE} '
                             f'is not shown')
