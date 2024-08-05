from urllib.error import HTTPError
import pytest
from crlat_cms_client.utils.exceptions import CMSException

import tests
from faker import Faker
from datetime import datetime
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from crlat_core.request.exceptions import InvalidResponseException
from crlat_cms_client.utils.date_time import get_date_time_as_string
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.last
@vtest
class Test_C65783512_Create_new_mobile_quick_links_for_home_page_in_CMS(BaseFeaturedTest):
    """
    TR_ID: C65783512
    NAME: Create new mobile quick links for home page in CMS
    DESCRIPTION: - The objective of this test cases is to create new mobile quick link in CMS
    DESCRIPTION: **Note :** Mobile Quick links are applicable only for mobile apps and web but not for desktop view. For desktop, we have other test case.
    PRECONDITIONS: - User should have valid access to Oxygen CMS(Test environment may change as per build availability)
    PRECONDITIONS: - Home page Quick link module should be created and enabled under sports pages -> home page menu in CMS
    PRECONDITIONS: - CMS system config -> structure -> Sports quick should be enabled
    PRECONDITIONS: *Environments*
    PRECONDITIONS: QA CMS : https://cms-api-ui-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/login ozoneqa@ivycomptech.com / Admin
    PRECONDITIONS: Stg CMS : https://cms-api-ui-stg0.coralsports.nonprod.cloud.ladbrokescoral.com/login qa@coral.co.uk / Admin
    PRECONDITIONS: Beta CMS : https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/login ozoneqa@coral.co.uk / Admin
    """
    keep_browser_open = True
    auto_segment = vec.bma.CSP_CMS_SEGEMENT
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    device_name = tests.mobile_default
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    now = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                      minutes=40)[:-3] + 'Z'
    no_of_QL = None
    @classmethod
    def custom_tearDown(cls):
        cls.get_cms_config().update_system_configuration_structure(
            config_item='Sport Quick Links', field_name='maxAmount', field_value=cls.no_of_QL)

    def verify_quick_links_rows_blocks(self):
        """
        This method verifies whether Quick links are displayed as rows or blocks
        """
        self.site.home.tab_content.quick_links.scroll_to_we()
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick Links found on page')
        quick_links_x_list, quick_links_y_list, quick_links_width = [], [], []
        quick_link_container_width = self.site.home.tab_content.quick_links.size.get('width')
        quick_link_names = list(quick_links.keys())
        total_number_of_quick_links = len(quick_link_names)
        for quick_link_index in range(total_number_of_quick_links):
            quick_link_name = quick_link_names[quick_link_index]
            quick_links_y_list.append(quick_links.get(quick_link_name).location.get('y'))
            quick_links_x_list.append(quick_links.get(quick_link_name).location.get('x'))
            quick_links_width.append(quick_links.get(quick_link_name).size.get('width'))
            current_quick_link_width = quick_links.get(quick_link_name).size.get('width')
            if self.brand == 'ladbrokes':
                if (total_number_of_quick_links % 2 == 0) or (total_number_of_quick_links % 2 != 0 and quick_link_index < total_number_of_quick_links - 1):
                    self.assertAlmostEqual(current_quick_link_width, quick_link_container_width // 2, delta=31,
                                           msg=f'Quick Link "{quick_link_name}" '
                                               f'Width: {current_quick_link_width} is not half of the Quick link Container width : {quick_link_container_width}')
                else:
                    self.assertAlmostEqual(current_quick_link_width, quick_link_container_width, delta=31,
                                           msg=f'Quick Link "{quick_link_name}" '
                                               f'Width: {current_quick_link_width} is not equal to quick link container width : {quick_link_container_width}')

        if self.brand == 'ladbrokes':
            self.assertListEqual(quick_links_y_list, sorted(quick_links_y_list),
                                 msg='Quick Links are not displayed as rows in the list')
        else:
            self.assertGreater(len(set(quick_links_x_list + quick_links_y_list)), 2,
                               msg='Quick Links containers does not have flexible width')

    def updating_the_count_of_quick_links(self,segement=None):
        # reading existing quick links for universal segment
        existing_quick_links = []
        if segement:
            cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'),segment=self.auto_segment)
        else:
            cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        for cms_quick_link in cms_quick_links:
            if (cms_quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= cms_quick_link[
                'validityPeriodEnd']) and cms_quick_link['disabled'] is False:
                existing_quick_links.append(cms_quick_link['title'].upper().strip())
        # updating max amount of QL in system configuration--->structure-->sportQuicklLink
        if len(existing_quick_links) < 6:
            update_max_amount = len(existing_quick_links) + 1
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                  field_name='maxAmount', field_value=update_max_amount)
            wait_for_haul(20)
            result = wait_for_result(lambda: int(self.cms_config.get_system_configuration_item('Sport Quick Links').get(
                'maxAmount')) == update_max_amount,
                                     name='Sport Quick Links "maxAmount" value to be changed', poll_interval=5,
                                     timeout=120)
            self.assertTrue(result, msg=f'"maxAmount" value is not set to: {update_max_amount}')
        else:
            raise CMSException(f"Already there are 6 Active quick link we can't create more than 6 generally")

    def verify_fe_quick_link_displayed(self,quick_link_name=None):
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        self.device.refresh_page()
        self.site.home.tab_content.quick_links.scroll_to_we()
        self.verify_quick_link_displayed(name=quick_link_name,timeout=30)

    def validate_quick_link_cms_unviersal(self):
        # creating one QL with "universal" segment
        self.updating_the_count_of_quick_links()
        self.__class__.quick_link_names = ['Auto' + Faker().city() for _ in range(2)]
        self.__class__.quick_link_data = self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=self.date_from, date_to=self.date_to)
        self.verify_fe_quick_link_displayed(quick_link_name=self.quick_link_names[0])
        self.verify_quick_links_rows_blocks()
        # creating more than the limit
        try:
            self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                              sport_id=self.homepage_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=self.date_from, date_to=self.date_to
                                              )
        except InvalidResponseException as ex:
            self.assertIn("400 Client Error:", ex.args[0],
                          msg="create quick link call haven't failed because of the number it failed due to other error and need to verify again")
        # FE Validation and expected result is False
        self.verify_quick_link_displayed(name=self.quick_link_names[1],timeout=5,expected_result=False)

    def validate_quick_link_cms_Segement(self):
        self.updating_the_count_of_quick_links(segement=self.auto_segment)
        self.__class__.segment_quick_link_names = ['Auto_segment' + Faker().city() for _ in range(2)]
        self.__class__.segment_quick_link_data = self.cms_config.create_quick_link(title=self.segment_quick_link_names[0],
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=self.date_from, date_to=self.date_to,
                                          inclusionList=[self.auto_segment],
                                          universalSegment=False
                                          )
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.auto_segment)
        wait_for_haul(20)
        wait_for_cms_reflection(lambda :self.site.home.tab_content.quick_links.items_as_ordered_dict,
                                refresh_count=2 ,timeout=40,ref=self)
        self.verify_quick_link_displayed(name=self.segment_quick_link_names[0],timeout=60)
        self.verify_quick_links_rows_blocks()
        # creating more than the limit
        try:
            self.cms_config.create_quick_link(title=self.segment_quick_link_names[1],
                                              sport_id=self.homepage_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=self.date_from, date_to=self.date_to,
                                              inclusionList=[self.auto_segment],
                                              universalSegment=False
                                              )
        except InvalidResponseException as ex:
            self.assertIn("400 Client Error:", ex.args[0],
                          msg="create quick link call haven't failed because of the number it failed due to other error and need to verify again")
        # FE validation: expected result is False
        self.verify_quick_link_displayed(name=self.segment_quick_link_names[1],timeout=5,expected_result=False)

    def changing_Quick_link_order(self, quick_link_list=[]):
        all_qls = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        ql_ids = []
        for i in range(len(quick_link_list)):
            for ql in all_qls:
                if ql.get('title').upper() == quick_link_list[i].upper():
                    ql_ids.append(ql.get('id'))
                    break
        all_ql_ids = [item['id'] for item in all_qls]
        i = 0
        for ql_id in ql_ids:
            all_ql_ids.remove(ql_id)
            all_ql_ids.insert(i, ql_id)
            self.cms_config.set_quicklinks_ordering(new_order=all_ql_ids, moving_item=ql_id)
            i += 1

    def verify_ordering_of_quick_links(self):
        wait_for_haul(30)
        sections = self.site.home.tab_content.quick_links.items_as_ordered_dict
        actual_quick_links = list(sections.keys())
        expected_quick_links = []
        qls = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        for cms_quick_link in qls:
            if (cms_quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= cms_quick_link[
                'validityPeriodEnd']) and cms_quick_link['disabled'] is False:
                expected_quick_links.append(cms_quick_link['title'].upper().strip())
        self.assertEqual(actual_quick_links[0].upper(), expected_quick_links[0].upper(),
                          msg=f"expected highlight carousel is {expected_quick_links[0].upper()} but {actual_quick_links[0].upper()} ")

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        if not self.is_quick_links_enabled():
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                  field_name="enabled",
                                                                  field_value=True)
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        self.__class__.no_of_QL = int(sport_quick_links.get('maxAmount'))


    def test_001_launch_chrome_browseraccess_cms_url_as_per_requirementenvironments__test_stg_and_betaenter_valid_user_name_in_username_editable_text_box_and_password_in_password_editable_text_box_and_click_on_login_buttonenv_urls_and_credentials_as_per_pre_conditions(
            self):
        """
        DESCRIPTION: Launch chrome browser
        DESCRIPTION: Access CMS url as per requirement(Environments : Test, stg and beta)
        DESCRIPTION: Enter valid user name in username editable text box and password in password editable text box and click on Login button
        DESCRIPTION: Env urls and credentials as per pre conditions
        EXPECTED: User should able to login to CMS and by default coral brand should be displayed in brand drop down at top right corner.
        """
        # covered in preconditions

    def test_002_select_required_brand_ladbrokesfrom_brand_drop_down_at_top_right_corner_and_verify_current_brand(self):
        """
        DESCRIPTION: select required brand (Ladbrokes)from brand drop down at top right corner and verify current brand
        EXPECTED: Ladbrokes name should be displayed as per selection and content related to selected brand should be displayed.
        EXPECTED: If this test case want to execute for coral, no need to change brand.
        """
        # covered in preconditions

    def test_003_navigate_system_configuration___structure_from_left_menu_scroll_to_quicklinks_section(self):
        """
        DESCRIPTION: Navigate system configuration - structure from left menu, scroll to quickLinks section
        EXPECTED: User should able to see quick links current configuration
        """
        # covered in preconditions

    def test_004_capture_the_sports_quick_links_configurationenabled_maxamount_under_systems_config__ampgt_structure(
            self):
        """
        DESCRIPTION: Capture the sports quick links configuration(enabled, maxAmount) under systems config -&amp;gt; structure
        EXPECTED: Store current configuration in temp variable.
        EXPECTED: In general, always it should be enabled and max amount should set to 6
        """
        # covered in preconditions

    def test_005_navigate_to_cms__ampgt_sports_pages__ampgt_home_page_and_click_on_quick_links_and_verify_ui_of_qls_page_in_cms(
            self):
        """
        DESCRIPTION: Navigate to CMS -&amp;gt; sports pages -&amp;gt; home page and Click on Quick links and Verify UI of QLs page in CMS
        EXPECTED: **Quick Links UI should have following fields and buttons**
        EXPECTED: - Active check box should display(As per pre conditions it should be enabled)
        EXPECTED: - Create sports quick links button(Active by default)
        EXPECTED: - Segment drop down (Universal by default)
        EXPECTED: - Download button
        EXPECTED: - Search field
        EXPECTED: - Save Changes button at bottom of screen(Disable by default)
        EXPECTED: - revert changes button at bottom of screen(Disable by default)
        EXPECTED: - Grid with following columns
        EXPECTED: 1. Title with sort option for the records
        EXPECTED: 2. Segment(s)
        EXPECTED: 3. Segments(S) exclusion
        EXPECTED: 4. Url
        EXPECTED: 5. Enabled
        EXPECTED: 6. Visibility period start
        EXPECTED: 7. Visibility period End
        EXPECTED: 8. Remove(remove icon at each row)
        EXPECTED: 9. Edit(Edit icon at each row)
        """
        # covered in preconditions

    def test_006_make_sure_universal_is_selected_from_segment_drop_down_list_and_sort_on_validity_period_end_date_in_descending_order_click_twice_on_validity_period_end_date(
            self):
        """
        DESCRIPTION: Make sure universal is selected from segment drop down list, and sort on validity period end date in descending order (Click twice on validity period end date).
        EXPECTED: All the records should sort in descending order
        """
        # updating max count and validating universal segments QL in FE
        self.validate_quick_link_cms_unviersal()
    def test_007_read_all_enabled__true_records_and_validity_period_end_date_is_greater_that_current_system_time(self):
        """
        DESCRIPTION: Read all enabled = true records and validity period end date is greater that current system time.
        EXPECTED: Store the current active records in temp variable
        """
        # covered in step6

    def test_008_click_on_create_sports_quick_link_button_and_enter_invalid_data_in_any_fields_and_click_on_create_buttoninvalid_date__destination_url_should_not_start_with_httpstitle_destination_url_are_mandatory_fields_and_visibility_end_date_should_have_future_end_date_if_user_not_providing_required_valid_data_create_button_will_be_in_disable_mode_(
            self):
        """
        DESCRIPTION: Click on create sports quick link button and enter invalid data in any fields and click on create button.
        DESCRIPTION: Invalid date : Destination url should not start with https;//
        DESCRIPTION: **Title, destination url are mandatory fields and visibility end date should have future end date**
        DESCRIPTION: _if user not providing required valid data create button will be in disable mode_
        EXPECTED: if user not providing required valid data create button should be in disable mode
        """
        # ******** Updation of Quick Link dates to Past dates *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-8.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format, url_encode=False,
                                            hours=-8.5)[:-3] + 'Z'
        try:
            self.cms_config.create_quick_link(title="Auto_date",
                                              sport_id=self.homepage_id.get('homepage'),
                                              destination=self.destination_url,
                                              date_from=start_time, date_to=end_time,
                                              )
        except InvalidResponseException as ex:
            self.assertIn("400 Client Error:", ex.args[0],
                          msg="create quick link call haven't failed even though date format is wrong")

        # giving URL whithout http

        Wrong_URL = "beta-sports.ladbrokes.com/sport/football/matches"
        try:
            self.cms_config.create_quick_link(title="Auto_URL",
                                              sport_id=self.homepage_id.get('homepage'),
                                              destination=Wrong_URL,
                                              date_from=self.start_date, date_to=self.date_to,
                                              )
        except InvalidResponseException as ex:
            self.assertIn("400 Client Error:", ex.args[0],
                          msg="create quick link call haven't failed even though URL format is wrong")
    def test_009_enter_valid_data_in_all_fields_and_click_on_create_buttonvalid_date__destination_url_should_start_with_httpstitle__should_contain_atleast_one_charactervalid_period_end_date_should_not_be_past_time_than_current_system_timetitle_destination_url_are_mandatory_fields_and_visibility_end_date_should_have_future_end_date_if_user_not_providing_required_valid_data_create_button_will_be_in_disable_mode_(
            self):
        """
        DESCRIPTION: Enter valid data in all fields and click on create button.
        DESCRIPTION: valid date : Destination url should start with https;//
        DESCRIPTION: Title : should contain atleast one character
        DESCRIPTION: Valid period end date: should not be past time than current system time
        DESCRIPTION: **Title, destination url are mandatory fields and visibility end date should have future end date**
        DESCRIPTION: _if user not providing required valid data create button will be in disable mode_
        EXPECTED: If the count of current active records (readings from step7) count &amp;gt;= the count of maxAmount(reading from step3) for universal view below error message should display
        EXPECTED: **Error: Validation failed with reason: 1 Quick Links are already scheduled for this period for segment(s) with Universal, Seg1, Seg2. Please amend your schedule for segment(s)**
        """
        # covered in above steps for validating date and urls


    def test_010_close_the_error_pop_up_and_navigate_back_to_quick_links_list_screen(self):
        """
        DESCRIPTION: Close the error pop up and navigate back to quick links list screen
        EXPECTED: Pop up should closed and user should be in quick links list page
        """
        # covered in above step

    def test_011_open_any_active_recordreading_from_step7_click_on_active_check_boxunselect_and_save_changes(self):
        """
        DESCRIPTION: Open any active record(reading from step7) click on active check box(unselect) and save changes
        EXPECTED: Quick link should be inactive and current active records count should decrease to -1
        EXPECTED: update readings in step7
        """
        ########################reading active QL's in home page#########################
        active_quick_links = []
        cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        for cms_quick_link in cms_quick_links:
            if (cms_quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= cms_quick_link[
                'validityPeriodEnd']) and cms_quick_link['disabled'] is False:
                active_quick_links.append(cms_quick_link['title'].upper().strip())
        active_QL_len = len(active_quick_links)

        ############# inactive one QL################
        self.cms_config.change_quick_link_state(active=False, quick_link_object = self.quick_link_data)

        ######################after inactive one QL####################
        after_inactive_quick_link = []
        after_cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        for after_cms_quick_link in after_cms_quick_links:
            if (after_cms_quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= after_cms_quick_link[
                'validityPeriodEnd']) and after_cms_quick_link['disabled'] is False:
                after_inactive_quick_link.append(after_cms_quick_link['title'].upper().strip())
        after_inactive_QL_len = len(after_inactive_quick_link)

        ####### assertion of inactive one QL#######

        self.assertEqual(active_QL_len-1, after_inactive_QL_len,
                         f'active quick links length {active_QL_len} is not reduced even after inactivation{after_inactive_QL_len} of a one QL')

        self.cms_config.change_quick_link_state(active=True, quick_link_object=self.quick_link_data)

    def test_012_repeat_step8_with_valid_date(self):
        """
        DESCRIPTION: Repeat step8 with valid date
        EXPECTED: Quick link should be saved and should display last in the row
        """
        # covered in above steps

    def test_013_sort_newly_created_ql_from_last_to_first_place_in_cms(self):
        """
        DESCRIPTION: Sort newly created QL from last to first place in CMS
        EXPECTED: QL order should change to top without page refresh
        """
        ql_list = [self.quick_link_data['title']]
        self.changing_Quick_link_order(quick_link_list=ql_list)
        wait_for_cms_reflection(lambda :self.site.home.tab_content.quick_links.items_as_ordered_dict, refresh_count=3,ref=self)
        self.device.refresh_page()
        self.verify_ordering_of_quick_links()

    def test_014_navigate_to_sports_pages_from_left_menu_and_click_on_home_page(self):
        """
        DESCRIPTION: Navigate to sports pages from left menu and click on home page
        EXPECTED: All home page modules should be displayed and quick links module should be enabled as per pre conditions
        """
        # updating max count and validating particular segments QL in FE

        self.validate_quick_link_cms_Segement()

    def test_015_sort_quick_links_modules_to_top_by_drag_and_drop(self):
        """
        DESCRIPTION: Sort quick links modules to top by drag and drop
        EXPECTED: quick links should be displayed at top for home page
        """
        pass
