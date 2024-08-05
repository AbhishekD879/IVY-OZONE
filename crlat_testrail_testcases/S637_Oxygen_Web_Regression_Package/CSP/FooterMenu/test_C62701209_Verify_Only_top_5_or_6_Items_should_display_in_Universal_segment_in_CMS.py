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
class Test_C62701209_Verify_Only_top_5_or_6_Items_should_display_in_Universal_segment_in_CMS(Common):
    """
    TR_ID: C62701209
    NAME: Verify Only top 5 or 6 Items should display in Universal segment in CMS
    DESCRIPTION: This test case verifies records for each segments
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Menus > Footer menu
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_2go_to_menu___footer_menues_page(self):
        """
        DESCRIPTION: 2.Go to Menu -> footer menues page
        EXPECTED: User should be able to see the Primary Tab Module page
        """
        pass

    def test_003_verify_message_on_top(self):
        """
        DESCRIPTION: Verify message on top
        EXPECTED: User should able to see message as "Only top 5 or 6 Items (depending on brand) of Each Device Type, Will be Displayed"
        """
        pass

    def test_004_verify_itemsrecords_for_each_segment(self):
        """
        DESCRIPTION: Verify items(records) for each segment
        EXPECTED: Only top 5 or 6 Items should display per segment on footer menus page
        """
        pass
