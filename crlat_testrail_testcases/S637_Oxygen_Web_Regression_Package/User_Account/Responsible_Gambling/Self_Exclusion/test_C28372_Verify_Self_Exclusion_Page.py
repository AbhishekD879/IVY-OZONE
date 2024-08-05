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
class Test_C28372_Verify_Self_Exclusion_Page(Common):
    """
    TR_ID: C28372
    NAME: Verify 'Self Exclusion' Page
    DESCRIPTION: This test case verifies 'Self Exclusion' page
    DESCRIPTION: Jira tickets: **BMA-3952, BMA-5513**
    PRECONDITIONS: User should be logged in to view 'Self Exclusion' page.
    PRECONDITIONS: To load CMS for English language support 'Self Exclusion EN' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: To load CMS for Ukrainian language support 'Self Exclusion UA' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_002_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_003_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_004_tap_the_read_more_about_self_exclusion_link(self):
        """
        DESCRIPTION: Tap the 'Read More About Self-Exclusion' link
        EXPECTED: User is navigated to the 'Self-Exclusion' page
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is directed to previous page after tapping Back button
        """
        pass

    def test_006_verify_the_self_exclusion_page(self):
        """
        DESCRIPTION: Verify the 'Self Exclusion' page
        EXPECTED: The 'Self-Exclusion' page consists of the next elements:
        EXPECTED: *   The 'More About Self Exclusion' title
        EXPECTED: *   The CMS-controlled policy
        EXPECTED: *   The 'Request Self Exclusion' link
        """
        pass

    def test_007_verify_the_request_self_exclusion_link(self):
        """
        DESCRIPTION: Verify the 'Request Self Exclusion' link
        EXPECTED: The 'Self Exclusion' pop-up is shown after clicking the link
        """
        pass
