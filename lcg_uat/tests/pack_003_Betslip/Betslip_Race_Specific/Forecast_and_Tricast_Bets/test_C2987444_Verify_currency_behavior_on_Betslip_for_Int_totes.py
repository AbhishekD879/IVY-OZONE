import pytest
import tests
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Horse_Racing_Specifics.Horse_Racing_Event_Details_Page.Tote_Pool_tab.BaseInternationalTote import \
    BaseInternationalTote
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.frequent_blocker
@vtest
class Test_C2987444_Verify_currency_behavior_on_Betslip_for_Int_totes(BaseInternationalTote, BaseBetSlipTest):
    """
    TR_ID: C2987444
    NAME: Verify currency behavior on Betslip for Int totes
    DESCRIPTION: This test case verifies the user currency and pool currency on Betslip for Int tote pools for users with different currency than pool currency.
    PRECONDITIONS: 1. User is logged in with different currency than pool one
    PRECONDITIONS: 2. User balance is enough to place a bet
    PRECONDITIONS: 3. User in on any Int tote pool (Win/Place/Execta/Trifecta...) race card.
    """
    keep_browser_open = True
    currency_USD = 'USD'
    expected_currency = "$"

    def test_001_choose_any_active_selection_from_any_pool_available_winplaceexectatrifecta_and_add_it_to_betslip(self):
        """
        DESCRIPTION: Choose any active selection from any pool available (Win/Place/Execta/Trifecta...) and add it to betslip
        EXPECTED: * Selection is successfully added to betslip
        EXPECTED: * Betslip counter is increased by 1 item
        """
        event = self.get_int_tote_event()
        self.__class__.user_USD = tests.settings.user_with_usd_currency_and_card
        self.site.login(username=self.user_USD)
        self.__class__.selection_id1 = event.selection_ids[:1]
        self.__class__.selection_id2 = event.selection_ids[1:2]
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        actual_currency = self.get_betslip_content().total_stake_currency
        self.assertEqual(actual_currency, self.expected_currency,
                         msg=f'Actual currency symbol "{actual_currency}". is not equal to'
                             f'Expected currency symbol "{self.expected_currency}".')

    def test_002_click_on_betslip_and_verify_the_stake_and_total_stake_currency_sign(self):
        """
        DESCRIPTION: Click on Betslip and verify the Stake and Total stake currency sign
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        # Covered in step 1

    def test_003_enter_any_value_into_stake_value_input_field(self):
        """
        DESCRIPTION: Enter any value into stake value input field
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(singles_section, msg='No stakes found')
        self.stake.amount_form.input.value = f'{self.bet_amount}'
        actual_currency = self.get_betslip_content().total_stake_currency
        self.assertEqual(actual_currency, self.expected_currency,
                         msg=f'Actual currency symbol "{actual_currency}". is not equal to'
                             f'Expected currency symbol "{self.expected_currency}".')

    def test_004_add_few_selections_from_1_pool_to_betslip_and_verify_currency_signs(self):
        """
        DESCRIPTION: Add few selections from 1 pool to betslip and verify currency signs
        EXPECTED: * Stake value currency is displayed in Pool currency and pool Currency Sign
        EXPECTED: * Total stake value currency is displayed in User currency and user Currency Sign
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id2)
        actual_currency = self.get_betslip_content().total_stake_currency
        self.assertEqual(actual_currency, self.expected_currency,
                         msg=f'Actual currency symbol "{actual_currency}". is not equal to'
                             f'Expected currency symbol "{self.expected_currency}".')
