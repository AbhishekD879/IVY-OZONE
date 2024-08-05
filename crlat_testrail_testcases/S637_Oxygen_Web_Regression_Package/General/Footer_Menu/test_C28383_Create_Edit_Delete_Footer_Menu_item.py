import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28383_Create_Edit_Delete_Footer_Menu_item(Common):
    """
    TR_ID: C28383
    NAME: Create/Edit/Delete Footer Menu item
    DESCRIPTION: This test case verifies possibility of creation, editing and deleting of Footer Menu item
    PRECONDITIONS: To open CMS use link:
    PRECONDITIONS: footer-menus
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_link_provided_in_preconditions___tap_create_footer_menu_button(self):
        """
        DESCRIPTION: Go to link provided in preconditions -> Tap 'Create Footer Menu' button
        EXPECTED: 
        """
        pass

    def test_002_enter_valid_data_to_link_title_and_target_uri_fields__tap_create_button(self):
        """
        DESCRIPTION: Enter valid data to 'Link Title' and 'Target Uri' fields => Tap 'Create' button
        EXPECTED: 
        """
        pass

    def test_003_go_to_refreshed_invictus_application__footer_menu(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Footer Menu
        EXPECTED: Footer Menu is shown with Menu item with data entered in step №2
        """
        pass

    def test_004_go_to_cms__change_order_of_footer_menu_items_by_drag_n_drop(self):
        """
        DESCRIPTION: Go to CMS => Change order of Footer Menu items by drag-n-drop
        EXPECTED: 
        """
        pass

    def test_005_go_to_refreshed_invictus_application__footer_menu(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Footer Menu
        EXPECTED: Footer Menu Items order corresponds to order configured in step №4
        """
        pass

    def test_006_go_to_cms__make_valid_changes_in_any_fields__click_save_button(self):
        """
        DESCRIPTION: Go to CMS => Make valid changes in any fields => Click 'Save' Button
        EXPECTED: 
        """
        pass

    def test_007_go_to_refreshed_invictus_application(self):
        """
        DESCRIPTION: Go to refreshed Invictus application
        EXPECTED: All made changes in step №6 are saved and shown
        """
        pass

    def test_008_go_to_cms_click_on_delete_icon_near_menu_item_title_and_confirm_deleting_by_clicking_ok_button(self):
        """
        DESCRIPTION: Go to CMS => Click on delete icon near Menu item title and confirm deleting by clicking 'Ok' button
        EXPECTED: 
        """
        pass

    def test_009_go_to_refreshed_invictus_application__footer_menu(self):
        """
        DESCRIPTION: Go to refreshed Invictus application => Footer Menu
        EXPECTED: Deleted item is no more shown in Footer Menu
        """
        pass
