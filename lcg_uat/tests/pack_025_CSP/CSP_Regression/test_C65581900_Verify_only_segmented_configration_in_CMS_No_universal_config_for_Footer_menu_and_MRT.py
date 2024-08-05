import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.reg156_fix
@pytest.mark.adhoc_suite
@pytest.mark.footer_menu
@pytest.mark.mobile_only
@vtest
class Test_C65581900_Verify_only_segmented_configration_in_CMS_No_universal_config_for_Footer_menu_and_MRT(Common):
    """
    TR_ID: C65581900
    NAME: This test case verifies only segmented configration in CMS (No universal config) for Footer menu and MRT.
    DESCRIPTION: This test case verifies only segmented configration in CMS (No universal config) for Footer menu and MRT.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > for Footer menu/MRT.
    PRECONDITIONS: Create atleast a record in each module for segment
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    title = "CSP_1900"
    tab_title = 'Auto_CSP_Segment_Dont_DELETE'

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Footermenu/MRT
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

    def test_001_launch_coral_and_lads_appmobile_web(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web
        EXPECTED: Homepage should load as per CMS config
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_universal_view_observe_for_Footer_menu_and_MRT_as_per_pre_conditions(self):
        """
        DESCRIPTION: verify universal view ,observe all modules(as per pre conditions)
        EXPECTED: No data (records) should be displayed for Footer menu and MRT as there is no universal configuration
        """
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertNotIn(self.title, footer_items,
                         msg=f'Footer menu {self.title} is displayed')
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertNotIn(self.tab_title, tabs,
                         msg=f'Module ribbon tab {self.tab_title} is displayed')

    def test_003_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Homepage should load as per CMS segment config.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=40)

    def test_004_verify_homepage(self):
        """
        DESCRIPTION: Verify homepage
        EXPECTED: Segmented records for Footer menu and MRT should display as per CMS configurations
        """
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertIn(self.title, footer_items,
                      msg=f'Footer menu {self.title} is not displayed')
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertIn(self.tab_title.upper(), tabs,
                      msg=f'Module ribbon tab {self.tab_title.upper()} is not displayed')
