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
class Test_C18258206_Vanilla_Log_in_after_time_out(Common):
    """
    TR_ID: C18258206
    NAME: [Vanilla] Log in after time-out
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: Prepare two users:
    PRECONDITIONS: - UK user
    PRECONDITIONS: - non UK user
    PRECONDITIONS: For both:
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
    PRECONDITIONS: User selects option - 'Id like to take an irreversible time-out or exclude myself from gaming'
    PRECONDITIONS: User selects the duration and reason of time-out and proceeds by clicking Continue (**remember selected date**)
    PRECONDITIONS: User clicks 'Take a short time-out' button
    PRECONDITIONS: User logs out from the app
    """
    keep_browser_open = True

    def test_001_click_the_login_button(self):
        """
        DESCRIPTION: Click the LOGIN button
        EXPECTED: Login pop-up appears
        """
        pass

    def test_002_log_in_using_credentials_of_timed_out_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of timed-out UK user
        EXPECTED: Error message appears on the login pop-up:
        EXPECTED: "Account Inaccessible
        EXPECTED: Your account is currently blocked because you have opted to take a time-out. You will not be able to access your account until <date> <time>"
        EXPECTED: ![](index.php?/attachments/get/35870)
        """
        pass

    def test_003_validate_the_date_and_time_of_time_out(self):
        """
        DESCRIPTION: Validate the date and time of time-out
        EXPECTED: Date and time is the same as the one selected as duration
        """
        pass

    def test_004_log_in_using_credentials_of_timed_out_non_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of timed-out non UK user
        EXPECTED: User is able to log in.
        """
        pass
