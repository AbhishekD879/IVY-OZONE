import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.quick_links
@pytest.mark.desktop_specific
@pytest.mark.adhoc_suite
@pytest.mark.other
@vtest
class Test_C65949623_Desktop_quick_links_creation_and_display(Common):
    """
    TR_ID: C65949623
    NAME: Desktop quick links creation and display
    DESCRIPTION: This test case is to validate Desktop Quick Links
    PRECONDITIONS: 1. User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2. Login with valid credentials
    PRECONDITIONS: 3.Navigate to Quick Link>Desktop Quick Links
    PRECONDITIONS: 4.Create a Desktop Quick Link
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    quick_link_title = 'Auto_quick_link'
    target_url = 'sport/football'

    def change_order_of_desktop_quick_link(self):
        desktop_quick_links = self.cms_config.get_desktop_quick_links()
        desktop_quick_link_ids_list = [desktop_quick_link.get('id') for desktop_quick_link in
                                     desktop_quick_links if desktop_quick_link.get('disabled') == False]
        desktop_quick_link_id = desktop_quick_link_ids_list[1]
        desktop_quick_link_ids_list.remove(desktop_quick_link_id)
        desktop_quick_link_ids_list.insert(0,desktop_quick_link_id)
        self.cms_config.change_order_of_desktop_quick_links(new_order=desktop_quick_link_ids_list, moving_item=desktop_quick_link_id)

    def get_active_desktop_quicklinks(self):
        desktop_quick_links = self.cms_config.get_desktop_quick_links()
        desktop_quick_link_titles = [desktop_quick_link.get('title') for desktop_quick_link in
                                     desktop_quick_links if desktop_quick_link.get('disabled') == False]
        return desktop_quick_link_titles

    def verify_desktop_quick_links_in_FE(self, name, expected_result=True):

        result = wait_for_cms_reflection(lambda: self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict.get(name),
                                            ref=self,timeout=10, refresh_count=5, expected_result=expected_result)
        if expected_result:
            self.assertTrue(result, msg=f'{name} is not present in desktop quick links')
        else:
            self.assertFalse(result, msg=f'{name} is present in desktop quick links')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 3.Navigate to Quick Link>Desktop Quick Links
        PRECONDITIONS: 4.Create a Desktop Quick Link
        """
        desktop_quick_link = self.cms_config.create_desktop_quick_links(title=self.quick_link_title, target_url = self.target_url)
        self.__class__.desktop_quick_link_id = desktop_quick_link.get('id')
        self.__class__.desktop_quick_link_title = desktop_quick_link.get('title')

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        # covered in above step

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # covered in above step

    def test_003_click_on_desktop_quick_link_sub_section(self):
        """
        DESCRIPTION: Click on Desktop Quick Link sub section.
        EXPECTED: User able to view List of Desktop Quick Links along with Filter section"Create Desktop Quick Link"and "Download CSV" button.
        """
        # covered in above step

    def test_004_click_on_create_desktop_quick_link_button(self):
        """
        DESCRIPTION: Click on "Create Desktop Quick Link" button
        EXPECTED: Fill all the Fields and click on "Save" button
        """
        # covered in above step

    def test_005_verify_created_desktop_quick_link_should_add_to_the_desktop_quick_links_list(self):
        """
        DESCRIPTION: Verify created desktop quick link should add to the Desktop Quick Links list
        EXPECTED: Newly creates Desktop quick Link is added to list
        """
        desktop_quick_links_list = self.get_active_desktop_quicklinks()
        self.assertIn(self.desktop_quick_link_title, desktop_quick_links_list, msg=f'{self.desktop_quick_link_title} is not present in quick liks {desktop_quick_links_list} in CMS')

    def test_006_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_007_scroll_the_page_down_to_view_desktop_quick_links(self):
        """
        DESCRIPTION: Scroll the page down to view Desktop Quick Links
        EXPECTED: User able to see all Desktop Quick Links at bottom of the page
        """
        self.site.home.quick_link_section.scroll_to()
        has_desktop_quick_link_section = self.site.home.has_quick_link_section()
        self.assertTrue(has_desktop_quick_link_section, msg='quick link section is not available')
        self.verify_desktop_quick_links_in_FE(name=self.desktop_quick_link_title)

    def test_008_desktop_quick_link_should_be_navigate_to_particular_page_which_has_configured_in_cms(self):
        """
        DESCRIPTION: Desktop Quick Link should be navigate to particular page which has configured in CMS
        EXPECTED: User able to navigate to particular page once user click on particular Desktop Quick Link
        """
        desktop_quick_link = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict.get(self.desktop_quick_link_title)
        desktop_quick_link.click()
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/{self.target_url}'
        self.assertEqual(actual_url, expected_url, msg=f'actual url {actual_url} is not equal to expected url {self.target_url}')
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_009_navigate_to_the_cms_and_edit_that_particular_desktop_quick_link(self):
        """
        DESCRIPTION: Navigate to the CMS and edit that particular Desktop Quick Link
        EXPECTED: Edit some fields and click on "Save" button
        """
        self.__class__.modified_quick_link_name = 'modified_Auto_quick_link'
        self.cms_config.update_desktop_quick_links(desktop_quick_link_id=self.desktop_quick_link_id, title=self.modified_quick_link_name)

    def test_010_new_changes_will_be_saved_in_cms(self):
        """
        DESCRIPTION: New changes will be saved in CMS
        EXPECTED: User able to see Recently changed changes for particualr Desktop Quick Link will be reflected in FE
        """
        self.verify_desktop_quick_links_in_FE(name=self.modified_quick_link_name)

    def test_011_navigate_to_the_cms(self):
        """
        DESCRIPTION: Navigate to the CMS
        EXPECTED: User able to see List of Desktop Quick Links along with columns like Title,Uri,Remove,Edit
        """
        # covered in above step

    def test_012_click_on_the_remove_button_of_particular_dekstop_quick_link(self):
        """
        DESCRIPTION: Click on the remove button of particular Dekstop Quick Link
        EXPECTED: User displays pop up like
        EXPECTED: "Are You Sure Want to Remove Desktop Quick Link?"
        """
        self.cms_config.delete_desktop_quick_lnk(desktop_quick_link_id=self.desktop_quick_link_id)
        self.cms_config._created_desktop_quick_links.remove(self.desktop_quick_link_id)

    def test_013_click_on_yes_button(self):
        """
        DESCRIPTION: Click on "Yes" button
        EXPECTED: The deleted Desktop Quick Link will be disappeared from List
        """
        # covered in above 12th step

    def test_014_navigate_to_fe(self):
        """
        DESCRIPTION: Navigate to FE
        EXPECTED: User cannot see the Desktop Quick Link which has been deleted
        """
        self.verify_desktop_quick_links_in_FE(name=self.modified_quick_link_name, expected_result=False)

    def test_015_navigate_to_cmsgtquick_linksgtdesktop_quick_linksverify_drag_option_is_displayed_in_the_list(self):
        """
        DESCRIPTION: Navigate to CMS&gt;Quick Links&gt;Desktop Quick Links
        DESCRIPTION: Verify drag option is displayed in the list
        EXPECTED: change the order of the Desktop Quick Links ordering using dragging option
        """
        self.change_order_of_desktop_quick_link()
        desktop_ql_list = self.get_active_desktop_quicklinks()
        wait_for_cms_reflection(lambda : list(self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict.keys()) == desktop_ql_list,
                                timeout=10, refresh_count=5, ref=self, haul=3)

    def test_016_navigate_to_fe(self):
        """
        DESCRIPTION: Navigate to FE
        EXPECTED: The Sorting order of Desktop Quick Links will be same in FE as configured in CMS
        """
        expected_desktop_quick_links = self.get_active_desktop_quicklinks()
        actual_desktop_quicklinks = list(self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict.keys())
        self.assertListEqual(actual_desktop_quicklinks, expected_desktop_quick_links, msg=f'actual Desktop Quick Links {actual_desktop_quicklinks} is not '
                                                                                          f'equal to expected Desktop Quick Links {expected_desktop_quick_links}')