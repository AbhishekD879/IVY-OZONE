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
class Test_C17338929_Vanilla_Verify_time_out_page_1(Common):
    """
    TR_ID: C17338929
    NAME: [Vanilla] Verify time-out page 1
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls
    """
    keep_browser_open = True

    def test_001_select_account_closure__reopening_option_and_click_the_choose_button(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening' option and click the **CHOOSE** button
        EXPECTED: 'Account Closure & Reopening' page is open
        """
        pass

    def test_002_select_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I'd like to take an irreversible time-out or exclude myself from gaming' option and click 'CONTINUE' button
        EXPECTED: **Take a short time-out** page is displayed:
        EXPECTED: - the duration for time-out is displayed with weeks, months & until options, **TO EDIT** No months option is available
        EXPECTED: - the options to select reason are provided,
        EXPECTED: - link to **Self exclusion** is provided at the bottom of the page,
        EXPECTED: - **Continue** button is provided to proceed with Time out,
        EXPECTED: - **Cancel** button is provided which will cancel the action and take the user back to the Gambling controls page with Deposit Limits option highlighted by default
        """
        pass

    def test_003_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the **CANCEL** button
        EXPECTED: Time-out action is cancelled.
        EXPECTED: The user is redirected back to the **Gambling Controls** page with **Deposit Limits** option highlighted by default.
        """
        pass
