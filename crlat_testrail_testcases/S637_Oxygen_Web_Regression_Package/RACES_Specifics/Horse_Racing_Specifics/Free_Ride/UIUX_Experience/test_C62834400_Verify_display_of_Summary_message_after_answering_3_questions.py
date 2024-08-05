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
class Test_C62834400_Verify_display_of_Summary_message_after_answering_3_questions(Common):
    """
    TR_ID: C62834400
    NAME: Verify display of Summary  message after answering 3 questions
    DESCRIPTION: This test case verifies display of Summary  message after answering 3 questions
    PRECONDITIONS: 1. Third question with Answers(option1,Option2 and Option3) and Summary message are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
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

    def test_002_verify_display_of_summary_message_in_free_ride_overlay(self):
        """
        DESCRIPTION: Verify display of Summary message in Free Ride Overlay
        EXPECTED: Summary message should be displayed as per the CMS configurations from 'Summary Message' field
        """
        pass

    def test_003_verify_the_display_rate_horse_and_odds_fields_along_with_summary_message(self):
        """
        DESCRIPTION: Verify the display Rate, Horse and Odds fields along with summary message
        EXPECTED: Rate, Horse and Odds fields along with summary message should be displayed
        """
        pass

    def test_004_verify_display_of_content_inrate_horse_and_odds_fields(self):
        """
        DESCRIPTION: Verify display of content in Rate, Horse and Odds fields
        EXPECTED: Content in Rate, Horse and Odds fields in free Ride overlay should display as below
        EXPECTED: * Rate: option selected by the user for question1
        EXPECTED: * Horse: option selected by the user for question2
        EXPECTED: * Odds: option selected by the user for question3
        """
        pass
