from collections import OrderedDict
import pytest

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
@pytest.mark.slow(600)
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C29159_ACCA_Suggested_Notification_displaying_depending_on_users_currency(BaseBetSlipTest):
    """
    TR_ID: C29159
    NAME: ACCA Suggested Notification displaying depending on users currency
    DESCRIPTION: This test case verifies 'Place your ACCA (X selections)' Section currency displaying depending on user's currency
    """
    keep_browser_open = True
    # In order to qualify for ACCA offer, combined odds should be >= 3/1, hence 3/1*3 = 9/1 and we will qualify
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        selection_ids_1 = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices).selection_ids
        selection_ids_2 = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices).selection_ids
        selection_ids_3 = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices).selection_ids

        self.__class__.selection_ids = (list(selection_ids_1.values())[0],
                                        list(selection_ids_2.values())[0],
                                        list(selection_ids_3.values())[0])

    def test_001_login_with_user_who_use_gbp_currency(self):
        """
        DESCRIPTION: Login with user who use GBP currency
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.odds_boost_user)

    def test_002_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_003_verify_acca_notification_displaying(self):
        """
        DESCRIPTION: Verify ACCA Notification displaying
        EXPECTED: ACCA Notification is displayed for user with GBP currency
        """
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER)

    def test_004_repeat_steps_1_3_for_user_with_euro_currency(self):
        """
        DESCRIPTION: Repeat steps 1-3 for user with Euro currency
        EXPECTED: ACCA Notification is displayed for user with Euro currency
        """
        self.clear_betslip()
        self.site.logout()
        self.site.login(username=tests.settings.user_with_euro_currency_and_card)
        self.test_002_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance()
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER, currency='€')

    def test_005_repeat_steps_1_3_for_user_with_usd_currency(self):
        """
        DESCRIPTION: Repeat steps 1-3 for user with USD currency
        EXPECTED: ACCA Notification is NOT displayed for user with USD currency even if in OpenBet response ACCA Offer is present
        """
        self.clear_betslip()
        self.site.logout()
        self.site.login(username=tests.settings.user_with_usd_currency_and_card)
        self.test_002_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance()
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER, expected_result=False)
