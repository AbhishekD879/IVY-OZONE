from datetime import datetime
import pytest
import tests
import datetime as dt
from faker import Faker
from tests.base_test import vtest
from tzlocal import get_localzone
from tests.Common import Common
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


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
class Test_C65939821_Verify_sorting_order_of_super_button_and_validate(Common):
    """
    TR_ID: C65939821
    NAME: Verify sorting order of super button and validate
    DESCRIPTION: This test case is to validate sorting order of Super button displaying in FE as per CMS configuration
    PRECONDITIONS: " 1) User should have oxygen CMS access
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
    PRECONDITIONS: f. Select sports from drop down for Show on Sports
    PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions
    PRECONDITIONS: h. Set Validity Period Start Date (ex- current date and time)
    PRECONDITIONS: i. Set Validity Period End date (Ex- Future date and time)
    PRECONDITIONS: j. Select Themes from Drop down
    PRECONDITIONS: k. Select Universal radio button
    PRECONDITIONS: l.Click on Create link
    PRECONDITIONS: 5) Create one more super button with same start date, start time, end date and end time of validity period of super button
    PRECONDITIONS: Note: Set newly created super button should  be on top order in the list of all super buttons.
    PRECONDITIONS: and Super buttons should  be active and running."
    """
    keep_browser_open = True
    destination_url = f'/sport/tennis/competitions'
    faker = Faker()
    competition_name = f'Auto big competition {faker.name()}'
    new_id = faker.random.randint(200, 1000)
    now = datetime.now()
    timezone = str(get_localzone())
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                      minutes=30)[:-3] + 'Z'

    # Creating big_competition
    def create_big_competition_and_sport_category(self, type_id):

        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=type_id, competition_name=self.competition_name)
        # Assign IDs and URIs from the new competition data
        self.__class__.new_competition_id = f"{new_competition.get('id')}"
        self.__class__.new_competition_uri = new_competition.get('uri')
        # Construct the URL for the new category
        new_category_ulr = f'big-competition{self.new_competition_uri}'
        # Create a new tab under the created Big competition
        new_tab_id = self.cms_config.create_tab_for_big_competition(competition_id=self.new_competition_id,
                                                                    tab_name='highlight').get('id')
        # Wait for a short time
        wait_for_haul(2)

        # Create a new module under the previously created big competition tab.
        # This module is necessary to house the super button for the big competition.
        # The super button will be positioned on top of this module.
        self.cms_config.create_module_for_big_competation(competition_id=self.new_competition_id,
                                                          tab_id=new_tab_id, module_name='surfaceBet',
                                                          module_type='SURFACEBET')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new sport category for the Big competition which is created
        self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                              ssCategoryCode=self.new_id, targetUri=new_category_ulr,
                                              tier='UNTIED', showInAZ=True, showInHome=True)

    def create_eventhub_and_add_it_to_sport_module_and_featured_tab(self, event_id):

        # Retrieve all existing event hubs from the CMS configuration.
        existing_event_hubs = self.cms_config.get_event_hubs()

        # maximum number of allowed eventhub is 6
        if len(existing_event_hubs) >= 6:
            # Get all module ribbon tabs
            all_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data

            # Filter inactive EventHub tabs using list comprehension
            all_inactive_eventhub_ids = [
                tab['internalId'].replace('tab-eventhub-', '')
                for tab in all_module_ribbon_tabs
                if tab.get('directiveName') == 'EventHub'
                   and (not tab.get('visible')
                        or dt.datetime.utcnow().isoformat() > tab.get('displayTo'))
            ]

            # Delete inactive EventHub modules
            for tab in existing_event_hubs:
                if str(tab.get('indexNumber')) in all_inactive_eventhub_ids:
                    self.cms_config.delete_event_hub_module(tab.get('id'))
                    break

        # Retrieve existing event hubs from the CMS configuration.
        existing_event_hubs = self.cms_config.get_event_hubs()

        # Extract the index numbers of existing event hubs.
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # Find the next available index number (from 1 to 19) that is not already in use.
        self.__class__.index_number = next(index for index in range(20, 30) if index not in existed_index_number)

        # Create a new event hub with the determined index number.
        self.cms_config.create_event_hub(index_number=self.index_number)

        # Add a sport module of type 'FEATURED' to the event hub.
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')

        # Add a featured tab module to the event hub, specifying various parameters.
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=event_id,
                                                              page_type='eventhub',
                                                              page_id=self.index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)

        # Set the module name to the uppercase version of its title.
        self.__class__.module_name = module_data['title'].upper()

        # Define an internal ID for the event hub tab.
        internal_id = f'tab-eventhub-{self.index_number}'

        # Create a tab for the event hub in module ribbon tabs with specified details.
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=self.index_number,
                                                                           display_date=True)

        # Set the event hub tab name to the uppercase version of its title.
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def verify_super_button_FE(self, title=None, description=None, theme=None, alignment=None,expected_result=True):
        if expected_result:
            self.assertTrue(self.site.home.super_button_section.super_button.has_button,
                            msg='Super button is not displayed')
            FE_super_button_name = self.site.home.super_button_section.super_button.button.name
            FE_super_button_description = self.site.home.super_button_section.super_button.description
            FE_super_button_ctaAlignment = self.site.home.super_button_section.cta_alignment
            FE_super_button_theme = self.site.home.super_button_section.super_button.get_attribute('class')
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
            self.assertFalse(self.site.home.has_quick_link_section(expected_result=False),
                             msg='Super button is displaying in FE')

    def changing_super_button_order(self, super_buttons_list=[]):
        all_sbs = self.cms_config.get_mobile_super_buttons()
        sb_ids = []
        for i in range(len(super_buttons_list)):
            for sb in all_sbs:
                if sb.get('title').upper() == super_buttons_list[i].upper():
                    sb_ids.append(sb.get('id'))
                    break
        all_sb_ids = [item['id'] for item in all_sbs]
        i = 0
        for sb_id in sb_ids:
            all_sb_ids.remove(sb_id)
            all_sb_ids.insert(i, sb_id)
            self.cms_config.set_superbutton_ordering(new_order=all_sb_ids, moving_item=sb_id)
            i += 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Super Button creation
        DESCRIPTION: Special Super Button creation
        """
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            event_id = event['event']['id']
            type_id = event['event']['typeId']
        else:
            # Add a new football event to the England Premier League and Assign event ID based on the added event
            event = self.ob_config.add_football_event_to_england_premier_league()
            event_id = event.event_id
            type_id = event.ss_response['event']['typeId']

        self.create_big_competition_and_sport_category(type_id=type_id)

        self.create_eventhub_and_add_it_to_sport_module_and_featured_tab(event_id=event_id)

        wait_for_haul(20)

        self.__class__.super_button_data = self.cms_config.add_mobile_super_button(home_tabs=[f"/home/eventhub/{self.index_number}"],
                                                                                   target_uri=self.destination_url,
                                                                                   validity_period_start=self.date_from,
                                                                                   validity_period_end=self.date_to,
                                                                                   competition_id=[self.new_competition_id]
                                                                                   )
        self.__class__.super_button_cms_url = self.super_button_data['targetUri']

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues.
        EXPECTED: By default home/featured tab should be loaded
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        wait_for_cms_reflection(
            lambda: self.site.home.super_button_section.super_button.button.name == self.super_button_title,
            ref=self, timeout=3, haul=5, refresh_count=2)
        self.site.wait_content_state_changed()

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: Verify newly created Super button on Home page (FE).
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config.
        EXPECTED: Super button will be displayed in FE which is on top of order as per CMS config (1st super button)
        """
        self.verify_super_button_FE(title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment']
                                    )

    def test_003_verify_the_title_of_cta_button_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the title of CTA button as per CMS Config
        EXPECTED: Title of CTA button should be displayed as per CMS config
        """
        # Covered in above step

    def test_004_verify_the_description_for_center_aligned_cta_of_super_button__as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the description for Center Aligned CTA of Super button  as per the CMS config
        EXPECTED: Description should be displayed for Center Aligned CTA of Super button  as per the CMS config
        """
        # covered in above step

    def test_005_validate_the_super_button_display_in_all_home_tabs_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Home tabs as per CMS config
        EXPECTED: Super button should be displayed in Home tabs as per the CMS Config
        """
        # covered in above step

    def test_006_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        self.site.login()

    def test_007_repeat_all_above_steps(self):
        """
        DESCRIPTION: Repeat all above steps
        EXPECTED: Result should be as expected above
        """
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        self.verify_super_button_FE(title=self.super_button_data['title'],
                                    description=self.super_button_data['description'],
                                    theme=self.super_button_data['themes'].replace('_', ''),
                                    alignment=self.super_button_data['ctaAlignment']
                                    )

    def test_008_in_cms_change_the_2nd_super_button_order_to_the_top_on__super_button_list(self):
        """
        DESCRIPTION: In CMS, Change the 2nd super button order to the top on  super button list
        EXPECTED: 2nd  super button should be on top order in CMS
        """
        self.__class__.super_button_data2 = self.cms_config.add_mobile_super_button(home_tabs=[f"/home/eventhub/{self.index_number}"],
                                                                                    target_uri=self.destination_url,
                                                                                    validity_period_start=self.date_from,
                                                                                    validity_period_end=self.date_to,
                                                                                    competition_id=[self.new_competition_id]
                                                                                    )
        sb_titles = [self.super_button_data2['title'], self.super_button_data['title']]
        self.changing_super_button_order(super_buttons_list=sb_titles)

    def test_009_go_to_fe_and_verify_2nd_super_button_displaying_or_not(self):
        """
        DESCRIPTION: Go to FE and verify 2nd super button displaying or not
        EXPECTED: 2nd super button which is moved to top order should be displayed in FE.
        EXPECTED: 1st super button should not be displayed in FE
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=20)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=20)
        self.verify_super_button_FE(title=self.super_button_data2['title'],
                                    description=self.super_button_data2['description'],
                                    theme=self.super_button_data2['themes'].replace('_', ''),
                                    alignment=self.super_button_data2['ctaAlignment']
                                    )

    def test_010_verify_the_title_of_cta_button_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the title of CTA button as per CMS Config
        EXPECTED: Title of CTA button should be displayed as per CMS config
        """
        # Covered in above step

    def test_011_verify_the_description_for_center_aligned_cta_of_super_button__as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the description for Center Aligned CTA of Super button  as per the CMS config
        EXPECTED: Description should be displayed for Center Aligned CTA of Super button  as per the CMS config
        """
        # Covered in above step

    def test_012_logout_from_the_application_and_verify_display_of_2nd_super_button_in_fe(self):
        """
        DESCRIPTION: Logout from the application and verify display of 2nd super button in FE
        EXPECTED: 2nd super button should be displayed in FE post logout as per CMS config
        """
        self.site.logout()
        self.navigate_to_page(f"/home/eventhub/{self.index_number}")
        self.verify_super_button_FE(title=self.super_button_data2['title'],
                                    description=self.super_button_data2['description'],
                                    theme=self.super_button_data2['themes'].replace('_', ''),
                                    alignment=self.super_button_data2['ctaAlignment']
                                    )

