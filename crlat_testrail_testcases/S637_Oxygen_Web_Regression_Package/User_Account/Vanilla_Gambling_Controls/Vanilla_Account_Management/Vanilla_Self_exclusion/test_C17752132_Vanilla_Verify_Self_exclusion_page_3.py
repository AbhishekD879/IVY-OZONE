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
class Test_C17752132_Vanilla_Verify_Self_exclusion_page_3(Common):
    """
    TR_ID: C17752132
    NAME: [Vanilla] Verify Self-exclusion page 3
    DESCRIPTION: this test case verifies the 3rd self-exclusion page (self-exclusion confirmation)
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration, the reason and proceeds to the next page
    PRECONDITIONS: User enters the correct password and clicks the 'Self Exclude' button
    PRECONDITIONS: User ticks both tickboxes on the self-exclusion confirmation pop-up
    """
    keep_browser_open = True

    def test_001_click_the_yes_button(self):
        """
        DESCRIPTION: Click the 'YES' button
        EXPECTED: Self-exclusion confirmation page appears:
        EXPECTED: - confirmation message is displayed,
        EXPECTED: - the consequences of Self-Exclusion are displayed,
        EXPECTED: - the links to help and contact pages are provided
        """
        pass
