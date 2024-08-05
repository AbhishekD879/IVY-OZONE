import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870143_Verify_account_closure_Verify_user_can_navigate_to_Responsible_Gambling_https_responsiblegamblingcoralcouk_Verify_details_for_Account_Closure_and_close_the_account_Verify_user_cant_login_to_sports_site_after_account_closure(Common):
    """
    TR_ID: C44870143
    NAME: "Verify account closure, Verify user can navigate to 'Responsible Gambling' https://responsiblegambling.coral.co.uk/ Verify details for 'Account Closure' and close the account. Verify user can't login to sports site after account closure."
    DESCRIPTION: "Verify account closure,
    DESCRIPTION: Verify user can navigate to 'Responsible Gambling' https://responsiblegambling.coral.co.uk/
    DESCRIPTION: Verify details for 'Account Closure' and close the account.
    DESCRIPTION: Verify user can't login to sports site after account closure."
    PRECONDITIONS: Load app and log in
    PRECONDITIONS: Navigate to Right Menu -> select Gambling Controls
    PRECONDITIONS: Tap/click 'Account Closure & Reopening' twistee
    PRECONDITIONS: Tap on Choose
    PRECONDITIONS: User is taken to Account Closure & Reopening page
    """
    keep_browser_open = True

    def test_001_on_account_closure__reopeningstep_1_page_is_opened_with_options_to_choose_and_continue_button_is_disabled(self):
        """
        DESCRIPTION: On 'Account Closure & Reopening'
        DESCRIPTION: Step 1 page is opened with options to choose and CONTINUE button is disabled
        EXPECTED: Option is selected and displayed within 'Closure Reason'
        EXPECTED: 'CONTINUE' button becomes enabled
        """
        pass

    def test_002_tap_continue(self):
        """
        DESCRIPTION: Tap CONTINUE
        EXPECTED: Options to CLOSE
        EXPECTED: Bingo/Casino/Poker & Sports are available.
        """
        pass

    def test_003_choose_any_options_or_close_all_the_accounts(self):
        """
        DESCRIPTION: Choose any options or Close All the accounts
        EXPECTED: Next page shows the user about the selection for the products to be closed with Consequences and Reopening along with options to choose DURATION & REASON FOR CLOSURE
        EXPECTED: with  CONTINUE button disabled.
        """
        pass

    def test_004_chose_any_options_for_duration__reason_for_closure_and_then_click_continue_button_becomes_enabled(self):
        """
        DESCRIPTION: Chose any options for DURATION & REASON FOR CLOSURE and then click 'CONTINUE' (button becomes enabled)
        EXPECTED: Pop up displayed with the following message:
        EXPECTED: Successfully closed: Bingo,Casino,Poker & Sports message is shown
        EXPECTED: Note: The user can still navigate within the app but will not be able to place bets.
        """
        pass
