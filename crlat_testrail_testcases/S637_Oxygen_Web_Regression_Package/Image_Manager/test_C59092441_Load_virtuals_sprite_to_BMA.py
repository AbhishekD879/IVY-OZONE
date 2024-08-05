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
class Test_C59092441_Load_virtuals_sprite_to_BMA(Common):
    """
    TR_ID: C59092441
    NAME: Load virtuals sprite to BMA
    DESCRIPTION: This test case verifies that Virtual sprite from CMS-Image manager is uploaded to the Oxygen App
    PRECONDITIONS: - Oxygen App is opened
    PRECONDITIONS: - CMS-Image manager is opened
    """
    keep_browser_open = True

    def test_001_in_oxygen_app_open_devtools_choose_network_tab_and_filter_requests_by_sprite(self):
        """
        DESCRIPTION: In Oxygen App open DevTools, choose Network tab and filter requests by <sprite>
        EXPECTED: Requests are filtered, <additional> sprite is in the list.
        EXPECTED: **NOTE:**
        EXPECTED: For mobile there will be <additional> and <featured> sprites.
        """
        pass

    def test_002_in_oxygen_app_navigate_to_virtual_sports_virtual_sports(self):
        """
        DESCRIPTION: In Oxygen App navigate to Virtual Sports (/virtual-sports).
        EXPECTED: 
        """
        pass

    def test_003_review_devtools(self):
        """
        DESCRIPTION: Review DevTools
        EXPECTED: One more sprite is added to the list - <virtual>
        """
        pass

    def test_004_open_cms_image_manager_and_add_new_active_icon_to_virtual_sprite_save_changes(self):
        """
        DESCRIPTION: Open CMS-Image manager and add new active icon to Virtual sprite, save changes.
        EXPECTED: Changes are saved, icon is added
        """
        pass

    def test_005_navigate_to_cms_virtual_sports_edit_sport_and_change_existing_icon_to_previously_createdsave_changes(self):
        """
        DESCRIPTION: Navigate to CMS-Virtual Sports-edit sport and change existing icon to previously created.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved, icon is added to virtual sport
        """
        pass

    def test_006_in_oxygen_app_refresh_the_page_open_virtual_request_and_verify_presence_of_previously_created_icon(self):
        """
        DESCRIPTION: In Oxygen app refresh the page, open <virtual> request and verify presence of previously created icon
        EXPECTED: Icon is present in the list
        """
        pass

    def test_007_in_oxygen_app_review_the_changed_icon(self):
        """
        DESCRIPTION: In Oxygen app review the changed icon
        EXPECTED: Icon is uploaded to UI correctly.
        """
        pass

    def test_008_inspect_ui_element_using_devtools(self):
        """
        DESCRIPTION: Inspect UI element using DevTools
        EXPECTED: Icon name is the same as in CMS
        """
        pass
