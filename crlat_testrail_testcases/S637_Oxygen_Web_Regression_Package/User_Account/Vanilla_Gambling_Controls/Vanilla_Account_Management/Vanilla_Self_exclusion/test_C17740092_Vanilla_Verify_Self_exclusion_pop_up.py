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
class Test_C17740092_Vanilla_Verify_Self_exclusion_pop_up(Common):
    """
    TR_ID: C17740092
    NAME: [Vanilla] Verify Self-exclusion pop-up
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration, the reason and proceeds to the next page (**remember the selected duration**)
    PRECONDITIONS: User enters the correct password
    """
    keep_browser_open = True

    def test_001_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self exclude' button
        EXPECTED: Self Exclusion pop-up appears with 2 tickboxes:
        EXPECTED: - confirmation of self-exclusion until selected time and no possibilities of accessing/reactivation account before that time,
        EXPECTED: - confirmation of understanding that it won't be possible to open new accounts during this period
        EXPECTED: - 'No' button is present
        EXPECTED: - 'Yes' button is present
        EXPECTED: ![](index.php?/attachments/get/35871)
        """
        pass

    def test_002_verify_self_exclusion_time(self):
        """
        DESCRIPTION: Verify self-exclusion time
        EXPECTED: Date is the same as the one selected as self-exclusion duration
        """
        pass

    def test_003_verify_yes_button(self):
        """
        DESCRIPTION: Verify 'YES' button
        EXPECTED: 'YES' button is disabled
        """
        pass

    def test_004_check_one_tickbox(self):
        """
        DESCRIPTION: Check one tickbox
        EXPECTED: 'YES' button is disabled
        """
        pass

    def test_005_check_the_second_tickbox(self):
        """
        DESCRIPTION: Check the second tickbox
        EXPECTED: 'YES' button is enabled
        """
        pass

    def test_006_click_the_no_button(self):
        """
        DESCRIPTION: Click the 'NO' button
        EXPECTED: Pop-up closes.
        EXPECTED: User stays on 'Self-exclusion' page
        """
        pass
