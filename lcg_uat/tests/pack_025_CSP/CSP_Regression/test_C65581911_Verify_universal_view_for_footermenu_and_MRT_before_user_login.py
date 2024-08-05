import pytest
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
class Test_C65581911_Verify_universal_view_for_footermenu_and_MRT_before_user_login(Common):
    """
    TR_ID: C65581911
    NAME: Verify universal view for Footer menu and MRT modules before user login.
    DESCRIPTION: This testcases verifies Universal view before user login
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Footermenu/MRT
    PRECONDITIONS: Create atleast a record in each module
    PRECONDITIONS: Select Universal Radio button while creating record.
    PRECONDITIONS: For Universal,There is atleast one record for each module added to the Homepage in CMS
    """
    keep_browser_open = True
    title = "CSP_1911"
    tab_title = 'Auto_CSP_Universal_Dont_DELETE'

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Footermenu/MRT
        """
        self.cms_config.create_footer_menu(title=self.title,
                                           universalSegment=True,
                                           showItemFor='loggedOut')
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
        self.cms_config.module_ribbon_tabs.update_tab(tab_name=self.tab_title)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application should launch successfully.
        """
        # Covered in above step

    def test_002_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: Home page should be opened.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_003_verify_universal_view_by_default_before_login(self):
        """
        DESCRIPTION: Verify universal view (by default) before login
        EXPECTED: User should able to view Universal records for each module (Footermenu/MRT) as configured in CMS.
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        if self.title not in footer_items:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='Homepage', timeout=30)
            footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertIn(self.title, footer_items,
                      msg=f'Footer menu {self.title} is not displayed')
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertIn(self.tab_title.upper(), tabs,
                      msg=f'Module ribbon tab {self.tab_title} is not displayed')
