import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C59487130_Vanilla_Verify_Marketing_Communication_Preferences_page(Common):
    """
    TR_ID: C59487130
    NAME: [Vanilla] Verify Marketing/Communication Preferences page
    DESCRIPTION: This test case verifies Communication Preferences page
    DESCRIPTION: *Note:*
    DESCRIPTION: My Account Menu or User Menu is handled and set on GVC side.
    DESCRIPTION: Marketing/Communication Preferences page is handled on GVC side.
    PRECONDITIONS: User is logged in with valid credentials
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account_gt_settings_gt_marketing_coral__communication_ladbrokes_preferences(self):
        """
        DESCRIPTION: Navigate to My Account &gt; Settings &gt; Marketing (Coral) / Communication (Ladbrokes) Preferences
        EXPECTED: *Coral:*
        EXPECTED: Marketing Preferences page consists of:
        EXPECTED: * Title 'Marketing Preferences', 'Back' and 'Close' button
        EXPECTED: * Decription of the page purpose
        EXPECTED: * "I would like to receive the latest offers and promotions from Coral by:" text in caps.
        EXPECTED: * Checkboxes (Email, Phone call, SMS, Post)
        EXPECTED: * Blue infobox is displayed if no or email checkbox not selected
        EXPECTED: * "You can update your preferences at any time. Further details are available in our Privacy Notice". "Privacy Notice" is hyperlinked.
        EXPECTED: * 'Save' button
        EXPECTED: ![](index.php?/attachments/get/115430232)
        EXPECTED: *Ladbrokes:*
        EXPECTED: Communication Preferences page consists of:
        EXPECTED: * Title 'Communication Preferences', 'Back' and 'Close' button
        EXPECTED: * Decription of the page purpose
        EXPECTED: * "I would like to receive the latest offers and promotions from Coral by:" text.
        EXPECTED: * Checkboxes (Email, Phone call, SMS, Post)
        EXPECTED: * Blue infobox is displayed if no or email checkbox not selected
        EXPECTED: * "You can update your preferences at any time. Further details are available in our Privacy Notice". "Privacy Notice" is hyperlinked.
        EXPECTED: * 'Save' button
        EXPECTED: ![](index.php?/attachments/get/115430233)
        """
        pass

    def test_002_make_all_checkboxes_deselected_and_verify_text_in_blue_infobox(self):
        """
        DESCRIPTION: Make all checkboxes deselected and verify text in blue Infobox
        EXPECTED: "Don't miss out on offers and promotions from Coral/Ladbrokes." Text displayed
        """
        pass

    def test_003_select_any_checkbox_except_email_and_verify_text_changes_blue_infobox(self):
        """
        DESCRIPTION: Select any checkbox except "Email" and Verify text changes blue Infobox
        EXPECTED: "Don't miss out on email offers and promotions from Coral/Ladbrokes" text displayed
        """
        pass

    def test_004_select_email_checkbox_and_verify_blue_infobox(self):
        """
        DESCRIPTION: Select "Email" checkbox and verify blue Infobox
        EXPECTED: Infobox not displayed
        """
        pass

    def test_005_click_privacy_notice(self):
        """
        DESCRIPTION: Click Privacy Notice
        EXPECTED: User redirected to corresponding brand Privacy Policy page
        """
        pass

    def test_006_select_some_checkboxes_and_click_save_button(self):
        """
        DESCRIPTION: Select some checkboxes and click 'Save' button
        EXPECTED: "Your communication preferences have been saved successfully" message displayed.
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/115430235)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/115430236)
        """
        pass
