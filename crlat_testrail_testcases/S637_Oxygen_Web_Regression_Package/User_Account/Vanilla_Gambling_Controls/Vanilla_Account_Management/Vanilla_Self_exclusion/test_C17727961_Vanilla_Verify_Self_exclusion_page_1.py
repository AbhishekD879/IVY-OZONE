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
class Test_C17727961_Vanilla_Verify_Self_exclusion_page_1(Common):
    """
    TR_ID: C17727961
    NAME: [Vanilla] Verify Self-exclusion page 1
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'I'd like to take an irreversible time-out or exclude myself from gaming' option
    """
    keep_browser_open = True

    def test_001_click_the_self_exclusion_link_bottom_of_the_page(self):
        """
        DESCRIPTION: Click the 'Self-exclusion' link (bottom of the page)
        EXPECTED: Gambling Controls page opens.
        EXPECTED: (Self exclusion option selected by default)
        """
        pass

    def test_002_click_the_choose_button(self):
        """
        DESCRIPTION: Click the 'Choose' button
        EXPECTED: User is redirected to the Self-Exclusion page:
        EXPECTED: - title is Self Exclusion,
        EXPECTED: - different self-exclusion periods are provided,
        EXPECTED: - brand selection is provided,
        EXPECTED: - reasons of self exclusion are provided
        EXPECTED: - 'Continue' button is available,
        EXPECTED: - 'Cancel' button is available
        """
        pass

    def test_003_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'Continue' button
        EXPECTED: 'Continue' button is disabled
        """
        pass

    def test_004_select_the_self_exclusion_duration(self):
        """
        DESCRIPTION: Select the self-exclusion duration
        EXPECTED: Duration gets selected.
        EXPECTED: 'Continue' button is disabled.
        """
        pass

    def test_005_select_the_reason(self):
        """
        DESCRIPTION: Select the reason
        EXPECTED: 'Continue' button is enabled.
        """
        pass

    def test_006_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the 'Cancel' button
        EXPECTED: User is redirected to Gambling Controls main page with Deposit Limits option selected by default.
        """
        pass
