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
class Test_C62978469_Verify_CMS_configurations_for_Question_tab_in_campaign_page(Common):
    """
    TR_ID: C62978469
    NAME: Verify CMS configurations for Question tab in campaign page
    DESCRIPTION: This test case verifies the CMS configurations for Question tab in campaign page
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

    def test_002_enter_the_data_andclick_on_create_campaign(self):
        """
        DESCRIPTION: Enter the data and Click on Create Campaign
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

    def test_005_enter_the_data(self):
        """
        DESCRIPTION: Enter the data
        EXPECTED: User should be able to enter the data in all the field
        """
        pass

    def test_006_click_on_save(self):
        """
        DESCRIPTION: Click on save
        EXPECTED: User should be able to save the data successfully
        """
        pass
