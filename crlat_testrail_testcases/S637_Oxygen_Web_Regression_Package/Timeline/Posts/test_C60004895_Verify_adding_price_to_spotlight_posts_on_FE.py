import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60004895_Verify_adding_price_to_spotlight_posts_on_FE(Common):
    """
    TR_ID: C60004895
    NAME: Verify adding price to spotlight posts on FE
    DESCRIPTION: This test case verifies adding price to spotlight posts
    PRECONDITIONS: "
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Load the CMS and Log in
    PRECONDITIONS: 3.Campaign should be configured / 'Spotlight' Template with 'selectionID' and 'Bet Prompt Header' should be configured
    PRECONDITIONS: 4.Navigate to the 'Timeline' section in the left menu (CMS -> 'Timeline' section -> 'Timeline Campaign' item -> 'Spotlights' button)
    PRECONDITIONS: 5.Insert classIds in the 'Fetch for classIds' field (e.g. 226,223)
    PRECONDITIONS: 6.Click on the 'Refresh Events' button
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_click_on_the_event_time_of_the_one_event(self):
        """
        DESCRIPTION: Click on the event time of the one event
        EXPECTED: Spotlight data is displayed for the selected event time
        """
        pass

    def test_002___click_on_the_create_post_in_spotlight_section___select_spotlight_template_with_configured_selectionid__click_on_the_create_post_button(self):
        """
        DESCRIPTION: - Click on the 'Create Post' in Spotlight section - Select 'Spotlight' template with configured SelectionID
        DESCRIPTION: - Click on the 'Create Post' button
        EXPECTED: - Spotlight Post is displayed with configured information
        EXPECTED: - SelectionID is auto-populated and displayed
        EXPECTED: - 'Price' button is displayed on the Post Preview and it always has general odds '100/1'
        EXPECTED: - Bet Prompt Header is populated and displayed
        """
        pass

    def test_003_click_on_the_create_post_and_publish_buttons(self):
        """
        DESCRIPTION: Click on the 'Create Post' and 'Publish' buttons
        EXPECTED: Spotlight Post is successfully created and published with available Price button
        """
        pass

    def test_004_go_to_the_ui_and_check_the_post(self):
        """
        DESCRIPTION: Go to the UI and check the post
        EXPECTED: - Post is present in the Timeline
        EXPECTED: - Price is present in the post
        EXPECTED: - Bet Prompt Header is present in the post
        EXPECTED: ![](index.php?/attachments/get/120925770)
        """
        pass

    def test_005_click_on_the_price(self):
        """
        DESCRIPTION: Click on the price
        EXPECTED: - Selection is added to QuickBet
        """
        pass

    def test_006_navigate_to_the_cms___template_section___open_spotlight_template___leave_selectionidand_bet_prompt_header_fields_empty_and_save_changes(self):
        """
        DESCRIPTION: Navigate to the CMS -> 'Template' section -> Open 'Spotlight' Template -> leave 'SelectionID'and 'Bet Prompt Header' fields empty and Save Changes
        EXPECTED: Spotlight Template Changes are successfully saved
        """
        pass

    def test_007____go_back_to_configured_post_and_check_the_selectionid_field(self):
        """
        DESCRIPTION: -  Go back to configured post and check the 'SelectionID' field
        EXPECTED: - SelectionID is present
        EXPECTED: - 'Price' button is displayed on the Post Preview
        EXPECTED: - Bet Prompt Header is displayed
        """
        pass

    def test_008_go_to_the_ui_and_check_the_post(self):
        """
        DESCRIPTION: Go to the UI and check the post
        EXPECTED: - Post is present in the Timeline
        EXPECTED: - Price is present in the post
        EXPECTED: - Bet Prompt Header is present in the post
        EXPECTED: ![](index.php?/attachments/get/120925770)
        """
        pass

    def test_009___navigate_back_to_the_same_event_in_the_cms__lick_on_the_create_post_in_spotlight_section__select_spotlight_template_without_configured_selectionid__click_on_the_create_post_and_publish_buttons(self):
        """
        DESCRIPTION: - Navigate back to the same event in the CMS
        DESCRIPTION: - Сlick on the 'Create Post' in Spotlight section
        DESCRIPTION: - Select 'Spotlight' template without configured SelectionID
        DESCRIPTION: - Click on the 'Create Post' and 'Publish' buttons
        EXPECTED: - SelectionID is deleted
        EXPECTED: - 'Price' button is NOT displayed on the Post Preview
        EXPECTED: - Bet Prompt Header is NOT present in the post
        """
        pass

    def test_010_go_to_the_ui_and_check_the_post(self):
        """
        DESCRIPTION: Go to the UI and check the post
        EXPECTED: - Post is present in the Timeline
        EXPECTED: - Price is NOT present in the post
        EXPECTED: - Bet Prompt Header is NOT present in the post
        EXPECTED: ![](index.php?/attachments/get/120925453)
        """
        pass
