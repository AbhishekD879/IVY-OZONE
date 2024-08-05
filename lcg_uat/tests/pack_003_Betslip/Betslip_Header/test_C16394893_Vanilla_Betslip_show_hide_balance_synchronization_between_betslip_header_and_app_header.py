import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C16394893_Vanilla_Betslip_show_hide_balance_synchronization_between_betslip_header_and_app_header(BaseBetSlipTest):
    """
    TR_ID: C16394893
    VOL_ID: C24641831
    NAME: [Vanilla] Betslip: show/hide balance synchronization between betslip header and app header
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies synchronization of show/hide balance functionality between betslip header and app header
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have some selections added to betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login into app
        DESCRIPTION: Add two selections to betslip
        EXPECTED: User is logged in
        EXPECTED: Two selections are added to betslip
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            for market in event['event']['children']:
                if market['market']['name'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_resp if
                                 'Unnamed' not in i['outcome']['name']}
            selection_ids = list(all_selection_ids.values())[:2]
            self._logger.debug(f'Horseracing event with selection ids:"{selection_ids}"')
        else:
            event_parameters = self.ob_config.add_UK_racing_event(number_of_runners=2)
            selection_ids = list(event_parameters.selection_ids.values())

        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.get_betslip_content().close_button.click()

    def test_001_verify_displaying_of_user_balance_on__app_header__betslip_header(self):
        """
        DESCRIPTION: Verify displaying of user balance on:
        DESCRIPTION: - App header
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed on:
        EXPECTED: - App header
        EXPECTED: - Betslip header
        """
        user_balance = self.site.header.user_balance
        self.assertTrue(user_balance, msg='App header does not containe user balance')
        self.site.open_betslip()
        self.assertTrue(self.get_betslip_content().header.user_balance_amount,
                        msg='Betslip header does not contain balance information, but was expected to contain')

    def test_002_1_open_betslip_tap_account_balance_area__hide_balance_button2_verify_displaying_of_user_balance_on__betslip_header(self):
        """
        DESCRIPTION: 1) Open betslip, tap 'Account Balance' area > 'Hide Balance' button
        DESCRIPTION: 2) Verify displaying of user balance on:
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed as 'Balance' word
        """
        self.get_betslip_content().hide_balance_option.click()

        result = wait_for_result(lambda: self.get_betslip_content().header.user_balance_amount == vec.betslip.BALANCE,
                                 name='Wait for header title to change',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'User balance is not displayed as "{vec.betslip.BALANCE}" word. '
                        f'Actual: "{self.get_betslip_content().header.user_balance_amount}"')
