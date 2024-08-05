import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28240_Verify_Hourly_alerts(Common):
    """
    TR_ID: C28240
    NAME: Verify Hourly alerts
    DESCRIPTION: This Test case verifies Hourly alerts.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-3300 (Hourly alerts ("reality checks"))
    DESCRIPTION: *   BMA-6871 LCCP Improvements: Current Hourly Notification - CMS Control
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User Session limit should be Not defined
    PRECONDITIONS: 3. '*Display hourly notification*' setting in CMS -> System Configuration is checked.
    """
    keep_browser_open = True

    def test_001_open_invictus_app(self):
        """
        DESCRIPTION: Open Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_load_application_and_verifyhourly_alert_after_60_min_elapsed(self):
        """
        DESCRIPTION: Load application and verify Hourly alert after 60 min elapsed
        EXPECTED: Hourly alert is appeared with next elements:
        EXPECTED: **Coral** :
        EXPECTED: 1.  'Hourly notification' header
        EXPECTED: 2.  'This is your hourly notification.' body
        EXPECTED: 3.  'Continue' button
        EXPECTED: 4.  'x' icon
        EXPECTED: **Ladbrokes** :
        EXPECTED: 1.  'Hourly notification' header
        EXPECTED: 2.  'This is your hourly notification.' body
        EXPECTED: 3.  'Continue' button
        EXPECTED: ![](index.php?/attachments/get/36355)
        """
        pass

    def test_003_tap_continue_button(self):
        """
        DESCRIPTION: Tap 'Continue' button
        EXPECTED: 1.  Alert is closed
        EXPECTED: 2.  Session timer is not reset
        EXPECTED: 3.  User session is active
        """
        pass

    def test_004_load_application_and_verifyhourly_alert_on_all_pages_after_60_min_elapsed_again(self):
        """
        DESCRIPTION: Load application and verify Hourly alert on All pages after 60 min elapsed again
        EXPECTED: Hourly alert appears on any app page (e.g. Deposit, Betslip, Sportsbook etc.)
        """
        pass

    def test_005_do_not_close_alert_for_few_minutes(self):
        """
        DESCRIPTION: Do not close alert for few minutes
        EXPECTED: Alert is still displayed
        """
        pass

    def test_006_tap_x_icon_for_coral_only(self):
        """
        DESCRIPTION: Tap 'x' icon (for Coral only)
        EXPECTED: 1.  Alert is closed
        EXPECTED: 2.  Session timer is not reset
        EXPECTED: 3.  User session is active
        """
        pass

    def test_007_verify_if_next_hourly_alert_appears_right_after_60_min_after_previous(self):
        """
        DESCRIPTION: Verify if next Hourly alert appears right after 60 min after previous
        EXPECTED: 1.  Hourly alert appears
        EXPECTED: 2.  Hourly alerts will appear each 60 min despite when previous alert was closed
        """
        pass

    def test_008_put_browser_window_with_opened_app_and_opened_hourly_alert_in_background_open_app_again(self):
        """
        DESCRIPTION: Put browser window with opened app and opened Hourly alert in background, open app again
        EXPECTED: 1.  Hourly alert is still opened
        EXPECTED: 2.  Session timer is not reset
        EXPECTED: 3.  User session is active
        """
        pass

    def test_009_do_not_close_hourly_alert_and_wait_60_min_more_then_verify_new_hourly_alert(self):
        """
        DESCRIPTION: Do not close Hourly alert and wait 60 min more then verify new Hourly alert
        EXPECTED: 1.  New hourly alert is shown
        EXPECTED: 2.  Previous Hourly alert is not displayed anymore
        """
        pass
