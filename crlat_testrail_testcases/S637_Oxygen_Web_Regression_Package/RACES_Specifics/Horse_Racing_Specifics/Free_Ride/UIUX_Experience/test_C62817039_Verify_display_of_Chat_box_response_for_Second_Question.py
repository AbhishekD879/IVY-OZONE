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
class Test_C62817039_Verify_display_of_Chat_box_response_for_Second_Question(Common):
    """
    TR_ID: C62817039
    NAME: Verify display of Chat box response for Second Question
    DESCRIPTION: This test case verifies display of Chat box response as per the CMS configurations for Second Question
    PRECONDITIONS: 1. Second question with Answers(option1,Option2 and Option3) are configured in CMS (Free Ride-&gt; campaign -&gt; Questions)
    PRECONDITIONS: 2. Login to Ladbrokes application with eligible customers for Free Ride
    PRECONDITIONS: 3. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 4. Click on CTA Button in Splash Page
    PRECONDITIONS: 5. User should select option for First question
    PRECONDITIONS: 6. User should be on Second question as Step 2 of 3 page
    """
    keep_browser_open = True

    def test_001_verify_the_display_of_second_question_with_3_options(self):
        """
        DESCRIPTION: Verify the display of Second question with 3 options
        EXPECTED: Second question with below 3 answer options should be displayed
        EXPECTED: * Big & Strong
        EXPECTED: * Small & Nimble
        EXPECTED: * Surprise me!
        """
        pass

    def test_002_select_1_option_from_the_above_3_options(self):
        """
        DESCRIPTION: Select 1 option from the above 3 options
        EXPECTED: * Selected option should be highlighted with 'Red color'
        EXPECTED: * Another 2 options should be in disabled mode
        """
        pass

    def test_003_verify_the_display_of_selected_option(self):
        """
        DESCRIPTION: Verify the display of selected option
        EXPECTED: Only selected one option should be displayed to the user
        """
        pass

    def test_004_verify_the_display_of_chat_box_response(self):
        """
        DESCRIPTION: Verify the display of chat box response
        EXPECTED: Chat box response should be displayed as per the CMS configurations from 'Chat box Q2 response' field
        """
        pass

    def test_005_verify_the_ui_experience_of_chat_box(self):
        """
        DESCRIPTION: Verify the UI experience of chat box
        EXPECTED: Interactive chat bot session should be displayed as per Zeplin
        """
        pass
