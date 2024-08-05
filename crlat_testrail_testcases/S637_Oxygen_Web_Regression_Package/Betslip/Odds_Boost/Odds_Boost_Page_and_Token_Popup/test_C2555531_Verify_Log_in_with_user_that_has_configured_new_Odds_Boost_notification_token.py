import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2555531_Verify_Log_in_with_user_that_has_configured_new_Odds_Boost_notification_token(Common):
    """
    TR_ID: C2555531
    NAME: Verify Log in with user that has configured new Odds Boost notification token
    DESCRIPTION: This test case verifies Log in with user that has configured new Odds Boost notification token
    PRECONDITIONS: Enable "Odds Boost" Feature Toggle in CMS
    PRECONDITIONS: Generate for user Odds boost token in TST2 Backoffice
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 'Allow User To Toggle Visibility option' is enabled in CMS > Odds Boost
    PRECONDITIONS: User has a new Odds Boosts token. Token is NOT expired
    """
    keep_browser_open = True

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: * User is logged in successfully
        EXPECTED: * The "Odds Boost" token notification is displayed
        """
        pass

    def test_002_verify_pop_up_dialog_elements(self):
        """
        DESCRIPTION: Verify pop-up dialog elements
        EXPECTED: It should contain the following information:
        EXPECTED: - Hardcoded image (odds boost logo)
        EXPECTED: - Static header text: 'Odds Boost'
        EXPECTED: - Hardcoded content text: 'You Have X Odds Boosts Available' (X is a value specific to the user as fetched on login)
        EXPECTED: - Hardcoded compliance text: '18+. Terms Apply'
        EXPECTED: - 'SHOW MORE' button
        EXPECTED: - 'OK, THANKS' close button
        EXPECTED: - 'X' close button
        EXPECTED: - Check-box - "Don’t show this again"
        EXPECTED: (updated for OX 105 design)
        EXPECTED: ![](index.php?/attachments/get/115670351)
        EXPECTED: ![](index.php?/attachments/get/115670352)
        """
        pass

    def test_003_tap_x_button_on_the_notification_or_ok_thanks_button_or_tap_outside_the_content_odds_boost_notification_area(self):
        """
        DESCRIPTION: Tap "X" button on the notification (or "OK THANKS" button, or tap outside the content "Odds Boost" notification area)
        EXPECTED: * The pop up is closed
        EXPECTED: * The respective underlying page is displayed
        EXPECTED: * Odds Boost token with added offer ID is saved in Local Storage (Developer Tools -&gt; Application -&gt; Local Storage -&gt; OX.oddsBoost)
        """
        pass

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        pass

    def test_005__clear_storage_dev_tools__gt_application__gt_clear_storage_repeat_steps_1_2(self):
        """
        DESCRIPTION: * Clear Storage (Dev Tools -&gt; Application -&gt; Clear storage)
        DESCRIPTION: * Repeat Steps 1-2
        EXPECTED: Results are the same
        """
        pass

    def test_006_tap_show_more_button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE' button
        EXPECTED: * The pop-up is closed
        EXPECTED: * The user is navigated to odds boost page
        """
        pass
