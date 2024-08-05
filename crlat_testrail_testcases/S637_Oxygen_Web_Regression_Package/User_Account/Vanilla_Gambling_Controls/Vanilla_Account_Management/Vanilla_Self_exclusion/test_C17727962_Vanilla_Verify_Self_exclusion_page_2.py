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
class Test_C17727962_Vanilla_Verify_Self_exclusion_page_2(Common):
    """
    TR_ID: C17727962
    NAME: [Vanilla] Verify Self-exclusion page 2
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure&Reopening
    PRECONDITIONS: User selects 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration and the reason
    """
    keep_browser_open = True

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: Self-Exclusion page appears:
        EXPECTED: - title is 'Self-Exclusion'
        EXPECTED: - date and time of the end of self-exclusion is provided,
        EXPECTED: - password confirmation field is displayed,
        EXPECTED: - consequences of self-exclusion are provided,
        EXPECTED: - after confirmation info is provided,
        EXPECTED: - 'Self exclude' button is present,
        EXPECTED: - 'Cancel' button is present
        """
        pass

    def test_002_verify_self_exclusion_date(self):
        """
        DESCRIPTION: Verify self exclusion date
        EXPECTED: Date is the same as the one selected as duration
        """
        pass

    def test_003_verify_self_exclude_button(self):
        """
        DESCRIPTION: Verify 'Self exclude' button
        EXPECTED: 'Self exclude' button is disabled
        """
        pass

    def test_004_enter_incorrect_password(self):
        """
        DESCRIPTION: Enter incorrect password
        EXPECTED: 'Self exclude' button is enabled
        """
        pass

    def test_005_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self exclude' button
        EXPECTED: 'Incorrect password' message appears
        """
        pass

    def test_006_enter_correct_password(self):
        """
        DESCRIPTION: Enter correct password
        EXPECTED: 'Self exclude' button is enabled
        """
        pass
