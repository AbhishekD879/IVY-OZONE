import pytest
import tests
from voltron.environments import constants as vec
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65599243_Verify_segmented_view_for_segmented_user_for_Featured_Module_and_Footer_Menu(BaseFeaturedTest):
    """
    TR_ID: C65599243
    NAME: Verify segmented view for segmented user for Featured Module and Footer Menu
    DESCRIPTION: This test case verifies segmented view for segmented user
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured Module/Footer Menu
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    title = "CSP_99243"

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Featured Module/Footer Menu
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
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=False,
                                                                             inclusionList=[self.segment],
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

    def test_001_launch_the_application_in_mobilewebapp(self):
        """
        DESCRIPTION: Launch the application in mobile(Web/App)
        EXPECTED: Application should launch successfully.
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_(self):
        """
        DESCRIPTION:
        EXPECTED: Home page should be opened.
        """
        # Covered in above step

    def test_003_login_with_specific_segmented_user__as_per_pre_conditions(self):
        """
        DESCRIPTION: Login with specific segmented user ( as per Pre-conditions)
        EXPECTED: User should login successfully
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_004_verify_segmented_record(self):
        """
        DESCRIPTION: Verify segmented record
        EXPECTED: User should able to see segmented record for specific segmented user as per CMS configuration
        """
        footer_items = list(self.site.navigation_menu.items_as_ordered_dict.keys())
        self.assertIn(self.title, footer_items,
                      msg=f'Footer menu {self.title} is not displayed')
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
