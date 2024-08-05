import time
import pytest
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@pytest.mark.other
@vtest
class Test_C65581898_Verify_user_can_able_to_select_and_delete_one_or_more_segments_from_the_Delete_Segment_page_list_and_Verify_in_FE_for_surface_bet_module(Common):
    """
    TR_ID: C65581898
    NAME: Verify user can able to select and delete one or more segments from the 'Delete Segment' page list and Verify in FE for Footer menu and MRT modules.
    DESCRIPTION: This testcase verifies delete one or more segments from the 'Delete Segment' page list
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > delete segment page
    PRECONDITIONS: CMS > Main navigation>Surface bet/SB/Footermenu/HC/MRT/Inplay/Featured/QL/Sports ribbon
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = 'CSP_AUTO_C65581898'
    tab_title = 'Auto_CSP_Segment_DELETE'
    title = "CSP_81898"

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS:  CMS > sports pages > Footermenu/MRT
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        self.cms_config.create_footer_menu(title=self.title,
                                           universalSegment=False,
                                           inclusionList=[self.segment],
                                           showItemFor='loggedIn')
        footer_items = self.cms_config.get_cms_menu_items(menu_types='Footer Menus')['Footer Menus']
        for item in footer_items:
            if item['linkTitle'] == self.title:
                drag_panel_id = item['id']
                break
        else:
            raise CMSException(f'Created item {self.title} not found')
        order = [item['id'] for item in footer_items]
        order.remove(drag_panel_id)
        order.insert(0, drag_panel_id)
        self.cms_config.change_order_of_footer_items(new_order=order, moving_item=drag_panel_id)
        self.cms_config.module_ribbon_tabs.create_tab(title=self.tab_title, directive_name="BuildYourBet")
        self.cms_config.module_ribbon_tabs.update_tab(tab_name=self.tab_title, inclusion_list=[self.segment], universal=False)

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        self.device.refresh_page()
        sleep(5)
        footer_items = wait_for_result(lambda: list(self.site.navigation_menu.items_as_ordered_dict.keys()), timeout=15)
        self.assertIn(self.title, footer_items,
                      msg=f'Footer menu {self.title} is not displayed')
        Module_ribbon_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertIn(self.tab_title.upper(), Module_ribbon_tabs,
                      msg=f'Module ribbon tab {self.tab_title.upper()} is not displayed')

    def test_002_navigate_to_delete_segments_page(self):
        """
        DESCRIPTION: Navigate to Delete segments page
        EXPECTED: Delete segment page should be opened with 'Segments list' dropdown
        """
        # covered in below step

    def test_003_verify_segments_list_dropdown(self):
        """
        DESCRIPTION: Verify Segments list dropdown
        EXPECTED: When user expand segments list ,all existing  segments should display with delete option
        """
        # can not validate CMS UI

    def test_004_select_segment_from_the_dropdown(self):
        """
        DESCRIPTION: Select segment from the dropdown
        EXPECTED: User should able to select segments with check boxes.
        """
        # can not validate CMS UI

    def test_005_select_single_segment_from_the_list(self):
        """
        DESCRIPTION: Select single segment from the list
        EXPECTED: 1. user should able to delete segment through delete icon
        EXPECTED: 2. User can able to delete selected segment from the list"
        """
        self.cms_config.delete_segment(segment_name=self.segment)
        sleep(5)

    def test_006_select_multiple_segments_from_the_list(self):
        """
        DESCRIPTION: Select multiple segments from the list
        EXPECTED: User should able to select and delect multiple segments from the list
        """
        # covered in above step

    def test_007_navigate_to_surfacebet_module_and_verify(self):
        """
        DESCRIPTION: Navigate to Surfacebet module and verify
        EXPECTED: 1.Deleted segment should not display in segment dropdown list
        EXPECTED: 2.Existing configuration should not display
        EXPECTED: 3.Excluded record also should not  dispaly in Universal
        """
        # can not validate CMS UI

    def test_008_navigate_to_fe_and_login_with_deleted_segmented_user(self):
        """
        DESCRIPTION: Navigate to FE and login with deleted segmented user
        EXPECTED: Universal view should display as segment is deleted
        """
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        if self.title in footer_items:
            wait_time = 3  # Wait time in seconds
            max_polling_time = 60  # Maximum polling time in seconds (1 minutes)
            start_time = time.time()
            while time.time() - start_time < max_polling_time:
                if self.title in footer_items:
                    wait_for_haul(wait_time)
                    self.device.refresh_page()
                    footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
                else:
                    break
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertNotIn(self.title, footer_items,
                         msg=f'deleted Footer menu {self.title} is displayed')

    def test_009_Repeat_same_steps_for_MRT_module(self):
        """
        EXPECTED: Universal view should displayed when delete segment user logged in
        """
        Module_ribbon_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertNotIn(self.tab_title.upper(), Module_ribbon_tabs,
                         msg=f'deleted Module ribbon tab {self.tab_title.upper()} is displayed')
