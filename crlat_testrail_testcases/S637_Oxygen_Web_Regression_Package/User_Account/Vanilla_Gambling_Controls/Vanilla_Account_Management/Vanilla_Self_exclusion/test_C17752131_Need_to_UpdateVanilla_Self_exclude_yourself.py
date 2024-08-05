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
class Test_C17752131_Need_to_UpdateVanilla_Self_exclude_yourself(Common):
    """
    TR_ID: C17752131
    NAME: [Need to Update][Vanilla] Self-exclude yourself
    DESCRIPTION: This test case verifies self-exclusion feature
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    """
    keep_browser_open = True

    def test_001_navigate_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Navigate to the bottom of the page
        EXPECTED: -
        """
        pass

    def test_002_click_the_self_exclusion_link(self):
        """
        DESCRIPTION: Click the 'Self-exclusion' link
        EXPECTED: User is redirected to Gambling controls page with 'Self Exclusion' option selected by default.
        """
        pass

    def test_003_click_the_choose_button(self):
        """
        DESCRIPTION: Click the 'Choose' button
        EXPECTED: User is redirected to 'Self-Exclusion' page with self-exclusion duration and reason selection.
        """
        pass

    def test_004_select_self_exclusion_duration(self):
        """
        DESCRIPTION: Select self-exclusion duration
        EXPECTED: Duration successfully selected
        """
        pass

    def test_005_select_the_reason(self):
        """
        DESCRIPTION: Select the reason
        EXPECTED: Reason successfully selected
        """
        pass

    def test_006_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: User is redirected to Self-Exclusion password confirmation page.
        """
        pass

    def test_007_enter_correct_password(self):
        """
        DESCRIPTION: Enter correct password
        EXPECTED: Password is successfully entered
        """
        pass

    def test_008_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self Exclude' button
        EXPECTED: Self exclusion confirmation pop-up appears
        """
        pass

    def test_009_tick_both_tickboxes(self):
        """
        DESCRIPTION: Tick both tickboxes
        EXPECTED: Tickboxes successfully ticked
        """
        pass

    def test_010_click_the_yes_button(self):
        """
        DESCRIPTION: Click the 'YES' button
        EXPECTED: User is self-excluded.
        EXPECTED: Self-exclusion confirmation page appears.
        """
        pass
