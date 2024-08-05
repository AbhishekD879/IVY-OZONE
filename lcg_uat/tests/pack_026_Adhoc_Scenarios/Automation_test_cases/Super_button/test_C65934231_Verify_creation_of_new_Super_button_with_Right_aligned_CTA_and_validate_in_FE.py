from datetime import datetime
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tzlocal import get_localzone

import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection
from crlat_cms_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
@vtest
class Test_C65934231_Verify_creation_of_new_Super_button_with_Right_aligned_CTA_and_validate_in_FE(Common):
    """
    TR_ID: C65934231
    NAME: Verify creation of new Super button with Right aligned CTA and validate in FE
    """
    keep_browser_open = True
    timezone = str(get_localzone())
    disabled_super_buttons = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=9):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            home_tabs = self.get_in_play_url()
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
        self._logger.info(f'{self.disabled_super_buttons}')

    def get_in_play_url(self):
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        inplay_tab = next((tab for tab in module_ribbon_tabs if
                                  tab['title'].upper() == "IN-PLAY"), None)
        if not (bool(inplay_tab) and inplay_tab.get('visible')):
            raise CMSException('todays racing tab is not configured or enabled in CMS')
        home_tabs.append(inplay_tab.get('url'))
        return home_tabs

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case is to validate Super button displaying in FE as per CMS configuration
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2)
        PRECONDITIONS: Ladbrokes:
        PRECONDITIONS: Navigate to Homepage -&gt; Super button -&gt; Click on Create super button link
        PRECONDITIONS: Coral:
        PRECONDITIONS: Navigate to Sport pages-&gt; Super button -&gt; Click on Create super button link
        PRECONDITIONS: 3) Check on the Active check box
        PRECONDITIONS: 4) Enter the valid data for following fields
        PRECONDITIONS: a. Select CTA Alignment from Drop down
        PRECONDITIONS: b. Give valid title for Center Aligned CTA Title
        PRECONDITIONS: c. Give valid description for Center Aligned Description
        PRECONDITIONS: d. Give valid URL for Destination URL
        PRECONDITIONS: e. Select tabs from drop down for Show on Home Tabs (ex: IN-PLAY)
        PRECONDITIONS: f. Select sports from drop down for Show on Sports(ex: Boxing)
        PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions (ex: World cup)
        PRECONDITIONS: h. Set Validity Period Start Date (ex- current date and time)
        PRECONDITIONS: i. Set Validity Period End date (Ex- Future date and time)
        PRECONDITIONS: j. Select Themes from Drop down
        PRECONDITIONS: k. Select Universal radio button
        PRECONDITIONS: l.Click on Create link
        PRECONDITIONS: Note: Set newly created super button should  be on top order in the list of all super buttons.
        """
        self.disable_all_other_super_buttons()
        self.__class__.super_button = self.cms_config.add_mobile_super_button(home_tabs = ['/home/in-play'],
                                                                              ctaAlignment = 'right',
                                                                              category_id = [9],
                                                                              competition_id = [],
                                                                              target_uri = '/sport/football/competitions')
        self.__class__.super_button_title = self.super_button.get('title').upper()
        self.__class__.tab_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                           raise_exceptions=True)
        self.assertTrue(self.tab_name,
                        msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play}" is not available')
    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues.
        EXPECTED: By default home/featured tab should be loaded
        """
        self.site.go_to_home_page()

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: verify newly created Super button on Home page in(FE)
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config.
        EXPECTED: Super button will not be displayed If current date and time is before the configured start date and time
        """
        tab_menus = self.site.home.module_selection_ribbon.tab_menu.items_names
        self.assertIn(self.tab_name, tab_menus ,msg=f'{self.tab_name} is not present inside {tab_menus}')
        if self.site.home.module_selection_ribbon.tab_menu.current != self.tab_name:
            self.site.home.module_selection_ribbon.tab_menu.click_button(self.tab_name)
        wait_for_cms_reflection(
            lambda: self.site.home.super_button_section.super_button.button.name == self.super_button_title,
            ref=self, timeout=3, haul=5)
        has_super_button = self.site.home.super_button_section.super_button.has_button()
        self.assertTrue(has_super_button, msg=f'super button section is not available in home page')
        super_button_section = self.site.home.super_button_section.super_button
        super_button_section.scroll_to_we()
        actual_title = super_button_section.button.name
        self.assertEqual(actual_title.upper(), self.super_button_title, msg=f'{self.super_button_title} is not displaying on home page')

    def test_003_verify_the_alignment_of_cta_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the alignment of CTA as per CMS config
        EXPECTED: Alignment of CTA should be displayed as per CMS config
        """
        expected_super_button_alignment = self.super_button.get('ctaAlignment')
        actual_super_button_alignment = self.site.home.super_button_section.cta_alignment
        self.assertEqual(actual_super_button_alignment, expected_super_button_alignment, msg=f'actual alignment {actual_super_button_alignment} is not equal to expected alignment {expected_super_button_alignment}')

    def test_004_verify_the_title_of_cta_button_as_per_cms_config(self):
        """
        DESCRIPTION: Verify the title of CTA button as per CMS Config
        EXPECTED: Title of CTA button should be displayed as per CMS config
        """
        # already covered in above step

    def test_005_verify_the_description_for_right_aligned_cta_of_super_button__as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the description for Right Aligned CTA of Super button  as per the CMS config
        EXPECTED: Description should be displayed for Right Aligned CTA of Super button  as per the CMS config
        """
        actual_description = self.site.home.super_button_section.super_button.description
        expected_description = self.super_button.get('description')
        self.assertEqual(actual_description.upper(), expected_description.upper(), msg=f'actual description {actual_description.upper()} is not equal to expected description {expected_description.upper()}')

    def test_006_validate_the_theme_of_super_button_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the theme of Super button as per CMS config
        EXPECTED: Theme of Super button should be as per CMS config
        """
        actual_theme = self.site.home.super_button_section.super_button.theme
        expected_theme = self.super_button.get('themes').replace('_','')
        self.assertEqual(actual_theme, expected_theme, msg=f'actual theme {actual_theme} is not equal to expected theme {expected_theme}')

    def test_007_validate_the_super_button_display_in_all_home_tabs_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Home tabs as per CMS config
        EXPECTED: Super button should be displayed in Home tabs as per the CMS Config
        """
        # already covered in above step

    def test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all sport pages as per CMS config
        EXPECTED: Super button should be displayed in Sport pages as per CMS config
        """
        self.navigate_to_page(name='sport/boxing')
        self.site.wait_content_state_changed(timeout=5)
        wait_for_cms_reflection(lambda: self.site.boxing.super_button_section.super_button.button.name == self.super_button_title,
            ref=self, timeout=15, refresh_count=5, haul=5)
        super_button = self.site.boxing.super_button_section.super_button.has_button()
        self.assertTrue(super_button, msg=f'cta button for super button is not displayed in sport page')
        super_button_title = self.site.home.super_button_section.super_button.button.name
        self.assertEqual(super_button_title.upper(), self.super_button_title,
                         msg=f'{self.super_button_title} is not displaying on home page')

    def test_009_validate_the_super_button_display_in_all_big_competition_hub_as_per_cms_config(self):
        """
        DESCRIPTION: Validate the Super button display in all Big competition hub as per CMS config
        EXPECTED: Super button should be displayed in Big competition hubs as per CMS config
        """
        # covered in C65934235

    def test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config(self):
        """
        DESCRIPTION: Click on the Super button and validate the navigating URL as per the CMS config
        EXPECTED: Should be navigate to exact URL and page as per CMS config after clicking on Super button
        """
        self.site.boxing.super_button_section.super_button.button.click()
        current_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}'+self.super_button.get('targetUri')
        self.assertEqual(expected_url, current_url, msg=f'expected url {expected_url} not in actual url {current_url}')

    def test_011_verify_the_validity_of_super_button_start_and_end_date_as_per_the_cms_config(self):
        """
        DESCRIPTION: Verify the validity of super button start and end date as per the CMS config
        EXPECTED: Super button should be display and disappear in FE as per the CMS config of Validity time period start and end date
        """
        # already covered in above steps

    def test_012_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        self.site.login()

    def test_013_repeat_all_above_steps(self):
        """
        DESCRIPTION: Repeat all above steps
        EXPECTED: should work as expected
        """
        self.test_001_hit_the_test_environment_url_to_launch_application()
        self.test_002_verify_newly_created_super_button_on_home_page_fe()
        self.test_003_verify_the_alignment_of_cta_as_per_cms_config()
        self.test_005_verify_the_description_for_right_aligned_cta_of_super_button__as_per_the_cms_config()
        self.test_006_validate_the_theme_of_super_button_as_per_cms_config()
        self.test_008_validate_the_super_button_display_in_all_sport_pages_as_per_cms_config()
        self.test_010_click_on_the_super_button_and_validate_the_navigating_url_as_per_the_cms_config()
