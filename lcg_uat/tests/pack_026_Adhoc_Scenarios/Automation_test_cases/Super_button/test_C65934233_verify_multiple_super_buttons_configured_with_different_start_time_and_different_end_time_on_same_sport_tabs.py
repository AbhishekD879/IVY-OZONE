from datetime import datetime
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.super_button
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.reg167_fix
@vtest
class Test_C65934233_verify_multiple_super_buttons_configured_with_different_start_time_and_different_end_time_on_same_sport_tabs(Common):
    """
    TR_ID: C65934233
    NAME: verify multiple super buttons configured with different start time and different end time on same sport tabs
    """
    # This TestCase Covers C65934236
    keep_browser_open = True
    theme = 'theme_1'
    event_ids = []
    timezone = str(get_localzone())
    description = 'Updated Auto 236 Super Button description'
    disabled_super_buttons = []
    mrt_tab_name = "TODAY'S RACING"

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=10):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            home_tabs = self.get_todays_racing_url()
            if supper_button.get('enabled') and (category_id in supper_button.get('categoryId') or home_tabs[0] in supper_button.get('homeTabs')):
                if self.timezone.upper() == "UTC":
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                             time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                             url_encode=False)[:-3] + 'Z'
                elif self.timezone.upper() == 'EUROPE/LONDON':
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                             time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                             url_encode=False, hours=-1)[:-3] + 'Z'
                else:
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                             time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                             url_encode=False, hours=-5.5)[:-3] + 'Z'
                if not (supper_button.get('validityPeriodStart') <= now <= supper_button.get('validityPeriodEnd')):
                    continue
                self.cms_config.update_mobile_super_button(name=supper_button.get('title'), enabled=False)
                self.disabled_super_buttons.append(supper_button.get('title'))

    def update_and_check(self, description="Hello This is Description", sb_response=None, page=None):
        sb_response = self.supper_button_response_2 if not sb_response else sb_response
        res = self.cms_config.update_mobile_super_button(name=sb_response["title"],
                                                   description=description, themes=self.theme)

        wait_for_haul(20)
        self.device.refresh_page()
        page = self.site.cricket if page == 'cricket' else self.site.home
        actual_updated_description = page.super_button_section.super_button.description
        actual_updated_theme = self.site.home.super_button_section.super_button.theme
        if description.upper() != actual_updated_description.upper() or self.theme.replace('_','').upper() != actual_updated_theme.upper():
            for i in range(15):
                self.device.refresh_page()
                wait_for_haul(5)
                page = self.site.cricket if page == 'cricket' else self.site.home
                actual_updated_description = page.super_button_section.super_button.description
                actual_updated_theme = self.site.home.super_button_section.super_button.theme
                if description.upper() == actual_updated_description.upper() and self.theme.replace('_', '').upper() == actual_updated_theme.upper():
                    break
        self.assertEqual(description.upper(), actual_updated_description.upper(),
                         msg=f'Expected updated description is "{description}" but actual "{actual_updated_description}"')

        actual_updated_theme = self.site.home.super_button_section.super_button.theme
        self.assertIn(self.theme.replace('_', '').upper(), actual_updated_theme.upper(),
                      msg=f'expected updated theme is {self.theme.replace("_", "")} not in actual {actual_updated_theme}')
        return res

    def get_super_button_status(self, sb_name=None, expected_result=True, time=1, page="", refresh=False):
        wait_for_haul(1)
        if time > 60:
            return not expected_result
        if refresh:
            self.device.refresh_page()
        wait_for_haul(2)
        page = self.site.cricket if page == 'cricket' else self.site.home
        fe_super_button = page.super_button_section.super_button.button.name if page.has_quick_link_section() else ""
        actual_result = fe_super_button.upper() == sb_name.upper()
        self._logger.info(f"actual result in  {actual_result}")
        if expected_result == actual_result:
            return expected_result
        else:
            return self.get_super_button_status(sb_name=sb_name, expected_result=expected_result, time=time+1, page=page)

    def get_todays_racing_url(self):
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        event_hub_tab_data = next((tab for tab in module_ribbon_tabs if
                                  tab['title'].upper() == self.mrt_tab_name), None)
        if event_hub_tab_data and not event_hub_tab_data.get('visible'):
            event_hub_tab_data = None
        if not event_hub_tab_data:
            existing_event_hubs = self.cms_config.get_event_hubs()
            existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
            index_number = next(index for index in range(1, 20) if index not in existed_index_number)
            self.cms_config.create_event_hub(index_number=index_number)
            internal_id = f'tab-eventhub-{index_number}'
            event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=index_number,
                                                                               display_date=True, title=self.mrt_tab_name)
        home_tabs.append(event_hub_tab_data.get('url'))
        return home_tabs

    def get_target_uri(self):
        try:
            event = self.get_active_events_for_category(category_id=10)[0]
            event_id = event['event']['id']
            self.event_ids.append(event['event']['id'])
            target_url = f'/event/{event_id}'
        except SiteServeException:
            target_url = '/sport/football'
        return target_url

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case is to validate the multiple super buttons are displaying on same sport pages as per CMS configuration
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2)
        PRECONDITIONS: Ladbrokes:
        PRECONDITIONS: Navigate to Homepage -&gt; Super button -&gt; Click on Create super button link
        PRECONDITIONS: Coral:
        PRECONDITIONS: Navigate to Sport pages -&gt; Super button -&gt; Click on Create Super button link
        PRECONDITIONS: 3) Check on the Active check box
        PRECONDITIONS: 4) Enter the valid data for following fields
        PRECONDITIONS: a. Select CTA Alignment from Drop down
        PRECONDITIONS: b. Give valid title for Center Aligned CTA Title
        PRECONDITIONS: c. Give valid description for Center Aligned Description
        PRECONDITIONS: d. Give valid url for Destination URL
        PRECONDITIONS: e. Select tabs from drop down for Show on Home Tabs
        PRECONDITIONS: (ex: TODAY'S RACING)
        PRECONDITIONS: f. Select sports from drop down for Show on Sports
        PRECONDITIONS: (ex: Cricket)
        PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions (ex: World cup)
        PRECONDITIONS: h. Set Validity Period Start Date and Time (Current date and Time)
        PRECONDITIONS: (ex: 9/7/2023 and 2:16:00 PM)
        PRECONDITIONS: i. Set Validity Period End date and Time (Future date and Time)
        PRECONDITIONS: (ex: 9/7/2023 and 6:00:00 PM)
        PRECONDITIONS: j. Select Themes from Drop down
        PRECONDITIONS: k. Select Universal radio button
        PRECONDITIONS: l.Click on Create link
        PRECONDITIONS: 5) Create one more super button
        PRECONDITIONS: with following above config in CMS but need to select different Start time and different end time
        PRECONDITIONS: (Future and Future time for start and end)
        PRECONDITIONS: (ex: Start date and time is 9/7/2023 and 4:00:00 PM
        PRECONDITIONS: end date and time is 9/7/2023 and 7:00:00 PM)
        PRECONDITIONS: Note: Both Super buttons should be configured on same sport pages (ex: Cricket, Volleyball).
        """
        self.disable_all_other_super_buttons()
        self.__class__.supper_button_response_1 = self.cms_config.add_mobile_super_button(category_id=[10],
                                                                                          competition_id=[],
                                                                                          ctaAlignment='center',
                                                                                          description='Auto Test Super Button. DO NOT EDIT/DELETE it',
                                                                                          home_tabs=self.get_todays_racing_url(),
                                                                                          target_uri=self.get_target_uri(),
                                                                                          themes=self.theme
                                                                                          )

        display_from = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
                                               url_encode=False, days=1)[:-3] + 'Z'
        display_to = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
                                               url_encode=False, days=2)[:-3] + 'Z'
        self.__class__.supper_button_response_2 = self.cms_config.add_mobile_super_button(category_id=[10],
                                                                                          competition_id=[],
                                                                                          ctaAlignment='center',
                                                                                          description='Auto Test Super Button. DO NOT EDIT/DELETE it',
                                                                                          home_tabs=self.get_todays_racing_url(),
                                                                                          target_uri=self.get_target_uri(),
                                                                                          validity_period_start=display_from,
                                                                                          validity_period_end=display_to
                                                                                          )
        wait_for_haul(30)

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues
        """
        self.site.wait_content_state(state_name='Home')
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        self._logger.info(f'HOME PAGE TABS : {home_page_tabs}')
        wait_for_result(
            lambda: self.mrt_tab_name in list(self.site.home.tabs_menu.items_as_ordered_dict.keys()),
            timeout=15,
            name=f"{self.mrt_tab_name} mrt tab is not in {list(self.site.home.tabs_menu.items_as_ordered_dict.keys())}",
            expected_result=True
        )
        fe_today_racing_tab = next((tab for name, tab in home_page_tabs.items() if name.upper() == self.mrt_tab_name),
                                   None)
        try:
            self.assertIsNotNone(fe_today_racing_tab, 'Todays Racing Tab is not visible in frontend')
        except:
            wait_for_haul(5)
            self.device.refresh_page()
            self.site.wait_content_state(state_name='Home')
            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            self._logger.info(f'HOME PAGE TABS : {home_page_tabs}')
            wait_for_result(
                lambda: self.mrt_tab_name in list(self.site.home.tabs_menu.items_as_ordered_dict.keys()),
                timeout=15,
                name=f"{self.mrt_tab_name} mrt tab is not in {list(self.site.home.tabs_menu.items_as_ordered_dict.keys())}",
                expected_result=True
            )
            fe_today_racing_tab = next(
                (tab for name, tab in home_page_tabs.items() if name.upper() == self.mrt_tab_name),
                None)
            self.assertIsNotNone(fe_today_racing_tab, 'Todays Racing Tab is not visible in frontend')
        fe_today_racing_tab.click()
        wait_for_haul(2)

    def test_002_verify_newly_created_super_button_on_home_page_fe(self, page="", sb_response=None):
        """
        DESCRIPTION: verify newly created Super button on Home page (FE)
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config
        """
        sb_response = self.supper_button_response_1 if not sb_response else sb_response
        status = self.get_super_button_status(page=page, sb_name=sb_response['title'], expected_result=True, refresh=True)
        self.assertTrue(status, msg=f'Super button {sb_response["title"]} is not displayed')
        page = self.site.cricket if page == 'cricket' else self.site.home
        self.__class__.fe_supper_button = page.super_button_section.super_button
        self.fe_supper_button.scroll_to_we()
        self.assertEqual(self.fe_supper_button.button.name.upper(), sb_response['title'].upper(),
                         msg=f'Actual button name "{self.fe_supper_button.button.name}" is not same as '
                             f'Expected button name {sb_response["title"]}')

        self.assertEqual(self.fe_supper_button.description.upper(),
                         sb_response['description'].upper(),
                         f'actual description: \n "{self.fe_supper_button.description.upper()}" \n is not equal to \n '
                         f'expected description : \n "{sb_response["description"].upper()}"')

    def test_003_verify_the_alignment_of_cta_as_per_cms_config(self, page=None):
        """
        DESCRIPTION: Verify the alignment of CTA as per CMS config
        EXPECTED: Alignment of CTA should be displayed as per CMS config
        """
        page = self.site.home if not page else self.site.home
        center_aligned = page.super_button_section.cta_alignment
        self.assertEqual(center_aligned, 'center', f'super button is not aligned to center')

    def test_004_verify_the_title_of_cta_button_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the title of CTA button as per CMS Config
        EXPECTED: Title of CTA button should be displayed as per CMS config
        """
        # covered in above step


    def test_005_verify_the_description_for_right_aligned_cta_of_super_button__as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the description for Right Aligned CTA of Super button  as per the CMS config
        EXPECTED: Description should be displayed for Right Aligned CTA of Super button  as per the CMS config
        """
        # covered in Right Aligned test case

    def test_006_validate_the_theme_of_super_button_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the theme of Super button as per CMS config
        EXPECTED: Theme of Super button should be as per CMS config
        """
        self.assertEqual(self.theme.replace('_', '').upper(), self.fe_supper_button.theme.upper(),
                      f'theme is not same as cms config, actual theme : "{self.theme}" , '
                      f'expected theme : "{self.fe_supper_button.theme.upper()}')

    def test_007_validate_the_super_button_display_in_all_home_tabs_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Home tabs as per CMS config
        EXPECTED: Super button should be displayed in Home tabs as per the CMS Config
        """
        # covered in above step

    def test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config(self, sb_response=None):
        """
        DESCRIPTION: Validate the Super button display in all sport pages as per CMS config
        EXPECTED: Super button should be displayed in Sport pages as per CMS config
        """
        sb_response = self.supper_button_response_1 if not sb_response else sb_response
        url = f'https://{tests.HOSTNAME}/sport/cricket'
        self.device.navigate_to(url=url, testautomation=True)
        self.site.wait_splash_to_hide()
        self.test_002_verify_newly_created_super_button_on_home_page_fe(page='cricket', sb_response=sb_response)

    def test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Big competition hub as per CMS config
        EXPECTED: Super button should be displayed in Big competition hubs as per CMS config
        """
        # covered in C65934235

    def test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config(self, sb=1):
        """
        DESCRIPTION: Click on the Super button and validate the navigating URL as per the CMS config
        EXPECTED: Should be navigate to exact url and page as per CMS config after clicking on Super button
        """
        self.fe_supper_button.button.click()
        if len(self.event_ids) > 0:
            self.site.wait_content_state_changed()
            wait_for_result(
                lambda: self.event_ids[sb - 1] in self.device.get_current_url(),
                timeout=15,
                name=f"{self.event_ids[sb - 1]} event id displayed in current url {self.device.get_current_url()}",
                expected_result=True
            )
            self.assertIn(self.event_ids[sb - 1], self.device.get_current_url(),
                          f'navigation is not done as per cms config. event id "{self.event_ids[sb - 1]}" , '
                          f'current url: "{self.device.get_current_url()}"')
        else:
            self.site.wait_content_state('Football')

    def test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config(self, sb_response=None):
        """
        DESCRIPTION: Verify the validity of super button start and end date, as per the CMS config
        EXPECTED: Super button should be display and disappear in FE as per the CMS config of Validity time period start and end date, time
        """
        sb_response = self.supper_button_response_1 if not sb_response else sb_response
        url = f'https://{tests.HOSTNAME}/sport/cricket'
        self.device.navigate_to(url=url, testautomation=True)
        self.site.wait_splash_to_hide()
        self.__class__.fe_supper_button = self.site.cricket.super_button_section.super_button
        now = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format='%Y-%m-%dT%H:%M:%S.%f', url_encode=False)[:-3] + 'Z'
        validity_status = sb_response['validityPeriodStart'] < now < sb_response['validityPeriodEnd']
        self.assertTrue(validity_status, f'validity period is not same as per cms config')

    def test_012_verify_that_2nd_super_button_displaying_in_fe(self):
        """
        DESCRIPTION: Verify that 2nd super button displaying in FE
        EXPECTED: 2nd super button should not display until and unless 1st super button expire and disappears
        """
        if self.timezone.upper() == "UTC":
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                     url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                     url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            start_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                     url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'
        self.__class__.supper_button_response_1 = self.cms_config.update_mobile_super_button(name=self.supper_button_response_1['title'], validity_period_end=start_time_cms)
        self.__class__.supper_button_response_2 = self.cms_config.update_mobile_super_button(name=self.supper_button_response_2['title'], validity_period_start=start_time_cms)
        wait_for_haul(60)
        self.device.refresh_page()
        sb_status = self.get_super_button_status(sb_name=self.supper_button_response_1['title'], expected_result=False,
                                                 page='cricket', refresh=True)
        self.assertFalse(sb_status,
                        f"{self.supper_button_response_1['title']} is not displayed after display from started")
        sb_status = self.get_super_button_status(sb_name=self.supper_button_response_2['title'],
                                                 expected_result=True, page='cricket', refresh=True)
        self.assertTrue(sb_status, f'{self.supper_button_response_2["title"]} '
                                   f'is not displayed after display from started')

    def test_013_verify_1st_super_button_disappeared_after_end_date_and_time_as_per_cms_config(self):
        """
        DESCRIPTION: Verify 1st super button disappeared after end date and time as per CMS config
        EXPECTED: 1st super button should be stopped displaying once end date and time reached. 2nd super button should be displayed automatically once 1st Super button stopped displaying in Same sport pages
        """
        # covered in above step

    def test_014_repeat_1_11_steps_and_validate_for_2nd_super_button_which_created_for_same_sport_pages_with_different_start_and_different_end_time(self):
        """
        DESCRIPTION: Repeat 1-11 steps and validate for 2nd super button which created for Same sport pages with different start and different end time
        EXPECTED: 2nd super button should be display on sport pages as per the CMS config
        """
        url = f'https://{tests.HOSTNAME}/'
        self.device.navigate_to(url=url, testautomation=True)
        self.site.wait_splash_to_hide()
        self.test_001_hit_the_test_environment_url_to_launch_application()
        self.test_002_verify_newly_created_super_button_on_home_page_fe(sb_response=self.supper_button_response_2)
        self.test_003_verify_the_alignment_of_cta_as_per_cms_config()
        self.test_004_verify_the_title_of_cta_button_as_per_cms_config()
        self.test_005_verify_the_description_for_right_aligned_cta_of_super_button__as_per_the_cms_config()
        self.test_006_validate_the_theme_of_super_button_as_per_cms_config()
        self.test_007_validate_the_super_button_display_in_all_home_tabs_as_per_cms_config()
        self.test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config(sb_response=self.supper_button_response_2)
        self.test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config()
        self.test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config(sb=2)
        self.test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config(sb_response=self.supper_button_response_2)

    def test_015_verify_2nd_super_button_title_description_theme_and_navigating_url(self):
        """
        DESCRIPTION: Verify 2nd Super button Title, description, Theme and navigating URL
        EXPECTED: 2nd Super button should be display on tabs with title, description, theme and navigation as per CMS config
        """
        # covered in above steps

    def test_016_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        self.__class__.theme = 'theme_2'
        self.__class__.supper_button_response_2 = self.update_and_check(page='cricket',
                                                                        sb_response=self.supper_button_response_2,
                                                                        description="Updated Description Before Login")
        url = f'https://{tests.HOSTNAME}/'
        self.device.navigate_to(url=url, testautomation=True)
        self.site.wait_splash_to_hide()
        self.site.login()

    def test_017_repeat_all_above_steps(self):
        """
        DESCRIPTION: Repeat all above steps
        EXPECTED: All steps should work as expected
        """
        self.test_014_repeat_1_11_steps_and_validate_for_2nd_super_button_which_created_for_same_sport_pages_with_different_start_and_different_end_time()
        self.__class__.theme = 'theme_1'
        self.update_and_check(page='cricket',
                              sb_response=self.supper_button_response_2, description="Updated Description After Login")
