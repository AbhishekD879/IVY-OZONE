import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.footer_menu
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581912_User_with_wrong_segment_which_is_other_than_CSP_for_Footermenu_and_MRT(Common):
    """
    TR_ID: C65581912
    NAME: User with wrong segment which is other than CSP_ for Footermenu/MRT
    DESCRIPTION: This test case verifies segment name
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Footermenu/MRT
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL.
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    Wrong_segment = vec.bma.UNIVERSAL_SEGMENT
    title = "CSP_C65581912"
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
        self.cms_config.change_order_of_footer_items(new_order=order, moving_item=drag_panel_id, segmentName=vec.bma.CSP_CMS_SEGEMENT)
        self.cms_config.module_ribbon_tabs.create_tab(title=self.tab_title, directive_name="BuildYourBet")
        self.cms_config.module_ribbon_tabs.update_tab(tab_name=self.tab_title, inclusion_list=[self.segment], universal=False)

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        # Covered in preconditions

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # Covered in preconditions

    def test_003_click_on_Footermenu_MRT_link(self):
        """
        DESCRIPTION: Click on Footermenu/MRT link.
        EXPECTED: User should be able to view existing super buttons
        """
        # Covered in preconditions

    def test_004_create_a_segmented_Footermenu_MRT_with_csp__excsp_1_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Footermenu/MRT with CSP_ (Ex:CSP_1) segment name and Login with Segmented user Verify in FE
        EXPECTED: User should able to view segmented Footermenu/MRT
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertIn(self.title, footer_items,
                      msg=f'Footer menu {self.title} is not displayed')
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertIn(self.tab_title.upper(), tabs,
                      msg=f'Module ribbon tab {self.tab_title} is not displayed')
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_005_create_a_segmented_Footermenu_MRT_otherthan_csp__exsegment_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Footermenu/MRT otherthan CSP_ (ex:Segment )segment name and Login with Segmented user Verify in FE
        EXPECTED: If user should belongs to wrong segment (without CSP_) Universal view should be displayed.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.Wrong_segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertNotIn(self.title, footer_items,
                         msg=f'Footer menu {self.title} is displayed')
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertNotIn(self.tab_title.upper(), tabs,
                         msg=f'Module ribbon tab {self.tab_title} is displayed')

    def test_006_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Universal view should displayed for wrong segmented name
        """
        # Covered in above steps
