import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.betslip
@vtest
class Test_C11257181_Betslip_displaying_balance_for_logged_out_user(BaseBetSlipTest):
    """
    TR_ID: C11257181
    NAME: Betslip: displaying balance for logged out user
    DESCRIPTION: This test case verifies that balance is not displayed for logged out user
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have some selections added to betslip and betslip should be opened
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections  "{self.selection_ids}"')
            self.__class__.team1_1 = list(self.selection_ids.keys())[0]
        else:
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1_1, self.__class__.selection_ids = event_params1.team1, event_params1.selection_ids

    def test_001_verify_displaying_account_balance_in_the_betslip_header(self):
        """
        DESCRIPTION: Verify displaying account balance in the betslip header
        EXPECTED: Balance is displayed at the top right corner
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1_1])
        self.__class__.betslip = self.get_betslip_content()
        self.assertTrue(self.betslip.header.has_user_balance,
                        msg='Balance is not displayed at the top right corner')

    def test_002___log_out_and_open_betslip__verify_displaying_account_balance_in_the_betslip_header(self):
        """
        DESCRIPTION: - Log out and open betslip
        DESCRIPTION: - Verify displaying account balance in the betslip header
        EXPECTED: Balance is NOT displayed at the top right corner
        """
        self.navigate_to_page("Homepage")
        self.site.logout()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1_1])
        self.assertFalse(self.betslip.header.has_user_balance,
                         msg='Balance is displayed at the top right corner ')
