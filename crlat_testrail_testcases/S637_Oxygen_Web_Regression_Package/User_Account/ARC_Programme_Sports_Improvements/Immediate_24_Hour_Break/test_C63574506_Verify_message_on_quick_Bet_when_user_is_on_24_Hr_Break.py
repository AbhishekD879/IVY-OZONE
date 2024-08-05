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
class Test_C63574506_Verify_message_on_quick_Bet_when_user_is_on_24_Hr_Break(Common):
    """
    TR_ID: C63574506
    NAME: Verify message on quick Bet when user is on 24 Hr Break
    DESCRIPTION: This test case verifies the display of message on quick bet when user is on Immediate 24 Hr Break
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes /Coral
        EXPECTED: User should be successfully logged in
        """
        pass

    def test_002_navigate_to_user_account_gt_gambling_control(self):
        """
        DESCRIPTION: Navigate to User Account &gt; Gambling Control
        EXPECTED: User should be navigated to Gambling Controls page
        """
        pass

    def test_003_click_on_the_immediate_24_hr_break_link(self):
        """
        DESCRIPTION: Click on the Immediate 24 Hr Break link
        EXPECTED: User should be displayed
        EXPECTED: "Your account has now been put on Time Out for the next 24 hours"
        EXPECTED: message
        """
        pass

    def test_004_only_mobilein_the_same_session_click_on_any_one_of_the_selection_and_validate_quick_bet(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: In the same session Click on ANY ONE of the selection and Validate Quick Bet
        EXPECTED: User should be displayed message that his account is temporarily suspended
        EXPECTED: Message should be displayed as configured in CMS
        """
        pass
