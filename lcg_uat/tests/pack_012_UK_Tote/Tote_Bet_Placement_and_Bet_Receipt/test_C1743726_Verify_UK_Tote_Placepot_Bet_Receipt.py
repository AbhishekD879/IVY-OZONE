import pytest
import tests
import voltron.environments.constants as vec
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
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55376')
@pytest.mark.login
@vtest
class Test_C1743726_Verify_UK_Tote_Placepot_Bet_Receipt(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C1743726
    NAME: Verify UK Tote Placepot Bet Receipt
    DESCRIPTION: This test case verifies Placepot Bet Receipt, which appears in betslip after the user has placed an Placepot Tote bet
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Placepot pool type is available for HR Event
    PRECONDITIONS: * **User should have placed an Placepot Tote bet**
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    bet_amount = 3
    expected_unit_stake = '{0:.2f}'.format(bet_amount)
    expected_combinations = 1
    expected_total_stake = '{0:.2f}'.format(bet_amount)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get the event with placepot totepool and place bet
        """
        event = self.get_uk_tote_event(uk_tote_placepot=True)
        self.__class__.eventID = event.event_id

        self.site.login(username=tests.settings.betplacement_user)

        place_bet_results = self.place_multiple_legs_bet(event_id=self.eventID,
                                                         tab_name=vec.uk_tote.UK_TOTE_TABS.placepot,
                                                         unit_stake=self.bet_amount)
        self.__class__.selected_outcomes = place_bet_results.get('selected_outcomes')
        self.__class__.races_titles = place_bet_results.get('races_titles')

        self.site.open_betslip()
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_001_verify_placepot_tote_bet_receipt_in_the_betslip(self):
        """
        DESCRIPTION: Verify Placepot Tote bet receipt in the betslip
        EXPECTED: The following information is displayed on the bet receipt:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Placepot Totepool"
        EXPECTED: * Number of lines
        EXPECTED: * Section for each Leg in bold with race name
        EXPECTED: * All selections selected in each Leg (in numbered order)
        EXPECTED: * Bet ID number
        EXPECTED: * Unit Stake value  x number of Lines
        EXPECTED: * Total Stake value
        EXPECTED: * Est. Returns
        EXPECTED: * Total Stake value at the bottom of Bet Receipt (Above 'Reuse Selection/Done buttons)
        EXPECTED: * Total Est. Returns value at the bottom of Bet Receipt (Above 'Reuse Selection/Done' buttons)
        EXPECTED: * 'Reuse Selection' button
        EXPECTED: * 'Done' button
        """
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
        name = f'{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}'
        self.__class__.single = single_selections.get(name)

        self.assertTrue(self.single, msg=f'"{name}" selection is not in Single sections {list(single_selections.keys())}')

        self.assertEqual(self.single.event_market_name, f'{self.expected_combinations} Line at £{self.expected_total_stake} per line',
                         msg=f'Event market name is not the same as expected. '
                             f'Actual: {self.single.event_market_name}. Expected: "{self.expected_combinations} Line"')

        for index, (leg_item_title, leg_item) in enumerate(
                list(self.single.multiple_legs.items_as_ordered_dict.items())):
            expected_title = f'Leg {index + 1}: {self.races_titles[index]}'
            self.assertEqual(expected_title, leg_item_title,
                             msg=f'Race {leg_item_title} is not displayed correctly in bet Receipt. '
                                 f'Actual: {leg_item_title}. Expected: {expected_title}.')

            selected_outcome_name = self.selected_outcomes[index]
            self.assertTrue(selected_outcome_name in leg_item.outcome,
                            msg=f'Outcome name {selected_outcome_name} is not present in Leg number {index + 1}.')

        self.assertTrue(self.single.bet_id, msg="Bet id is not shown in the Bet Receipt")

        self.assertEqual(self.site.bet_receipt.footer.total_stake, self.expected_total_stake,
                         msg=f'Footer total stake is not the same as expected. '
                             f'Actual: {self.site.bet_receipt.footer.total_stake} '
                             f'Expected: {self.expected_total_stake}')

        self.assertEqual(self.site.bet_receipt.footer.total_est_returns_raw, 'N/A',
                         msg=f'Footer Est. Returns is not the same as expected. '
                             f'Actual: {self.site.bet_receipt.footer.total_est_returns_raw} Expected: "N/A"')

        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='"Reuse Selection" button is not displayed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='"Done" button is not displayed')

    def test_002_verify_total_stake(self):
        """
        DESCRIPTION: Verify Total Stake
        EXPECTED: Total stake value corresponds to the actual total stake based on the stake value entered
        """
        self.assertEqual(self.single.total_stake, self.expected_total_stake,
                         msg=f'Total stake is not the same as expected. '
                             f'Actual: {self.single.total_stake} Expected: {self.expected_total_stake}')

    def test_003_verify_est_returns(self):
        """
        DESCRIPTION: Verify Est. Returns
        EXPECTED: Est. Returns value is "N/A"
        """
        self.assertEqual(self.single.est_returns_raw, 'N/A',
                         msg=f'Est. Returns is not the same as expected. '
                             f'Actual: {self.single.est_returns_raw} Expected: "N/A"')

    def test_004_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on 'Reuse Selection' button
        EXPECTED: * "Placepot Totepool" bet appears in the BetSlip again
        EXPECTED: * Previous stake value is entered
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]

        self.assertEqual(stake.outcome_name, f'{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}',
                         msg=f'Outcome name is not the same as expected. '
                             f'Actual: {stake.outcome_name}. Expected: \'{f"{vec.uk_tote.UPLP} {vec.uk_tote.TOTEPOOL.title()}"}\'')

        self.assertEqual(int(stake.amount_form.input.value), self.bet_amount,
                         msg=f'Stake amount is not the same as expected. '
                             f'Actual: {stake.amount_form.input.value}. Expected: {self.bet_amount}.')

    def test_005_place_a_placepot_bet_again(self):
        """
        DESCRIPTION: Place a Placepot bet again
        EXPECTED: * Placepot bet is placed successfully
        EXPECTED: * Bet Receipt appears
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_006_tap_the_done_button(self):
        """
        DESCRIPTION: Tap the "Done" button
        EXPECTED: * Bet receipt is removed from the betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * User is on racecard
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
