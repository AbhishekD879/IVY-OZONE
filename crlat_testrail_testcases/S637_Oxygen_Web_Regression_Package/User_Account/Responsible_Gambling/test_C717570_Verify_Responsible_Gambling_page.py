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
class Test_C717570_Verify_Responsible_Gambling_page(Common):
    """
    TR_ID: C717570
    NAME: Verify "Responsible Gambling" page
    DESCRIPTION: This test case verifies content of "Responsible Gambling" page
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_tap_the_balance_icon(self):
        """
        DESCRIPTION: Tap the balance icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_my_account(self):
        """
        DESCRIPTION: Tap "My Account"
        EXPECTED: User menu is opened
        """
        pass

    def test_003_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap "Responsible Gambling"
        EXPECTED: User is navigated to the "Responsible Gambling" page
        """
        pass

    def test_004_in_the_network_tab_check_the_responsible_gambling_en_us_request(self):
        """
        DESCRIPTION: In the "Network" tab, check the **responsible-gambling-en-us** request
        EXPECTED: HTML with all content for "Responsible Gambling" page is received from a static block in CMS
        """
        pass

    def test_005_verify_the_page_content(self):
        """
        DESCRIPTION: Verify the page content
        EXPECTED: Page content corresponds to the data, received in the response to the **responsible-gambling-en-us** request
        """
        pass

    def test_006_in_cms_go_to_static_blocks___responsible_gambling_en(self):
        """
        DESCRIPTION: In CMS, go to Static Blocks -> Responsible Gambling EN
        EXPECTED: The page contains all information visible in the app on the "Responsible Gambling" page
        """
        pass

    def test_007_make_any_changes_to_the_text_and_save(self):
        """
        DESCRIPTION: Make any changes to the text and save
        EXPECTED: Changes are saved
        """
        pass

    def test_008_refresh_the_responsible_gambling_page_in_oxygen_app_and_verify_the_text(self):
        """
        DESCRIPTION: Refresh the "Responsible Gambling" page in Oxygen app and verify the text
        EXPECTED: Changes, made during previous step, are reflected on the front end
        """
        pass
