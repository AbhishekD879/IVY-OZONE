import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from datetime import datetime
from datetime import timedelta
from time import sleep


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod  # no possibility to grant freebet on PROD/HL
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C29112_Verify_Notification_On_Betslip(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C29112
    NAME: Verify Notification On Betslip
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has not Free Bets available on their account
    PRECONDITIONS: JIRA Ticket: BMA-10056 Display Notification On Betslip
    """
    keep_browser_open = True
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Login as a user without freebets available
        EXPECTED: Homepage is opened
        EXPECTED: User is logged in
        EXPECTED: 'Freebet' notification icon is not displayed on the header (on the Balance button)
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username)

        self.assertFalse(self.site.header.has_freebets(expected_result=False),
                         msg='Freebet icon is shown for new user')

    def test_002_apply_freebet_tokens_to_the_relevant_user_account(self):
        """
        DESCRIPTION: Apply Freebet tokens to the relevant user account
        """
        self.ob_config.grant_freebet(username=self.username)

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Page is reloaded
        EXPECTED: 'Freebet' notification icon is displayed on the header
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.header.has_freebets(), msg='Freebet icon is not shown')

    def test_004_place_a_bet_using_last_freebet(self):
        """
        DESCRIPTION: Place a bet using last Freebet
        EXPECTED: 'Freebet' notification disappeared from the header (from the Balance button)
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()
        self.assertFalse(self.site.header.has_freebets(expected_result=False), msg='Freebet icon is shown')
        self.site.bet_receipt.close_button.click()

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Apply Freebet tokens to the relevant user account
        EXPECTED: Freebet is added
        """
        exp_date = datetime.utcnow() + timedelta(seconds=5)
        self.ob_config.grant_freebet(username=self.username, level='event', id=self.eventID, expiration_date=exp_date)

    def test_006_expiration_date_and_time_of_available_freebet_has_passes(self):
        """
        DESCRIPTION: Expiration date and time of available Freebet has passes
        EXPECTED: User's freebet is expired after 5 seconds
        """
        self._logger.info('*** Waiting 5 seconds for Freebet expiry')
        sleep(5)

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Freebet' notification icon is disappeared
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertFalse(self.site.header.has_freebets(expected_result=False), msg='Freebet icon is shown after expiry of Freebet')

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Apply Freebet tokens to the relevant user account
        EXPECTED: Freebet is added
        """
        self.ob_config.grant_freebet(username=self.username)
        self.test_003_refresh_the_page()

    def test_009_log_out_from_the_oxygen_application(self):
        """
        DESCRIPTION: Log out from the Oxygen application
        EXPECTED: 'Freebet' notification icon is hidden
        """
        self.site.logout()
        self.assertFalse(self.site.header.has_freebets(expected_result=False), msg='Freebet icon is shown after logout')
