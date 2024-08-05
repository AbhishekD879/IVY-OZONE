from datetime import datetime

from selenium.common.exceptions import StaleElementReferenceException
from tzlocal import get_localzone
from faker import Faker
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
@vtest
# this test case covered C65934237
class Test_C65934232_Verify_multiple_super_buttons_configured_with_same_start_time_and_on_different_home_tabs(Common):
    """
    TR_ID: C65934232
    NAME: Verify multiple super buttons configured with same start time and on different home tabs
    DESCRIPTION: This test case is to validate the multiple super buttons are displaying at same time in different tabs as per CMS configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2)
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: Navigate to Homepage -&gt; Super button -&gt; Click on Create super button link
    PRECONDITIONS: coral:
    PRECONDITIONS: Navigate to Sport pages -&gt; Super button -&gt; Click on Create super button link
    PRECONDITIONS: 3) Check on the Active check box
    PRECONDITIONS: 4) Enter the valid data for following fields
    PRECONDITIONS: a. Select CTA Alignment from Drop down
    PRECONDITIONS: b. Give valid title for Center Aligned CTA Title
    PRECONDITIONS: c. Give valid description for Center Aligned Description
    PRECONDITIONS: d. Give valid URL for Destination URL
    PRECONDITIONS: e. Select tabs from drop down for Show on Home Tabs
    PRECONDITIONS: (ex: US sports)
    PRECONDITIONS: f. Select sports from drop down for Show on Sports
    PRECONDITIONS: (ex: Tennis)
    PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions
    PRECONDITIONS: h. Set Validity Period Start Date and Time (Current date and Time)
    PRECONDITIONS: i. Set Validity Period End date and Time (Future date and Time)
    PRECONDITIONS: j. Select Themes from Drop down
    PRECONDITIONS: k. Select Universal radio button
    PRECONDITIONS: l.Click on Create link
    PRECONDITIONS: 5) Create one more super button
    PRECONDITIONS: with following above config in CMS but need to select different tabs to display super button
    PRECONDITIONS: (ex: Home tabs - Next races)
    """
    keep_browser_open = True
    destination_url = f'/sport/tennis/competitions'
    faker = Faker()
    competition_name = f'Auto big competition {faker.name()}'
    competition_title = f'Auto{faker.name()}'
    new_id = faker.random.randint(200, 1000)
    now = datetime.now()
    home_tabs=[]
    timezone = str(get_localzone())
    disabled_super_buttons=[]
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                      minutes=30)[:-3] + 'Z'

    # get existing super buttons, and we are disabling existing super buttons
    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=34):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            home_tabs = self.home_tabs
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

    def verify_super_button_FE(self, title=None, description=None, theme=None, alignment=None, page_type=None,expected_result=True):
        if expected_result:
            if page_type == "Home":
                page = self.site.home
            elif page_type == "Tennis":
                page = self.site.tennis
            elif page_type == "Big Competition":
                page = self.site.big_competitions
            self.assertTrue(page.super_button_section.super_button.has_button,
                            msg='Super button is not displayed')
            FE_super_button_name = page.super_button_section.super_button.button.name
            FE_super_button_description = page.super_button_section.super_button.description
            FE_super_button_ctaAlignment = page.super_button_section.cta_alignment
            FE_super_button_theme = page.super_button_section.super_button.get_attribute('class')
            # Assertion on super button name as per CMS
            self.assertEqual(FE_super_button_name.upper(), title.upper(),
                             msg=f'Actual button name "{FE_super_button_name.upper()}" is not same as '
                                 f'Expected button name {title.upper()}')
            # Assertion on super button description as per CMs
            self.assertEqual(FE_super_button_description.upper(), description.upper(),
                             msg=f'Actual button description "{FE_super_button_description.upper()}" is not same as '
                                 f'Expected button description {description.upper()}')
            # Assertion on super button CTA alignment as per CMS
            self.assertEqual(FE_super_button_ctaAlignment.upper(), alignment.upper(),
                             msg=f'Actual button description "{FE_super_button_ctaAlignment.upper()}" is not same as '
                                 f'Expected button description {alignment.upper()}')
            # Assertion on super button theme as per CMS
            self.assertIn(theme.upper(), FE_super_button_theme.upper(),
                          msg=f'Actual theme "{theme.upper()}" is not in '
                              f'Expected  {FE_super_button_theme.upper()}')
        else:
            wait_for_cms_reflection(lambda : self.site.home.has_quick_link_section(expected_result=False),
                                    ref=self,
                                    timeout=30, refresh_count=10, haul=5, expected_result=False
                                    )
            self.assertFalse(self.site.home.has_quick_link_section(expected_result=False),
                             msg='Super button is displaying in FE')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Super Button
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        # Check if the environment is 'prod' for big_competition
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            self.__class__.typeid = event['event']['typeId']
        # getting tabs of module ribbon tab from cms and checking if any of them are event hub
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and
                                   tab['directiveName'] == 'EventHub' and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.event_hub_tab_name = next((tab.upper() for tab in self.tabs_cms if tab.upper() == 'US SPORTS'), None)
        self.__class__.index_number = None
        # getting index of the US SPORT event hub
        if self.event_hub_tab_name:
            self.__class__.index_number = next((tab['hubIndex'] for tab in module_ribbon_tabs if
                                            tab['title'].upper() == self.event_hub_tab_name.upper()), None)

        if self.event_hub_tab_name is None or self.index_number is None:
            #     Creating the eventhub
            existing_event_hubs = self.cms_config.get_event_hubs()
            existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

            # need a unique non-existing index for new Event hub
            self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)

            response = self.cms_config.create_event_hub(index_number=self.index_number)
            self.__class__.created_event_hub_id = response.get('id')
            #  Create the event hub name
            self.__class__.event_hub_name = f'Auto EventHub_{self.index_number}'
            #   Adding event hub to module ribbon tab
            internal_id = f'tab-eventhub-{self.index_number}'
            event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=self.index_number,
                                                                               display_date=True)
            self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=self.typeid,
                                                                 competition_name=self.competition_name,
                                                                 title=self.competition_title)
        # Assign IDs and URIs from the new competition data
        new_competition_id = new_competition.get('id')
        new_competition_uri = new_competition.get('uri')
        # Construct the URL for the new category
        self.__class__.new_category_ulr = f'big-competition{new_competition_uri}'
        # Create a new tab under the created Big competition
        new_tab_id = self.cms_config.create_tab_for_big_competition(competition_id=new_competition_id,
                                                                    tab_name='highlight').get('id')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new module under the tab which is created
        new_module = self.cms_config.create_module_for_big_competation(competition_id=new_competition_id,
                                                                       tab_id=new_tab_id, module_name='surfaceBet',
                                                                       module_type='SURFACEBET')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new sport category for the Big competition which is created
        self.__class__.new_sports = self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                                           ssCategoryCode=self.new_id, targetUri=self.new_category_ulr,
                                                           tier='UNTIED', showInAZ=True, showInHome=True)
        current_super_buttons = self.cms_config.get_mobile_super_buttons()

        self.__class__.home_tabs = [f'/home/eventhub/{self.index_number}']

        # disabling existing super buttons
        self.disable_all_other_super_buttons()

        self.__class__.super_button_data = self.cms_config.add_mobile_super_button(category_id=[34],
                                                                                   home_tabs=self.home_tabs,
                                                                                   target_uri=self.destination_url,
                                                                                   validity_period_start=self.date_from,
                                                                                   validity_period_end=self.date_to,
                                                                                   competition_id=[new_competition_id]
                                                                                   )
        self.__class__.super_button_cms_url = self.super_button_data['targetUri']

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues
        """
        self.site.wait_content_state('homepage')
        # getting tabs in home page tabs for mobile
        home_page_tabs = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict, timeout=20,
                                         name="waiting for the tab menu of the home page")
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        if self.event_hub_tab_name.upper() not in home_page_tab_names:
            home_page_tabs = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict.get(self.event_hub_tab_name), timeout=40,
                                             name="waiting for the tab menu of the home page",bypass_exceptions=(VoltronException, StaleElementReferenceException,AttributeError))
            home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        self.assertIn(self.event_hub_tab_name, home_page_tab_names,
                      f'Created Event Hub tab:{self.event_hub_tab_name} is not found in '
                      f'Current Home Page tabs : {home_page_tab_names}')
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),
                                       None)
        # navigating to the event hub tab which is created
        home_page_tabs.get(self.event_hub_tab_name).click()
        self.assertEqual(self.site.home.tabs_menu.current,
                         self.event_hub_tab_name,
                         f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: verify newly created Super button on Home page (FE)
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config
        """
        wait_for_cms_reflection(lambda: self.site.home.super_button_section, ref=self,
                                timeout=30, refresh_count=3, haul=5)
        self.verify_super_button_FE(page_type="Home", title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment']
                                    )

    def test_003_verify_the_alignment_of_cta_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the alignment of CTA as per CMS config
        EXPECTED: Alignment of CTA should be displayed as per CMS config
        """
        # covered in above step

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
        # covered in above step

    def test_006_validate_the_theme_of_super_button_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the theme of Super button as per CMS config
        EXPECTED: Theme of Super button should be as per CMS config
        """
        # Covered in above step

    def test_007_navigate_to_configured_home_tabs_of_1st_super_button_and_verify_the_presence(self):
        """
        DESCRIPTION: Navigate to configured home tabs of 1st super button and verify the presence.
        EXPECTED: 1st Super button should be displayed in all configured Home tabs as per the CMS Config.
        """
        # covered in step 2 calling verify

    def test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all sport pages as per CMS config
        EXPECTED: Super button should be displayed in Sport pages as per CMS config
        """
        self.site.open_sport(name='TENNIS')
        self.site.wait_content_state_changed(timeout=10)
        self.verify_super_button_FE(page_type="Tennis", title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment']
                                    )

    def test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Big competition hub as per CMS config
        EXPECTED: Super button should be disaplyed in Big competition hubs as per CMS config
        """
        self.navigate_to_page(self.new_category_ulr)
        self.site.wait_content_state_changed(timeout=20)
        self.verify_super_button_FE(page_type="Big Competition", title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment'])

    def test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config(self):
        """
        DESCRIPTION: Click on the Super button and validate the navigating url as per the CMS config
        EXPECTED: Should be navigate to exact URL and page as per CMS config after clicking on Super button
        """
        # click on super button
        self.site.big_competitions.super_button_section.super_button.button.click()
        self.site.wait_content_state('tennis')
        super_button_url = self.device.get_current_url()
        expected_url_from_cms = f'https://{tests.HOSTNAME}'+self.super_button_cms_url
        self.assertEqual(super_button_url, expected_url_from_cms,
                         msg=f'Current url: "{super_button_url}" is not the same as expected: "{expected_url_from_cms}"')

    def test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the validity of super button start and end date as per the CMS config
        EXPECTED: Super button should be display and disappear in FE as per the CMS config of Validity time period start and end date
        """
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'  # formatting the now time as CMS time format
        display_from = self.super_button_data['validityPeriodStart']
        display_to = self.super_button_data['validityPeriodEnd']
        status = display_from < now < display_to
        self.assertTrue(status, f'Super button is not displayed as per CMS configurations(in between start '
                                f'time and end time)')

    def test_012_repeat_all_above_steps_and_validate_for_2nd_super_button_which_created_for_different_tabs_to_display(
            self):
        """
        DESCRIPTION: Repeat all above steps and validate for 2nd super button which created for different tabs to display
        EXPECTED: Only 2nd super button should be display on tabs as per the CMS config.
        """
        # creating second super button in Live stream tab in home page
        self.__class__.second_super_button = self.cms_config.add_mobile_super_button(category_id=[34],
                                                                                     home_tabs=['/home/live-stream'],
                                                                                     target_uri=self.destination_url,
                                                                                     validity_period_start=self.date_from,
                                                                                     validity_period_end=self.date_to
                                                                                     )

    def test_013_verify_2nd_super_button_title_description_theme_and_navigating_url(self):
        """
        DESCRIPTION: Verify 2nd Super button Title, description, Theme and navigating URL
        EXPECTED: 2nd Super button should be display on tabs with title, description, theme and navigation as per CMS config
        """
        # navigating Live Stream
        self.navigate_to_page('/')
        home_page_tabs = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict, timeout=20,
                                         name="waiting for the tab menu of the home page")
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == 'LIVE STREAM'),
                                       None)
        self.assertIsNotNone(self.event_hub_tab_name, msg = f'LIVE STREAM tab is not Present')
        # navigating to the event hub tab which is LIVE STREAM
        home_page_tabs.get(self.event_hub_tab_name).click()
        wait_for_haul(10)
        self.assertEqual(self.site.home.tabs_menu.current,
                         self.event_hub_tab_name,
                         f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')

        # Verify FE validation of second Super Button
        self.device.refresh_page()
        wait_for_haul(10)
        self.verify_super_button_FE(page_type="Home", title=self.second_super_button['title'],
                                    description=self.second_super_button['description'],
                                    theme=self.second_super_button['themes'].replace('_', ''),
                                    alignment=self.second_super_button['ctaAlignment']
                                    )

    def test_014_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        # Login with valid user
        self.site.login()

    def test_015_navigate_to_1st_super_button_configured_home_tabs_and_validate_its_presence(self):
        """
        DESCRIPTION: Navigate to 1st Super button configured home tabs and validate its presence.
        EXPECTED: 1st super button should be displayed on configured tabs only
        """
        # Navigate to US SPORT or New Event hub AND verify super button
        home_page_tabs = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict, timeout=20,
                                         name="waiting for the tab menu of the home page")
        self.event_hub_tab_name = next((tab.upper() for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),
                                       None)
        # navigating to the event hub tab which is created
        home_page_tabs.get(self.event_hub_tab_name).click()
        self.site.wait_content_state_changed(timeout=20)
        self.assertEqual(self.site.home.tabs_menu.current,
                         self.event_hub_tab_name,
                         f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')

        # Verifying super button in US SPORT
        self.verify_super_button_FE(page_type="Home", title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment']
                                    )

    def test_016_navigate_to_2_nd_super_button_configured_home_tabs_and_validate_the_presence(self):
        """
        DESCRIPTION: Navigate to 2 nd Super button configured home tabs and validate the presence.
        EXPECTED: Only 2n d Super button should be displayed on configured tabs.
        EXPECTED: 1st Super button should not be displayed at all on those tabs.
        """
        home_page_tabs = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict, timeout=20,
                                         name="waiting for the tab menu of the home page")
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == 'LIVE STREAM'),
                                       None)
        # navigating to the event hub tab which is LIVE STREAM
        home_page_tabs.get(self.event_hub_tab_name).click()
        self.site.wait_content_state_changed(timeout=20)
        self.assertEqual(self.site.home.tabs_menu.current,
                         self.event_hub_tab_name,
                         f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')

        # Verify FE validation of second Super Button
        self.site.wait_content_state_changed(timeout=20)
        self.verify_super_button_FE(page_type="Home", title=self.second_super_button['title'],
                                    description=self.second_super_button['description'],
                                    theme=self.second_super_button['themes'].replace('_', ''),
                                    alignment=self.second_super_button['ctaAlignment']
                                    )
        # Inactive super button and verify FE
        self.cms_config.update_mobile_super_button(enabled=False,name=self.second_super_button['title'])
        self.device.refresh_page()
        wait_for_haul(20)
        self.verify_super_button_FE(expected_result=False)