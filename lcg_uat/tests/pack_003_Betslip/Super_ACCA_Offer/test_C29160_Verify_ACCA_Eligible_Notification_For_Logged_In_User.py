import pytest
import tests
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29160_Verify_ACCA_Eligible_Notification_For_Logged_In_User(BaseBetSlipTest):
    """
    TR_ID: C29160
    NAME: Verify ACCA Eligible Notification displaying for logged in user
    DESCRIPTION: This test case verifies ACCA Eligible Notification displaying for logged in user
    """
    keep_browser_open = True
    stake = None
    prices = {
        'odds_home': '5/1',
        'odds_draw': '3/2',
        'odds_away': '4/1'
    }

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events and login
        """
        # Autotest ACCA offer for autotest leagues2 has TBL bet type so it requires only 3 selections to be 'eligible'
        selection_ids_1 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids
        selection_ids_2 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids
        selection_ids_3 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids
        selection_ids_4 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids

        self.__class__.selection_ids = (list(selection_ids_1.values())[0],
                                        list(selection_ids_2.values())[0],
                                        list(selection_ids_3.values())[0],
                                        list(selection_ids_4.values())[0])

        self.site.login(username=tests.settings.freebet_user)

    def test_001_open_selections_in_betslip(self):
        """
        DESCRIPTION: Add selections to Betslip that are applicable for ACCA Insurance and their combined odds are above 3/1
        EXPECTED: In order to see ACCA Eligible Notification, the number of selections should correspond to the offer trigger type in OB
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_check_eligible_acca_offer(self):
        """
        DESCRIPTION: Verify ACCA Eligible Notification displaying in Betslip for appropriate Multiple
        EXPECTED: ACCA Eligible Notification is displayed for Treble Multiples
        """
        self.__class__.stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.ACC4,
                                                               offer_type=self.cms_config.constants.ACCA_ELIGIBLE_INSURANCE_OFFER)

    def test_003_enter_value_less_than_2_pounds(self):
        """
        DESCRIPTION: Enter value that is less than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification disappears
        """
        bet_amount = '1.50'
        try:
            self.stake.amount_form.input.value = bet_amount
            amount = self.stake.amount_form.input.value
        except StaleElementReferenceException:
            self.__class__.stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                                                   offer_type=self.cms_config.constants.ACCA_ELIGIBLE_INSURANCE_OFFER)
            self.stake.amount_form.input.value = bet_amount
            amount = self.stake.amount_form.input.value

        self.assertEqual(amount, bet_amount, msg=f'Stake amount value "{amount}" '
                                                 f'is not the same as entered "{bet_amount}"')
        self.stake.wait_for_element_disappear(timeout=2)
        self.assertFalse(self.stake.has_acca_insurance_offer(expected_result=False),
                         msg='Treble stake still have ACCA Eligible offer however entered stake is less than 2 pounds')

    def test_004_enter_value_that_is_equal_2_pounds(self):
        """
        DESCRIPTION: Enter value that is equal to 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification appears
        """
        bet_amount = '2.00'
        self.stake.amount_form.input.value = bet_amount
        amount = self.stake.amount_form.input.value
        self.assertEqual(amount, bet_amount, msg=f'Stake amount value "{amount}" '
                                                 f'is not the same as entered "{bet_amount}"')
        self.assertTrue(self.stake.has_acca_insurance_offer(), msg='Treble stake does not have ACCA Eligible offer')

    def test_005_enter_value_that_is_more_than_2_pounds(self):
        """
        DESCRIPTION: Enter value that is more than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Eligible Notification appears
        """
        bet_amount = '2.50'
        self.stake.amount_form.input.value = bet_amount
        amount = self.stake.amount_form.input.value
        self.assertEqual(amount, bet_amount, msg=f'Stake amount value "{amount}" '
                                                 f'is not the same as entered "{bet_amount}"')
        self.assertTrue(self.stake.has_acca_insurance_offer(), msg='Treble stake does not have ACCA Eligible offer')
