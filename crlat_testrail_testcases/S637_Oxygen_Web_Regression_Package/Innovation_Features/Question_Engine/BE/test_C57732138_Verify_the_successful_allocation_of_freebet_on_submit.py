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
class Test_C57732138_Verify_the_successful_allocation_of_freebet_on_submit(Common):
    """
    TR_ID: C57732138
    NAME: Verify the successful allocation of freebet on submit
    DESCRIPTION: This test case verifies the successful allocation of freebet on submit.
    PRECONDITIONS: 1. Create a Promotional Opt In trigger regarding the provided instruction https://confluence.egalacoral.com/display/SPI/How+to+setup+and+use+Promotional+Opt+In+trigger
    PRECONDITIONS: 2. The CMS User is logged in.
    PRECONDITIONS: For more information please consider heh provided instructions:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+instantly+assign+free+bets+for+a+user+from+BE
    """
    keep_browser_open = True

    def test_001_navigate_to_the_prizes_tab_of_an_active_quiz(self):
        """
        DESCRIPTION: Navigate to the 'Prizes' tab of an active Quiz.
        EXPECTED: The table of prizes is displayed.
        """
        pass

    def test_002_select_the_token_value_in_the_submit_row(self):
        """
        DESCRIPTION: Select the "Token" value in the 'Submit' row.
        EXPECTED: The "Token" value is displayed as selected in the 'Prize type' column.
        """
        pass

    def test_003_set_a_valid_promotion_id_in_the_promotion_id_field(self):
        """
        DESCRIPTION: Set a valid promotion id in the 'Promotion Id' field.
        EXPECTED: The entered promotion id is displayed in the field.
        """
        pass

    def test_004_click_the_save_changes_button(self):
        """
        DESCRIPTION: Click the 'Save Changes' button.
        EXPECTED: The 'Saving of' pop-up is opened.
        """
        pass

    def test_005_click_the_yes_button(self):
        """
        DESCRIPTION: Click the 'Yes' button.
        EXPECTED: The 'Saving of' pop-up is closed.
        EXPECTED: The 'Quiz Changes Are Saved' message is displayed.
        """
        pass

    def test_006_send_a_post_request_in_postman_to_be_with_the_valid_quizid_questionid_and_answerideg_httpsquestion_engine_dev0coralsportsdevcloudladbrokescoralcomapiv1user_answer_with_bodysourceid_testusername_durnincquizid_5e204001c9e77c0001e73750customerid_12345questionidtoanswerid_32151f9d_1f24_4e45_992c_1e09d2116c8d_791985bc_b854_4bc9_a3ee_e4634ada2fa7(self):
        """
        DESCRIPTION: Send a POST request in Postman to BE with the valid quizId, questionId and answerId.
        DESCRIPTION: (e.g. https://question-engine-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/user-answer with body
        DESCRIPTION: {
        DESCRIPTION: "sourceId": "/test",
        DESCRIPTION: "username": "DURNINC",
        DESCRIPTION: "quizId": "5e204001c9e77c0001e73750",
        DESCRIPTION: "customerId": "12345",
        DESCRIPTION: "questionIdToAnswerId": {
        DESCRIPTION: "32151f9d-1f24-4e45-992c-1e09d2116c8d": ["791985bc-b854-4bc9-a3ee-e4634ada2fa7"]
        DESCRIPTION: }
        DESCRIPTION: }
        DESCRIPTION: )
        EXPECTED: The 201 status code is received.
        """
        pass
