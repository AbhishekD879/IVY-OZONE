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
class Test_C62846792_Verify_display_of_automated_betslip_after_answering_3_questions(Common):
    """
    TR_ID: C62846792
    NAME: Verify display of automated betslip after answering 3 questions
    DESCRIPTION: This test case verifies display of automated betslip after answering 3 questions
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
        EXPECTED: Summary message with Rate, Horse and Odds information should be displayed
        """
        pass

    def test_003_verify_display_of_automated_betslip(self):
        """
        DESCRIPTION: Verify display of automated betslip
        EXPECTED: Automated betslip should be successfully generated in Free Ride Overlay
        """
        pass

    def test_004_verify_the_fields_inautomated_betslip(self):
        """
        DESCRIPTION: Verify the fields in automated betslip
        EXPECTED: Below information should be displayed:
        EXPECTED: * That’s it! We made something for you:
        EXPECTED: * Name of the Horse:
        EXPECTED: * Name of the Jockey
        EXPECTED: * Event Time, Meeting place name
        EXPECTED: * Jockey(kits and crests) logo below to summary details
        EXPECTED: * "CTA TO RACECARD" CTA should be displayed
        """
        pass
