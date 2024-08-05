import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.currency
@pytest.mark.login
@pytest.mark.medium
@vtest
class Test_C29155_Verify_ACCA_Suggested_Notification_Displaying_For_Logged_In_User(BaseBetSlipTest):
    """
    TR_ID: C29155
    NAME: Verify ACCA Suggested Notification displaying for logged in user
    DESCRIPTION: This test case verifies Super ACCA Notification message is displayed for logged in user
    """
    keep_browser_open = True
    selection_ids_2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        selection_ids_1 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        selection_ids_2 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        selection_ids_3 = self.ob_config.add_autotest_premier_league_football_event().selection_ids

        self.__class__.selection_ids = (list(selection_ids_1.values())[0],
                                        list(selection_ids_2.values())[0],
                                        list(selection_ids_3.values())[0])

        self.__class__.selection_ids_2 = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_login_with_user_who_use_gbp_currency(self):
        """
        DESCRIPTION: Login with user who use GBP currency
        EXPECTED: User successfully logged in
        """
        self.site.login(username=tests.settings.freebet_user)

    def test_002_add_at_least_three_selections_to_betslip_that_are_applicable_for_acca_insurance(self):
        """
        DESCRIPTION: Add at least three selections to Betslip that are applicable for ACCA Insurance
        EXPECTED: ACCA Offer is received from Open Bet for the user
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_003_verify_acca_notification_message_displaying_in_betslip_for_appropriate_multiple(self):
        """
        DESCRIPTION: Verify ACCA Notification message displaying in Betslip for appropriate Multiple
        EXPECTED: ACCA Notification message is displayed for the user with next elements:
        EXPECTED: * number of extra selections required in order for User to trigger the Acca offer
        EXPECTED: * available Bonus amount
        EXPECTED: * maximum lose legs that the user will benefit from with the offer
        """
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER)

    def test_004_add_one_more_selection_with_applicable_acca_insurance_and_verify_message_content_update(self):
        """
        DESCRIPTION: Add one more selection with applicable ACCA Insurance and verify message content update
        EXPECTED: Number of extra selections required for Acca Offer is appropriately decreased of 1 in the message
        EXPECTED: Number of extra selections is updated in real time without page refresh
        """
        self.__class__.selection_name, selection_id = list(self.selection_ids_2.items())[0]
        self.open_betslip_with_selections(selection_ids=selection_id)

        self.check_acca_offer_for_stake(stake_name=vec.betslip.ACC4,
                                        offer_type=self.cms_config.constants.ACCA_ELIGIBLE_INSURANCE_OFFER)

    def test_005_remove_selection_with_applicable_acca_offer_from_the_betslip_and_verify_message_content_update(self):
        """
        DESCRIPTION: Remove selection with applicable Acca Offer from the Betslip and verify message content update
        EXPECTED: Number of extra selections required for Acca Offer is appropriately increased of 1 in the message
        EXPECTED: Number of extra selections is updated in real time without page refresh
        """
        self.remove_stake(name=self.selection_name)
        self.check_acca_offer_for_stake(stake_name=vec.betslip.TBL,
                                        offer_type=self.cms_config.constants.ACCA_SUGGESTED_INSURANCE_OFFER)
