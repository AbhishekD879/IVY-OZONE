import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C2987448_Verify_currency_behavior_on_Bet_Receipt_for_UK_tote_pools(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2987448
    NAME: Verify currency behavior on Bet Receipt for UK tote pools
    DESCRIPTION: This test case verifies the user currency and pool currency on Bet receipt for UK tote pools for users with different currency than pool currency.
    """
    keep_browser_open = True
    bet_amount = 1
    user_name_USD = tests.settings.user_with_usd_currency_and_card
    expected_currency = "$"

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged in with different currency than pool one
        PRECONDITIONS: 2. User balance is enough to place a bet
        PRECONDITIONS: 3. User has added one or few UK totes selections to betslip from any pool type available (Win/Place/Execta/Trifecta...)
        PRECONDITIONS: 4. User has placed bet and is on Bet receipt
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.site.login(username=self.user_name_USD)
        outcomes = self.get_single_leg_outcomes(event_id=self.eventID, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta)
        self.__class__.list_of_names = []
        self.__class__.list_of_numbers = []
        for index, (outcome_name, outcome) in enumerate(outcomes[:2]):
            self.list_of_names.append(outcome_name)
            self.list_of_numbers.append(str(index + 1))
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
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        actual_currency = self.get_betslip_content().total_stake_currency
        self.assertEqual(actual_currency, self.expected_currency,
                         msg=f'Actual currency symbol "{actual_currency}". is not equal to'
                             f'Expected currency symbol "{self.expected_currency}".')

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))

        self.get_betslip_content().bet_now_button.click()
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed')

    def test_001_on_bet_receipt_verify_the_unit_a_stake_currency_and_currency_sign_under_the_bet(self):
        """
        DESCRIPTION: On bet receipt verify the Unit a Stake currency and currency sign under the bet
        EXPECTED: * Unit Stake currency is displayed in pool currency and pool Currency Sign:
        EXPECTED: 1 Line at £2.00 per line
        EXPECTED: * Total stake currency is displayed in user currency and user Currency Sign:
        EXPECTED: Stake:€2.94
        """
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')

        single_section = receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section,
                        msg=f'"{vec.betslip.BETSLIP_SINGLES_NAME}" not found in {list(receipt_sections.keys())}')

        bet_type = single_section.bet_type
        self.assertEqual(bet_type, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Bet type is not the same as expected. '
                             f'Expected: "{vec.betslip.BETSLIP_SINGLES_NAME}". Actual: {bet_type}')

        single_selections = single_section.items_as_ordered_dict
        self.assertTrue(single_selections, msg='No single selections found')
        name = f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}'
        single = single_selections.get(name)

        self.assertTrue(single, msg=f'"{name}" selection is not in Single sections {list(single_selections.keys())}')

        self.assertEqual(single.runners_names, self.list_of_names,
                         msg=f' List of runners is not the same as expected. '
                             f'Actual: {single.runners_names}. Expected: {self.list_of_names}')
        self.assertEqual(single.runners_numbers, self.list_of_numbers,
                         msg=f' List of runners numbers is not the same as expected. '
                             f'Actual: {single.runners_numbers}. Expected: {self.list_of_numbers}')

    def test_002_verify_total_stake_currency_and_sign_at_the_bottom_of_the_bet_receipt(self):
        """
        DESCRIPTION: Verify Total stake currency and sign at the bottom of the bet receipt
        EXPECTED: Total stake currency is displayed in user currency and user Currency Sign
        EXPECTED: Eg: Total Stake: £ 1.40
        """
        # Covered in step 1
