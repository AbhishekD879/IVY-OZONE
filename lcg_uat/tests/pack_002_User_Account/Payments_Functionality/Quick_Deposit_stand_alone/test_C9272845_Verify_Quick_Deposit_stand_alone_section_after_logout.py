import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C9272845_Verify_Quick_Deposit_stand_alone_section_after_logout(BaseBetSlipTest):
    """
    TR_ID: C9272845
    NAME: Verify 'Quick Deposit' stand alone section after logout
    DESCRIPTION: This test case verifies 'Quick Deposit' stand alone section after logout
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C24102243]
    PRECONDITIONS: 1. App is loaded;
    PRECONDITIONS: 2. User has credit cards added to his account;
    PRECONDITIONS: 3. User is logged in;
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    PRECONDITIONS: 5. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: - Log in to one browser tab;
    PRECONDITIONS: - Duplicate tab;
    PRECONDITIONS: - Log out from the second tab -> session is over in both tabs.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. App is loaded;
        PRECONDITIONS: 2. User has credit cards added to his account;
        PRECONDITIONS: 3. User is logged in;
        PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
        PRECONDITIONS: 5. In order to trigger case when the session is over, perform the next steps:
        PRECONDITIONS: - Log in to one browser tab;
        PRECONDITIONS: - Duplicate tab;
        PRECONDITIONS: - Log out from the second tab -> session is over in both tabs.
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next((market['market']['children'] for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = [i['outcome']['id'] for i in outcomes]
        else:
            selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

        self.site.login(username=tests.settings.quick_deposit_user)
        self.open_betslip_with_selections(selection_ids=selection_ids[0])
        user_balance = self.site.header.user_balance
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = user_balance + 5
        if int(user_balance):
            self.site.betslip.make_quick_deposit_button.click()
        if self.device_type == 'mobile':
            if not self.get_betslip_content().has_deposit_form():
                self.site.close_betslip()
                self.site.wait_content_state_changed(10)
                self.site.open_betslip()

        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=15)
        self.assertTrue(result, msg='Quick Deposit is not displayed')

        self.device.open_new_tab()
        self.device.navigate_to(url=tests.HOSTNAME + '?automationtest=true&q=1')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(timeout=10), msg='User was not logged in')
        try:
            self.site.logout()
        except VoltronException:
            login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
            self.assertTrue(login_dialog, msg='User was not logged out')

    def test_001_follow_step_4_from_preconditions(self):
        """
        DESCRIPTION: Follow step 4 from Preconditions
        EXPECTED: User session is over
        """
        self.assertFalse(self.site.wait_logged_in(timeout=5), msg='User is still "logged in" in the new tab ')
        self.device.open_tab(tab_index=0)
        self.assertFalse(self.site.wait_logged_in(timeout=5), msg='User is still "logged in" in the old tab ')

    def test_002_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' section
        EXPECTED: - Quick Deposit section is NOT displayed anymore
        EXPECTED: - 'Log out' pop up is displayed
        """
        try:
            self.get_betslip_content().has_deposit_form()
            self.assertTrue(False, msg='Quick Deposit pop up was not closed')
        except VoltronException:
            self._logger.info('Quick Deposit pop up was closed')
        login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(login_dialog, msg='Log out pop up is not displayed')
