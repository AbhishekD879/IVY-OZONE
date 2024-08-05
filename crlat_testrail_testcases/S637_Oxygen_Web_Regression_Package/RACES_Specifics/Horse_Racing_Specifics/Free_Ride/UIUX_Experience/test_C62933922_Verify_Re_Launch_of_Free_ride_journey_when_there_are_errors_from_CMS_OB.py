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
class Test_C62933922_Verify_Re_Launch_of_Free_ride_journey_when_there_are_errors_from_CMS_OB(Common):
    """
    TR_ID: C62933922
    NAME: Verify Re-Launch of Free ride journey when there are errors from CMS/OB
    DESCRIPTION: This test case verifies  Re-Launch of Free ride journey when there are errors from CMS/OB
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

    def test_003_verify_the_display_of_summary_message_and_automated_betslip(self):
        """
        DESCRIPTION: Verify the display of summary message and Automated Betslip
        EXPECTED: * Summary message should not be displayed in Free Ride overlay
        EXPECTED: * Automated Betslip should not be displayed in free Ride overlay and My Bets page
        """
        pass

    def test_004_navigate_to_home_page_and_click_on_free_ride_launch_banner(self):
        """
        DESCRIPTION: Navigate to Home page and click on 'Free Ride Launch Banner'
        EXPECTED: Splash page with CTA button should be displayed
        """
        pass

    def test_005_click_on_cta_button_in_splash_page_and_verify_display_of_welcome_message(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page and verify display of welcome Message
        EXPECTED: * Free Ride overlay should be displayed
        EXPECTED: * welcome Message should be displayed in Free Ride Overlay screen
        EXPECTED: Note:
        EXPECTED: 'welcome message' should be displayed as per Welcome Message' field in Questions section in campaign (CMS)
        """
        pass

    def test_006_verify_display_of_question_and_answer_options_for_first_question(self):
        """
        DESCRIPTION: Verify display of Question and Answer Options for First Question
        EXPECTED: * First Question should be displayed in Free Ride Overlay screen
        EXPECTED: * Answer Options should be displayed below to Step 1 of 3 as below
        EXPECTED: Top Player
        EXPECTED: Dark Horse
        EXPECTED: Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        pass

    def test_007_select_answer_for_first_question_and_verifydisplay_of_question_and_answer_options_for_second_question(self):
        """
        DESCRIPTION: Select Answer for First question and verify display of Question and Answer Options for Second Question
        EXPECTED: * Selected Answer should be displayed below to Step 1 of 3 for First question
        EXPECTED: * Second Question should be displayed in Free Ride Overlay screen
        EXPECTED: * Answer Options should be displayed below to Step 2 of 3 as below
        EXPECTED: Big & Strong
        EXPECTED: Small & Nimble
        EXPECTED: Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        pass

    def test_008_select_answer_for_second_question_and_verify_display_of_question_and_answer_options_for_third_question(self):
        """
        DESCRIPTION: Select Answer for Second question and verify display of Question and Answer Options for Third Question
        EXPECTED: * Selected Answer should be displayed below to Step 2 of 3 for second question
        EXPECTED: * Third Question should be displayed in Free Ride Overlay screen
        EXPECTED: * Answer Options should be displayed below to Step 3 of 3 as below
        EXPECTED: Good Chance
        EXPECTED: Nice price
        EXPECTED: Surprise Me!
        EXPECTED: Note: 3 options are configured in CMS
        """
        pass

    def test_009_select_answer_for_third_question(self):
        """
        DESCRIPTION: Select Answer for Third Question
        EXPECTED: Selected answer should be displayed
        """
        pass

    def test_010_verify_the_display_of_summary_message_and_automated_betslip(self):
        """
        DESCRIPTION: Verify the display of Summary message and Automated Betslip
        EXPECTED: * Summary message should be displayed
        EXPECTED: * Automated Betslip should be generated successfully
        """
        pass
