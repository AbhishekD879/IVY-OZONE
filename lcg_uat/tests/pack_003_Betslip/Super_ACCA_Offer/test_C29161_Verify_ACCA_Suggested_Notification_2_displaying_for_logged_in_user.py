import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29161_Verify_ACCA_Suggested_Notification_2_displaying_for_logged_in_user(BaseBetSlipTest):
    """
    TR_ID: C29161
    NAME: Verify ACCA Suggested Notification 2 displaying for logged in user
    DESCRIPTION: Verify ACCA Suggested Notification 2 displaying for logged in user
    """
    keep_browser_open = True
    prices = {
        'odds_home': '1/100',
        'odds_draw': '1/200',
        'odds_away': '1/20'
    }
    treble_stake = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        selection_ids_1 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids
        selection_ids_2 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids
        selection_ids_3 = self.ob_config.add_football_event_to_autotest_league2(lp=self.prices).selection_ids

        self.__class__.selection_ids = (list(selection_ids_1.values())[0],
                                        list(selection_ids_2.values())[0],
                                        list(selection_ids_3.values())[0])

    def test_001_login_as_user_that_has_sufficient_funds_to_place_bet(self):
        """
        DESCRIPTION: Login as user that has sufficient funds to place a bet
        """
        self.site.login(username=tests.settings.freebet_user)

    def test_002_open_selections_in_betslip(self):
        """
        DESCRIPTION: Add selections to Betslip that are applicable for ACCA Insurance and their combined odds are below 3/1
        EXPECTED: In order to see ACCA Eligible Notification, the number of selections should correspond to the offer trigger type in OB
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_003_verify_acca_suggested_notification_2_displaying_in_betslip_for_appropriate_multiple(self):
        """
        DESCRIPTION: Verify ACCA Suggested Notification 2 displaying in Betslip for appropriate Multiple
        EXPECTED: ACCA Suggested Notification 2 is displayed
        """
        self.__class__.treble_stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                                                      offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER)

    def test_004_enter_value_that_is_less_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is less than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 disappears
        """
        try:
            self.treble_stake.amount_form.input.value = 1
            amount = self.treble_stake.amount_form.input.value
        except StaleElementReferenceException:
            self.__class__.treble_stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                                                          offer_type=self.cms_config.constants.ACCA_SUGGESTED_TYPE2_INSURANCE_OFFER)
            self.treble_stake.amount_form.input.value = 1
            amount = self.treble_stake.amount_form.input.value
        self.assertEqual(amount, '1', msg=f'Stake amount value "{amount}" is not the same as entered 1')

        self.assertFalse(self.treble_stake.has_acca_insurance_offer(expected_result=False),
                         msg='Treble stake still has Suggested offer however entered stake is less than 2 pounds')

    def test_005_enter_value_that_is_equal_to_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is equal to 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 appears
        """
        try:
            self.treble_stake.amount_form.input.value = 2
            amount = self.treble_stake.amount_form.input.value
        except StaleElementReferenceException:
            self.__class__.treble_stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                                                          offer_type=self.cms_config.constants.ACCA_SUGGESTED_TYPE2_INSURANCE_OFFER)
            self.treble_stake.amount_form.input.value = 2
            amount = self.treble_stake.amount_form.input.value
        self.assertEqual(amount, '2', msg=f'Stake amount value "{amount}" is not the same as entered 2')
        self.assertTrue(self.treble_stake.has_acca_insurance_offer(),
                        msg='Treble stake does not have ACCA Suggested offer type 2')

    def test_006_enter_value_that_is_more_than_2_gbpeur_in_stake_field(self):
        """
        DESCRIPTION: Enter value that is more than 2 (GBP/EUR) in 'Stake' field
        EXPECTED: ACCA Suggested Notification 2 is still displayed
        """
        try:
            self.treble_stake.amount_form.input.value = 3
            amount = self.treble_stake.amount_form.input.value
        except StaleElementReferenceException:
            self.__class__.treble_stake = self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                                                          offer_type=self.cms_config.constants.ACCA_SUGGESTED_TYPE2_INSURANCE_OFFER)
            self.treble_stake.amount_form.input.value = 3
            amount = self.treble_stake.amount_form.input.value
        self.assertEqual(amount, '3', msg=f'Stake amount value "{amount}" is not the same as entered 3')
        self.assertTrue(self.treble_stake.has_acca_insurance_offer(),
                        msg='Treble stake does not have ACCA Suggested offer type 2')
