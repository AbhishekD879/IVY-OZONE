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
class Test_C16269002_Vanilla_Successful_Log_In_with_card_and_PIN_InShop_User(Common):
    """
    TR_ID: C16269002
    NAME: [Vanilla] Successful Log In with card and PIN (InShop User)
    DESCRIPTION: This test case verifies successful log in with connect card number and PIN
    DESCRIPTION: Note: User is considered as retail user only when he is trying to log in with 16-digit card number and 4-digit PIN, in all other cases when card number <> 16 digits and/or PIN <> 4 digits
    DESCRIPTION: user will be handled as online user that is tryin to log in with username and password
    DESCRIPTION: [C9689891]
    DESCRIPTION: [C9697992]
    DESCRIPTION: Following user can be used for testing:
    DESCRIPTION: Card: 9000000000468943
    DESCRIPTION: PIN: 1234
    DESCRIPTION: if you need to generate new in-shop account use attached postman collection (run 'get-token' request, then 'Create In-Shop account' where you need to set 'mobile' parameter with random phone number in format 7xxxxxxxxx) (Note: not working for Vanilla, needs investigation)
    PRECONDITIONS: Make sure In-Shop User log In feature is turned on in CMS: System configuration -> Connect -> login
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_002_enter_existing_correct_card_numberindexphpattachmentsget34258the_grid___for_ladbrokesconnect_card_for__coral(self):
        """
        DESCRIPTION: Enter existing correct card number
        DESCRIPTION: ![](index.php?/attachments/get/34258)
        DESCRIPTION: The Grid - for Ladbrokes
        DESCRIPTION: Connect Card for- Coral
        EXPECTED: Card number is displayed
        """
        pass

    def test_003_enter_correct_corresponding_pin_4_digits(self):
        """
        DESCRIPTION: Enter correct corresponding PIN (4 digits)
        EXPECTED: Entered PIN is displayed as ****
        """
        pass

    def test_004_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: * Log in popup is closed
        EXPECTED: * User is logged in successfully
        EXPECTED: * Page from which user made log in is still shown
        """
        pass
