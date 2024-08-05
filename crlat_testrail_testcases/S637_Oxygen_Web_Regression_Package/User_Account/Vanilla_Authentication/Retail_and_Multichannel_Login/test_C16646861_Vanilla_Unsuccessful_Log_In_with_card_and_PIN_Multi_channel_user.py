import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C16646861_Vanilla_Unsuccessful_Log_In_with_card_and_PIN_Multi_channel_user(Common):
    """
    TR_ID: C16646861
    NAME: [Vanilla] Unsuccessful Log In with card and PIN (Multi-channel user)
    DESCRIPTION: This test case verifies UNsuccessful log in with connect card number and PIN
    DESCRIPTION: Note: User is considered as retail user only when he is trying to log in with 16-digit card number and 4-digit PIN, in all other cases when card number <> 16 digits and/or PIN <> 4 digits
    DESCRIPTION: user will be handled as online user that is tryin to log in with username and password
    DESCRIPTION: Following user(ukmigct-tstEUR01/123123) can be used for testing:
    DESCRIPTION: Card: 5544440553493973
    DESCRIPTION: PIN: 1234
    DESCRIPTION: Other users can be found in doc: https://docs.google.com/spreadsheets/d/1VX1aBRgqLmclGxLYm-YcWVazCnODcDdebILKHpNHrI0/edit#gid=1026296319
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_002_do_not_enter_anything(self):
        """
        DESCRIPTION: Do not enter anything.
        EXPECTED: Card number and PIN fields are blank.
        """
        pass

    def test_003_click_log_in_button(self):
        """
        DESCRIPTION: Click LOG IN button.
        EXPECTED: 'Please enter your credentials' error message is displayed.
        EXPECTED: ![](index.php?/attachments/get/34569)
        """
        pass

    def test_004_enter_the_correct_card_number_and_correct_pin_and_click_on_log_in_button(self):
        """
        DESCRIPTION: Enter the correct card number and correct PIN and click on LOG IN button.
        EXPECTED: User should NOT be logged in.
        EXPECTED: "You have upgraded your account. Please use your Username and Password to log in with" Red message should be displayed.
        EXPECTED: ![](index.php?/attachments/get/34570)
        """
        pass
