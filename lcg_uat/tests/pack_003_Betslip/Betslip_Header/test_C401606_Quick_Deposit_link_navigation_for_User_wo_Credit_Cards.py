import pytest

import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.creditcard
@pytest.mark.mobile_only
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C401606_Quick_Deposit_link_navigation_for_User_wo_Credit_Cards(BaseBetSlipTest):
    """
    TR_ID: C401606
    VOL_ID: C9698288
    NAME: 'Quick Deposit' link Navigation User w/o Credit Cards
    DESCRIPTION: This test case verifies whether 'Quick Deposit' link in the Betslip header navigates a user, with no registered credit cards, to Deposit page > My Payments tab
    PRECONDITIONS: Make sure you have:
    PRECONDITIONS: - User account with no added payment methods
    PRECONDITIONS: - User account with added PayPall/NETELLER payment methods
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Invictus application, create event
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        number_of_events=1)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1, self.__class__.selection_id = list(selection_ids.items())[0]
            self._logger.debug(
                f'*** Football event id "{event["event"]["id"]}" with selection ids "{self.selection_ids}" and team "{self.team1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_id = event_params.team1, event_params.selection_ids.get(event_params.team1)

    def test_001_log_in_with_account_with_no_added_payment_methods(self):
        """
        DESCRIPTION: Log in with **account with no added payment methods**
        EXPECTED: User is successfully logged in
        """
        self.site.login(username=tests.settings.deposit_page_users)

    def test_002_add_a_selection_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add a selection to the Betslip -> Open Betslip
        EXPECTED: Selection is displayed within Betslip
        EXPECTED: 'Quick Deposit' section is not available
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='Deposit section is visible!')

    def test_003_tap_on_quick_deposit_link(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' link
        EXPECTED: User is navigated to Deposit page > My Payments tab
        """
        is_beta_environment = 'beta' in self.device.get_current_url().split("sports", 1)[0]
        expected_url = self.device.get_current_url().split(".com", 1)[0].replace('https://', '')
        self.get_betslip_content().quick_deposit_link.click()
        wait_for_result(lambda: self.site.select_deposit_method.is_displayed(),
                        name='Deposit Method',
                        timeout=5)
        self.assertTrue(self.site.select_deposit_method.is_displayed(), msg='User is not navigated to the deposit page')
        wait_for_result(lambda: self.site.select_deposit_method.close_button.is_displayed(),
                        name='Deposit Method close button',
                        timeout=5)
        self.site.select_deposit_method.close_button.click()
        actual_url = self.device.get_current_url().split(".com", 1)[0].replace('https://', '')
        if is_beta_environment and 'beta' not in self.device.get_current_url().split("sports", 1)[0]:
            self.assertTrue(actual_url in expected_url, msg='close button is getting re-directed to unexpected page')
            self.navigate_to_page('/')
        '''
        if this TC is running for beta/lower environments, and when close the deposit method page
        it will redirects us to production environment. which is expected.
        So in the above step we are navigating back to the environment this TC was running on.
        '''
        self.site.wait_content_state(state_name='Homepage')

    def test_004_logout(self):
        """
        DESCRIPTION: Logout
        """
        self.site.logout()
