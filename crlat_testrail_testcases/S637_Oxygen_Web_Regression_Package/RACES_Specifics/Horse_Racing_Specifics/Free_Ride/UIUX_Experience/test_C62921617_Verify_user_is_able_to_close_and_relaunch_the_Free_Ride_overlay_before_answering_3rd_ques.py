import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62921617_Verify_user_is_able_to_close_and_relaunch_the_Free_Ride_overlay_before_answering_3rd_ques(Common):
    """
    TR_ID: C62921617
    NAME: Verify user is able to close and relaunch the Free Ride overlay before answering 3rd ques
    DESCRIPTION: This test case verifies user is able to close and relaunch the Free Ride overlay before answering 3rd ques
    PRECONDITIONS: Campaign should be created and questions are configured in cms
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully and Free Ride Banner should be displayed
        """
        pass

    def test_002_click_on_launch_free_ride_banner_in_homepage(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner' in Homepage
        EXPECTED: * Splash page with CTA button should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        pass

    def test_003_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        pass

    def test_004_repeat_step2_and_click_on_cta_button_in_splash_page(self):
        """
        DESCRIPTION: Repeat step2 and Click on CTA button in Splash Page
        EXPECTED: * Free Ride overlay with Welcome message should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        pass

    def test_005_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        pass

    def test_006_repeat_step_4_and_select_answer_option_for_question1(self):
        """
        DESCRIPTION: Repeat step 4 and select answer option for question1
        EXPECTED: * Selected answer option should be highlighted in Red color in First question answer page
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        pass

    def test_007_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        pass

    def test_008_repeat_step_6_and_wait_for_chat_box_response_for_question1(self):
        """
        DESCRIPTION: Repeat step 6 and wait for chat box response for question1
        EXPECTED: * Chat box response for question1 should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        pass

    def test_009_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        pass

    def test_010_repeat_steps_6_9_for_question2(self):
        """
        DESCRIPTION: Repeat steps 6-9 for question2
        EXPECTED: 
        """
        pass

    def test_011_repeat_step4_and_select_answer_options_for_question12(self):
        """
        DESCRIPTION: Repeat step4 and select answer options for question1,2
        EXPECTED: * Free Ride overlay with question3 page should be displayed
        EXPECTED: * close button (X on the top right side) should be displayed
        """
        pass

    def test_012_click_close_button_x_on_the_top_right_side(self):
        """
        DESCRIPTION: Click close button (X on the top right side)
        EXPECTED: Free Ride overlay should be closed
        """
        pass

    def test_013_repeat_step2(self):
        """
        DESCRIPTION: Repeat step2
        EXPECTED: 
        """
        pass
