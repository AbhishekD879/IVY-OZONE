import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C15306890_Vanilla_Verify_Odd_Boost_pop_up_notification_for_the_user_with_Odds_Boost(Common):
    """
    TR_ID: C15306890
    NAME: [Vanilla] Verify 'Odd Boost' pop-up notification for the user with Odds Boost
    DESCRIPTION: This test case verifies visibility of 'Odd Boost' pop-up notification
    PRECONDITIONS: User has an Odds Boosts token. Token is NOT expired
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        pass

    def test_002_verify_pop_up_dialog_elements(self):
        """
        DESCRIPTION: Verify pop-up dialog elements
        EXPECTED: It should contain the following information:
        EXPECTED: - Hardcoded image (odds boost logo)
        EXPECTED: - Static header text: 'Odds Boost'
        EXPECTED: - Hardcoded content text: 'You have X Odds Boost available' (X is a value specific to the user as fetched on login)
        EXPECTED: - Hardcoded compliance text: '18+. Terms Apply'
        EXPECTED: - 'SHOW MORE' button
        EXPECTED: - 'OK, THANKS' close button
        EXPECTED: - 'X' close button
        EXPECTED: - Checkbox - "Don’t show this again" is displayed if enabled in CMS > Odds Boost
        EXPECTED: ![](index.php?/attachments/get/36667)
        """
        pass

    def test_003_tap_x_button_on_the_notification_or_ok_thanks_button_or_tap_outside_the_content_odds_boost_notification_area(self):
        """
        DESCRIPTION: Tap "X" button on the notification (or "OK THANKS" button, or tap outside the content "Odds Boost" notification area)
        EXPECTED: The pop up is removed from display
        EXPECTED: The respective underlying page is displayed
        """
        pass

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        pass

    def test_005_login_into_application_with_another_user_who_has_an_odds_boosts_token(self):
        """
        DESCRIPTION: Login into application with another user who has an Odds Boosts token
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        pass

    def test_006_tap_show_more_button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE' button
        EXPECTED: The overlay is closed
        EXPECTED: The user is navigated to the hardcoded URL (Odds Boost page) with information about odds boost
        """
        pass
