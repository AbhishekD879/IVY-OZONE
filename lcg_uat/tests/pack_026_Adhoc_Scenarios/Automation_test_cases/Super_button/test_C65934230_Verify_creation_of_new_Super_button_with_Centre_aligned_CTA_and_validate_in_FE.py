import pytest
import tests
from datetime import datetime
import random
from tzlocal import get_localzone
from tests.base_test import vtest
from tests.Common import Common
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65934230_Verify_creation_of_new_Super_button_with_Centre_aligned_CTA_and_validate_in_FE(Common):
    """
    TR_ID: C65934230
    NAME: Verify creation of new Super button with Centre aligned CTA and validate in FE
    DESCRIPTION: This test case is to validate Super button displaying in FE as per CMS configuration
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
    PRECONDITIONS: e. Select tabs from drop down for Show on Home Tabs (ex: Highlights)
    PRECONDITIONS: f. Select sports from drop down for Show on Sports (ex: Football)
    PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions (ex: World cup)
    PRECONDITIONS: h. Set Validity Period Start Date (ex- current date and time)
    PRECONDITIONS: i. Set Validity Period End date (Ex- Future date and time)
    PRECONDITIONS: j. Select Themes from Drop down
    PRECONDITIONS: k. Select Universal radio button
    PRECONDITIONS: l. Click on Create link
    PRECONDITIONS: Note: Set newly created super button should  be on top order in the list of all super buttons.
    """
    keep_browser_open = True
    super_button_name = f'Auto_sb_{random.randint(1, 1000)}'
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    timezone = str(get_localzone())
    disabled_super_buttons = []
    tab_names = ['/home/featured']

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=16):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            home_tabs = self.tab_names
            if supper_button.get('enabled') and (
                    category_id in supper_button.get('categoryId') or home_tabs[0] in supper_button.get('homeTabs')):
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

    def get_super_button(self, page='home', expected_result=True):
        super_button = None
        if page == 'home':
            super_button = wait_for_cms_reflection(lambda: self.site.home.super_button_section, ref=self,
                                                   timeout=3, refresh_count=3, haul=3, expected_result=expected_result)
        elif page == 'football':
            super_button = wait_for_cms_reflection(lambda: self.site.football.super_button_section, ref=self,
                                                   timeout=3, refresh_count=3, haul=3, expected_result=expected_result)
        return super_button

    def test_000_preconditions(self):
        """
        DESCRIPTION: Super Button creation
        """
        self.disable_all_other_super_buttons()

        destination_url = '/sport/football/matches'
        date_to = get_date_time_as_string(time_format=self.time_format, days=1)[:-3] + 'Z'

        # Current time + 1 minute
        if self.timezone.upper() == "UTC":
            date_from = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_from = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            date_from = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'

        self.__class__.super_button = self.cms_config.add_mobile_super_button(name=self.super_button_name,
                                                                              home_tabs=self.tab_names,
                                                                              category_id=[16], ctaAlignment='center',
                                                                              validity_period_start=date_from,
                                                                              validity_period_end=date_to,
                                                                              target_uri=destination_url,
                                                                              competition_id=[])

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues.
        EXPECTED: By default home/featured tab should be loaded
        """
        self.site.wait_content_state('Homepage')
        current_tab = self.site.home.tabs_menu.current.upper()
        self.__class__.expected_tab = 'FEATURED' if self.brand == 'bma' else 'HIGHLIGHTS'  # checking the featured tab
        self.assertEqual(current_tab, self.expected_tab,
                         msg=f'current tab {current_tab} is not equal to expected {self.expected_tab}')

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: Verify newly created Super button on Home page (FE).
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config.
        EXPECTED: Super button will not be displayed If current date and time is before the configured start date and time
        """
        # super button should not be displayed up to 1min from now
        sb_button = self.get_super_button(expected_result=False)
        if sb_button:
            super_button = sb_button.super_button.button.name.upper()
            self.assertNotEqual(super_button, self.super_button_name.upper(),
                                msg=f'super button {self.super_button_name} is displayed')
        self.assertFalse(sb_button, msg=f'super button {self.super_button_name} is displayed')
        wait_for_haul(60)
        self.__class__.super_button_fe = self.get_super_button()
        super_button = self.super_button_fe.super_button.button.name
        self.assertEqual(super_button.upper(), self.super_button_name.upper(),
                         msg=f'Expected name {self.super_button_name.upper()} is not equal to Actual name {super_button.upper()}')

    def test_003_verify_the_alignment_of_cta_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the alignment of CTA as per CMS config
        EXPECTED: Alignment of CTA should be displayed as per CMS config
        """
        # Alignment
        self.__class__.super_button_fe = self.get_super_button()
        super_button_alignment = self.super_button_fe.cta_alignment
        self.assertEqual(super_button_alignment, self.super_button['ctaAlignment'], msg=f'Expected Alignment {self.super_button["ctaAlignment"]} is '
                                                                                        f'not equal to {super_button_alignment}')

    def test_004_verify_the_title_of_cta_button_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the title of CTA button as per CMS Config
        EXPECTED: Title of CTA button should be displayed as per CMS config
        """
        super_button = self.super_button_fe.super_button.button.name
        self.assertEqual(super_button.upper(), self.super_button['title'].upper(),
                         msg=f'Actual super button is {super_button.upper()}, But expected super button is '
                             f'{self.super_button["title"].upper()}')

    def test_005_verify_the_description_for_center_aligned_cta_of_super_button__as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the description for Center Aligned CTA of Super button  as per the CMS config
        EXPECTED: Description should be displayed for Center Aligned CTA of Super button  as per the CMS config
        """
        super_button_description = self.super_button_fe.super_button.description
        self.assertEqual(super_button_description.upper(), self.super_button['description'].upper(),
                         msg=f"Actual super button description is{super_button_description.upper()}, But expected is {self.super_button['description'].upper()}")

    def test_006_validate_the_theme_of_super_button_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the theme of Super button as per CMS config
        EXPECTED: Theme of Super button should be as per CMS config
        """
        super_button_theme = self.super_button_fe.super_button.theme
        self.assertEqual(super_button_theme.upper(), self.super_button['themes'].upper().replace("_", ""),
                         msg=f'Expected super button theme {super_button_theme.upper()} is not equal to {self.super_button["themes"].upper().replace("_", "")} ')

    def test_007_validate_the_super_button_display_in_all_home_tabs_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Home tabs as per CMS config
        EXPECTED: Super button should be displayed in Home tabs as per the CMS Config
        """
        # Covered in step 02

    def test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all sport pages as per CMS config
        EXPECTED: Super button should be displayed in Sport pages as per CMS config
        """
        # Super button validated on football sport page
        self.site.open_sport(name='FOOTBALL')
        super_button = self.get_super_button(page='football').super_button.button.name
        self.assertEqual(super_button.upper(), self.super_button_name.upper(), msg='Suber button is displayed ')

    def test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Big competition hub as per CMS config
        EXPECTED: Super button should be displayed in Big competition hubs as per CMS config
        """
        # This step is covered in C65934235

    def test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config(self):
        """
        DESCRIPTION: Click on the Super button and validate the navigating URL as per the CMS config
        EXPECTED: Should be navigate to exact URL and page as per CMS config after clicking on Super button
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')
        self.get_super_button().super_button.button.click()
        wait_for_haul(1)
        current_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}' + self.super_button.get('targetUri')
        self.assertEqual(current_url, expected_url, msg=f'actual url {current_url}, expected url is {expected_url}')

    def test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the validity of super button start and end date as per the CMS config
        EXPECTED: Super button should be display and disappear in FE as per the CMS config of Validity time period start and end date
        """
        # Current time + 1 minute. super button will expire after 1 min
        if self.timezone.upper() == "UTC":
            date_to = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                              minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_to = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                              minutes=-59)[:-3] + 'Z'
        else:
            date_to = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                              hours=-5.5, minutes=1)[:-3] + 'Z'

        # update super button
        self.cms_config.update_mobile_super_button(name=self.super_button_name, validity_period_end=date_to)

        # super button displayed
        sb_button = self.get_super_button(page='football').super_button.button.name.upper()
        self.assertEqual(self.super_button_name.upper(), sb_button,
                         msg=f'Expected super button is {self.super_button_name}, But actual super button is {sb_button}')

        # super button not displayed
        wait_for_haul(60)
        sb_button = self.get_super_button(page='football', expected_result=False)
        self.assertFalse(sb_button, msg=f'super button is displayed ')

        # Back to home page
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

        # Again update the end time
        date_to = get_date_time_as_string(time_format=self.time_format, days=2)[:-3] + 'Z'
        self.cms_config.update_mobile_super_button(name=self.super_button_name, validity_period_end=date_to)

    def test_012_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        self.site.login()

    def test_013_repeat_all_above_steps(self):
        """
        DESCRIPTION: Repeat all above steps
        EXPECTED: Result should be as expected above
        """
        self.test_003_verify_the_alignment_of_cta_as_per_cms_config()
        self.test_004_verify_the_title_of_cta_button_as_per_cms_config()
        self.test_005_verify_the_description_for_center_aligned_cta_of_super_button__as_per_the_cms_config()
        self.test_006_validate_the_theme_of_super_button_as_per_cms_config()
        self.test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config()
        self.test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config()
        self.test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config()
        self.test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config()
