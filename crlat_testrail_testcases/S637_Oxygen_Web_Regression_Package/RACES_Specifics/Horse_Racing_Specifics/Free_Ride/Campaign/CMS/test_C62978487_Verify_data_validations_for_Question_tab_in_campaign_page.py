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
class Test_C62978487_Verify_data_validations_for_Question_tab_in_campaign_page(Common):
    """
    TR_ID: C62978487
    NAME: Verify data validations for Question tab in campaign page
    DESCRIPTION: This test case verifies data validations for Question tab in campaign page
    PRECONDITIONS: 1: Login to CMS with admin access
    PRECONDITIONS: 2: Click on Free Ride -&gt; campaign
    """
    keep_browser_open = True

    def test_001_click_on_create_campaign_button(self):
        """
        DESCRIPTION: Click on 'Create Campaign' button
        EXPECTED: Campaign page should be displayed with the below fields
        EXPECTED: * *Name
        EXPECTED: * Start date
        EXPECTED: * End date
        EXPECTED: * *Open Bet Campaign Id
        EXPECTED: * *Opti move Id
        """
        pass

    def test_002_enter_the_data_and_click_on_create_campaign(self):
        """
        DESCRIPTION: Enter the data and Click on Create Campaign
        EXPECTED: * Campaign should be created successfully
        EXPECTED: * User should be in campaign details page with all the entered data
        EXPECTED: * Campaign ID should be displayed in the URL
        EXPECTED: * Save, Revert changes and Remove CTAs should be displayed
        EXPECTED: * Save option should be in disabled mode
        """
        pass

    def test_003_verify_display_of_the_tabs(self):
        """
        DESCRIPTION: Verify display of the Tabs
        EXPECTED: * Questions, Horse Selection and Pot Creation Tabs should be displayed
        """
        pass

    def test_004_click_on_question_tab(self):
        """
        DESCRIPTION: Click on Question tab
        EXPECTED: Below fields should be displayed
        EXPECTED: * Questions
        EXPECTED: * Welcome Message
        EXPECTED: * Question1
        EXPECTED: * Answers (Option 1,Option 2 and Option 3)
        EXPECTED: * Chat box Response
        EXPECTED: * Question2
        EXPECTED: * Answers (Option 1,Option 2 and Option 3)
        EXPECTED: * Chat box Response
        EXPECTED: * Question3
        EXPECTED: * Answers (Option 1,Option 2 and Option 3)
        EXPECTED: * Chat box Response
        EXPECTED: * Summary Message
        EXPECTED: * Horse Selection Message
        """
        pass

    def test_005_verify_data_validations_of_the_fields_in_questions_tab(self):
        """
        DESCRIPTION: Verify data validations of the fields in questions tab
        EXPECTED: * Welcome Message - Allows 200 chars
        EXPECTED: * Question1 - Allows 200 chars
        EXPECTED: * Answers (Option 1, 2, 3) - Allows 50 chars
        EXPECTED: * Chat box Response - Allows 200 chars
        EXPECTED: * Question2 - Allows 200 chars
        EXPECTED: * Answers (Option 1, 2, 3) - Allows 50 chars
        EXPECTED: * Chat box Response - Allows 200 chars
        EXPECTED: * Question3 - Allows 200 chars
        EXPECTED: * Answers (Option 1, 2, 3) - Allows 50 chars
        EXPECTED: * Chat box Response - Allows 200 chars
        EXPECTED: * Summary Message - Allows 200 chars
        EXPECTED: * Horse Selection Message - Allows 200 chars
        """
        pass
