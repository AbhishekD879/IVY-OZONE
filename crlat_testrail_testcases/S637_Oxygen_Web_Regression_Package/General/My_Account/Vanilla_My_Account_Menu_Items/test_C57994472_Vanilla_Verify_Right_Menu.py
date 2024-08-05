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
class Test_C57994472_Vanilla_Verify_Right_Menu(Common):
    """
    TR_ID: C57994472
    NAME: [Vanilla] Verify Right Menu
    DESCRIPTION: This test case verifies Right Menu
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_app_and_login(self):
        """
        DESCRIPTION: Load app and login
        EXPECTED: User is logged in
        """
        pass

    def test_002_click_on_the_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on the avatar icon on the header
        EXPECTED: Mini menu is displayed
        """
        pass

    def test_003_verify_menu_items(self):
        """
        DESCRIPTION: Verify Menu Items
        EXPECTED: Menu items (Banking, Offers, History, etc) are clickable.
        EXPECTED: Relevant sub menu or another page is displayed after clicking on menu item.
        """
        pass

    def test_004_verify_sub_menu(self):
        """
        DESCRIPTION: Verify Sub Menu
        EXPECTED: Sub Menu is displayed.
        EXPECTED: Relevant page is displayed after clicking on sub menu item.
        EXPECTED: It is possible to go back to the main menu via Back button.
        """
        pass

    def test_005_verify_menu_closure(self):
        """
        DESCRIPTION: Verify Menu closure
        EXPECTED: Menu and Sub menus can be closed
        """
        pass
