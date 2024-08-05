from collections import OrderedDict
import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
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
class Test_C29157_Verify_ACCA_Suggested_Notification_appearing_for_NOT_Logged_In_user(BaseBetSlipTest):
    """
    TR_ID: C29157
    NAME: Verify ACCA Suggested Notification appearing for NOT Logged In user
    DESCRIPTION: This test case verifies that ACCA Suggested Notification does not appear for NOT Logged In user
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

    def test_001_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_verify_acca_notification_message_displaying(self):
        """
        DESCRIPTION: Verify ACCA Notification message displaying
        EXPECTED: ACCA Notification message is NOT displayed for user in the Betslip for appropriate Multiple
        """
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER, expected_result=False)
        self.site.close_betslip()

    def test_003_login_to_application_and_verify_acca_notification_message_displaying(self):
        """
        DESCRIPTION: Login to application and verify ACCA Notification message displaying
        EXPECTED: ACCA Notification message is displayed for user after login
        """
        self.site.login(username=tests.settings.freebet_user)
        self.site.open_betslip()
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER)
