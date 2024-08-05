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
class Test_C63574481_Verify_message_on_Betslip_when_user_is_on_24_Hr_Break(Common):
    """
    TR_ID: C63574481
    NAME: Verify  message on Betslip when user is on 24 Hr Break
    DESCRIPTION: This Test case verifies the message on Betslip when User is on Immediate 24 Hr Break
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

    def test_004_in_the_same_session_navigate_to_bet_slip_by_adding_any_one_or_more_selection(self):
        """
        DESCRIPTION: In the same session Navigate to Bet slip by adding any ONE or More selection
        EXPECTED: User should be displayed message that his account is temporarily suspended
        EXPECTED: Message should be displayed as configured in CMS
        """
        pass

    def test_005_validate_the_display_of_place_bet__stake_field(self):
        """
        DESCRIPTION: Validate the display of Place Bet & Stake Field
        EXPECTED: Place Bet should be disabled
        EXPECTED: Stake field should be disabled
        """
        pass
