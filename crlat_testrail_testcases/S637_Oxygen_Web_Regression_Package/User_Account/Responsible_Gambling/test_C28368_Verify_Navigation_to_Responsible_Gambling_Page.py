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
class Test_C28368_Verify_Navigation_to_Responsible_Gambling_Page(Common):
    """
    TR_ID: C28368
    NAME: Verify Navigation to 'Responsible Gambling' Page
    DESCRIPTION: This test case verifies navigation to 'Responsible Gambling' page
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User is viewing Home page
    """
    keep_browser_open = True

    def test_001_for_mobiletablettap_right_menu_button(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Tap Right Menu button
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_002_tapclick_on_my_account_item(self):
        """
        DESCRIPTION: Tap/click on 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_003_tapclick_on_responsible_gambling(self):
        """
        DESCRIPTION: Tap/click on 'Responsible Gambling'
        EXPECTED: 'Responsible Gambling' page is opened
        """
        pass

    def test_004_go_to_the_responsible_gambling_page_via_direct_linkhttpsenvironmentresponsible_gambling(self):
        """
        DESCRIPTION: Go to the 'Responsible Gambling' page via direct link:
        DESCRIPTION: https://{environment}/responsible-gambling
        EXPECTED: 'Responsible Gambling' page is opened
        """
        pass

    def test_005_tapclick_on_back_button(self):
        """
        DESCRIPTION: Tap/click on 'Back' button
        EXPECTED: Homepage is opened
        """
        pass
