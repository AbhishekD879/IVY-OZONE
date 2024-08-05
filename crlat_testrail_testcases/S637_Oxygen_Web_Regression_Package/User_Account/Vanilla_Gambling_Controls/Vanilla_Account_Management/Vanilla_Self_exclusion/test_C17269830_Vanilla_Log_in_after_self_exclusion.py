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
class Test_C17269830_Vanilla_Log_in_after_self_exclusion(Common):
    """
    TR_ID: C17269830
    NAME: [Vanilla] Log in after self-exclusion
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: Prepare two users:
    PRECONDITIONS: - UK user
    PRECONDITIONS: - non UK user
    PRECONDITIONS: *For both:*
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link, where Self-exclusion option is selected by default and clicks the Choose button
    PRECONDITIONS: User selects the duration and reason of self-exclusion and proceeds by clicking Self Exclude
    PRECONDITIONS: User ticks both ticks on self-exclusion pop-up and proceeds by clicking YES
    PRECONDITIONS: User logs out from the app
    """
    keep_browser_open = True

    def test_001_click_the_login_button(self):
        """
        DESCRIPTION: Click the LOGIN button
        EXPECTED: Login pop-up appears
        """
        pass

    def test_002_log_in_using_credentials_of_self_excluded_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of self-excluded UK user
        EXPECTED: Error message appears on the login pop-up:
        EXPECTED: "Account Inaccessible
        EXPECTED: Your account is locked because you have chosen to self-exclude yourself from our products."
        EXPECTED: ![](index.php?/attachments/get/35867)
        """
        pass

    def test_003_log_in_using_credentials_of_self_excluded_non_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of self-excluded non UK user
        EXPECTED: User is able to log in.
        """
        pass
