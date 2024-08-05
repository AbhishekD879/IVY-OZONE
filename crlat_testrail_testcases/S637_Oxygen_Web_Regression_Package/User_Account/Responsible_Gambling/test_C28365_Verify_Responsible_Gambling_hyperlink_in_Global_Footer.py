import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28365_Verify_Responsible_Gambling_hyperlink_in_Global_Footer(Common):
    """
    TR_ID: C28365
    NAME: Verify 'Responsible Gambling' hyperlink in Global Footer
    DESCRIPTION: This test case verifies CMS and UI side of 'Responsible Gambling' hyperlink on the Global Footer.
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms_admin_static_blocks_footer_markup_bottom(self):
        """
        DESCRIPTION: Go to CMS->Admin->Static Blocks->Footer Markup Bottom
        EXPECTED: 'Footer Markup Bottom' page is opened
        """
        pass

    def test_002_enter_the_responsible_gambling_text_in_html_markup_field(self):
        """
        DESCRIPTION: Enter the 'Responsible Gambling' text in **Html Markup** field
        EXPECTED: * 'Responsible Gambling' text is displayed in **Html Markup** field
        EXPECTED: * It is possible to edit 'Responsible Gambling' text
        """
        pass

    def test_003_select_text_in_html_markup_field_and_click_on_insertedit_link_button(self):
        """
        DESCRIPTION: Select text in Html Markup field and click on **Insert/edit link** button
        EXPECTED: **Insert link** window is opened with the following fields:
        EXPECTED: *   **Url** field
        EXPECTED: *   **Text to display ** field
        EXPECTED: *   **Title** field
        EXPECTED: *   **Target** drop-down
        """
        pass

    def test_004_set_httpresponsiblegamblingcoralcouk_inurl_field(self):
        """
        DESCRIPTION: Set http://responsiblegambling.coral.co.uk/ in Url field
        EXPECTED: It is possible to set/edit Url
        """
        pass

    def test_005_verify_text_to_display_field(self):
        """
        DESCRIPTION: Verify **Text to display** field
        EXPECTED: * Filled in by selected text from step 3
        EXPECTED: * It is possible to edit text
        """
        pass

    def test_006_verify_title_field(self):
        """
        DESCRIPTION: Verify **Title** field
        EXPECTED: It is possible to set/edit text
        """
        pass

    def test_007_verify_target_drop_down(self):
        """
        DESCRIPTION: Verify **Target** drop-down
        EXPECTED: *   None is selected by default
        EXPECTED: *   Target drop-down contains: **None** and **New window**
        """
        pass

    def test_008_click_ok_button(self):
        """
        DESCRIPTION: Click **Ok** button
        EXPECTED: 
        """
        pass

    def test_009_verify_active_check_box(self):
        """
        DESCRIPTION: Verify **Active** check-box
        EXPECTED: It is possible to hide/show all hyperlinks in Bottom Global Footer
        """
        pass

    def test_010_click_save_button(self):
        """
        DESCRIPTION: Click **Save** button
        EXPECTED: Changes have been saved successfully
        """
        pass

    def test_011_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_012_go_to_global_footer(self):
        """
        DESCRIPTION: Go to Global Footer
        EXPECTED: * 'Responsible Gambling' text from step 2 is shown as hyperlink
        EXPECTED: * Hyperlinks in Bottom Global Footer are shown/hidden depending on settings in step 9
        """
        pass

    def test_013_click_on_the_responsible_gambling_hyperlink(self):
        """
        DESCRIPTION: Click on the 'Responsible Gambling' hyperlink
        EXPECTED: * 'Responsible Gambling Policy' is opened in the same window or new window depending on settings in step 7
        EXPECTED: * User is redirected to URL from step 4
        """
        pass
