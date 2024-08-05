import pytest
import tests
import voltron.environments.constants as vec
import time
from datetime import datetime
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@vtest
class Test_C64881009_Verify_Universal_exclusion_for_CSP_related_modules_QL_and_MRT(BaseFeaturedTest):
    """
    TR_ID: C64881009
    NAME: Verify Universal exclusion for CSP related modules QL & MRT.
    DESCRIPTION: This test case verifies universal exclusion
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    """
    keep_browser_open = True
    destination_url = f'https://{tests.HOSTNAME}//sport/football/matches'
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    sport_id = {'homepage': 0}
    tab_title = 'Auto_CSP_Segment_Dont_DELETE'

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_title = 'Autotest_' + 'C64881009'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.sport_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          universalSegment=True,
                                          exclusionList=[self.segment])
        self.cms_config.module_ribbon_tabs.create_tab(title=self.tab_title, directive_name="BuildYourBet")
        self.cms_config.module_ribbon_tabs.update_tab(tab_name=self.tab_title, exclusion_list=[self.segment],
                                                      universal=True)

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # covered in step 001

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on HC.
        EXPECTED: User should be able to view existing super buttons should be displayed.
        """
        # covered in step 001

    def test_004_click_on_super_button_cta_button(self):
        """
        DESCRIPTION: Click on HC CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        # covered in step 001

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting Universal radio button ,Segment(s) Exclusion text field should be enabled and able to enter text (ex: Football)
        """
        # covered in step 001

    def test_006_click_on_create_button(self):
        """
        DESCRIPTION: Click on create button
        EXPECTED: On successful creation, page should redirect to super button module page
        """
        # covered in step 001

    def test_007_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_008_login_in_fe_with_userexcept_specific_segmented_user__which_is_excluded(self):
        """
        DESCRIPTION: Login in FE with user(except specific segmented user  which is excluded)
        EXPECTED: Universal user should able to view super buttons across the application except in football segment (as we have configured segment(s) Exclusion as Football)
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        quick_link_stauts = self.site.home.tab_content.has_quick_links()
        if quick_link_stauts:
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            quick_link = quick_links.get(self.quick_link_title)
            refresh_count = 0
            max_refresh_attempts = 3
            while quick_link and refresh_count < max_refresh_attempts:
                # Wait for a short time and refresh the page
                wait_for_haul(5)
                self.device.refresh_page()
                # Check if the desired quick link is present
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                quick_link = quick_links.get(self.desired_quick_link_title)
                # Increment the refresh counter
                refresh_count += 1
            self.assertFalse(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')

    def test_009_repeat_same_steps_for_remaining_all_other_modules(self):
        """
        DESCRIPTION: Repeat same steps for remaining all other modules (as per pre conditions )
        EXPECTED: Excluded record should not displayed for specific segmented user.
        """
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertNotIn(self.tab_title, tabs,
                         msg=f'Module ribbon tab {self.tab_title} is displayed')
