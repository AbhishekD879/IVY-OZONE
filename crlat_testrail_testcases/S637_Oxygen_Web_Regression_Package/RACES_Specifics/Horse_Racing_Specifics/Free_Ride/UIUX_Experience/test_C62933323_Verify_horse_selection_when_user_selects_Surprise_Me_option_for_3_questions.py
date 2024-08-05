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
class Test_C62933323_Verify_horse_selection_when_user_selects_Surprise_Me_option_for_3_questions(Common):
    """
    TR_ID: C62933323
    NAME: Verify horse selection, when user selects 'Surprise Me' option for 3 questions
    DESCRIPTION: This test case verifies horse selection, when user selects 'Surprise Me' option for 3 questions
    PRECONDITIONS: CMS:Below specifics are configured in cms
    PRECONDITIONS: 1.Splash Page
    PRECONDITIONS: 2.Questions and Options(Free Ride -Campaign -&gt;Questions)
    PRECONDITIONS: FE:
    PRECONDITIONS: 1.Eligible user logins to ladbrokes application
    PRECONDITIONS: 2. Click on 'Launch Banner' in Homepage
    PRECONDITIONS: 3. Click on CTA Button in Splash Page
    PRECONDITIONS: 4. User should be on First question as Step 1 of 3 page
    """
    keep_browser_open = True

    def test_001_verify_the_display_of_first_question(self):
        """
        DESCRIPTION: Verify the display of first question
        EXPECTED: User can view the first question with below options
        EXPECTED: 1. Top Player
        EXPECTED: 2. Dark Horse
        EXPECTED: 3. Surprise Me
        """
        pass

    def test_002_select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red.
        """
        pass

    def test_003_verify_the_display_of_second_question(self):
        """
        DESCRIPTION: Verify the display of second question
        EXPECTED: Second Question is displayed with below options
        EXPECTED: 1.Big and Strong
        EXPECTED: 2.Small & Nimble
        EXPECTED: 3. Surprise Me
        """
        pass

    def test_004_select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: Select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red
        """
        pass

    def test_005_verify_the_display_of_third_question(self):
        """
        DESCRIPTION: Verify the display of third question
        EXPECTED: Third Question is displayed with below options
        EXPECTED: 1.Good Chance
        EXPECTED: 2.Nice Price
        EXPECTED: 3. Surprise Me
        """
        pass

    def test_006_select_surprise_me_from_the_options(self):
        """
        DESCRIPTION: Select 'Surprise Me' from the options
        EXPECTED: Selected Option is highlighted in Red
        """
        pass

    def test_007_verify_the_summary_message(self):
        """
        DESCRIPTION: Verify the summary message
        EXPECTED: Summary message is displayed to the user, with below fields
        EXPECTED: Rate: Surprise Me
        EXPECTED: Horse: Surprise Me
        EXPECTED: Odds: Surprise Me
        """
        pass

    def test_008_verify_the_allocated_horse_details_in_cms(self):
        """
        DESCRIPTION: Verify the allocated horse details in cms
        EXPECTED: Allocated horse should be from the below pot - DarkHorse + Small & Nimble+ Nice Price
        """
        pass
