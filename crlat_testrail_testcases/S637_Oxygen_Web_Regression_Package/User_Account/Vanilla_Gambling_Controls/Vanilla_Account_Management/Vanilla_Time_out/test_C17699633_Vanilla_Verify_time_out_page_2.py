import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C17699633_Vanilla_Verify_time_out_page_2(Common):
    """
    TR_ID: C17699633
    NAME: [Vanilla] Verify time-out page 2
    DESCRIPTION: This test case verifies the 2nd page of time-out
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure & Reopening
    PRECONDITIONS: User selects the third option - 'I’d like to take an irreversible time-out or exclude myself from gaming', selects the time-out period and the reason of closure (**remember selected date**)
    """
    keep_browser_open = True

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: The confirmation screen of time-out is displayed:
        EXPECTED: - the title of the page is 'Take a short time-out',
        EXPECTED: - date and time of the end of time-out,
        EXPECTED: - consequences of a time-out,
        EXPECTED: - information what would happen after confirmation,
        EXPECTED: - "Take a short time-out" button,
        EXPECTED: - "Cancel" button
        """
        pass

    def test_002_validate_date_and_time_of_time_out(self):
        """
        DESCRIPTION: Validate date and time of time-out
        EXPECTED: Date and time is the same as the one selected as duration
        """
        pass
