import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C62933357_Verify_error_handling_on_Free_Ride_overlay(Common):
    """
    TR_ID: C62933357
    NAME: Verify error handling on Free Ride overlay
    DESCRIPTION: This test case verifies  error handling on Free Ride overlay when there is an error from CMS or OB (Time out or server error) after selecting answers for 3 question
    PRECONDITIONS: 1. 3 questions with Answers(option1,Option2 and Option3) and Summary message are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select answers for First, Second and Third questions
    """
    keep_browser_open = True

    def test_001_verify_the_display_of_third_question_with_selected_option(self):
        """
        DESCRIPTION: Verify the display of Third question with selected option
        EXPECTED: Third question with selected answer should be displayed to the user
        """
        pass

    def test_002_trigger_error_from_cms_or_open_bet_timeout_or_server_failed(self):
        """
        DESCRIPTION: Trigger error from CMS or Open Bet (Timeout or Server failed)
        EXPECTED: Error message should be displayed to the user
        """
        pass

    def test_003_verify_the_display_of_summary_message(self):
        """
        DESCRIPTION: Verify the display of summary message
        EXPECTED: Summary message should not be displayed in Free Ride overlay
        """
        pass

    def test_004_verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of Automated Betslip
        EXPECTED: Automated Betslip should not be displayed in free Ride overlay and My Bets page
        """
        pass
