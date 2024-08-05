import random
from datetime import datetime
import pytest
import tests
from tzlocal import get_localzone
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec



@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65934235_Verify_displaying_of_super_button_for_segmented_user(Common):
    """
    TR_ID: C65934235
    NAME: Verify displaying of super button for segmented user.
    DESCRIPTION: This test case is to validate the super button is displaying as per CMS configuration
    PRECONDITIONS: 1) Login to oxygen CMS.
    PRECONDITIONS: 2)
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: Navigate to Homepage -&gt; Super button
    PRECONDITIONS: Coral:
    PRECONDITIONS: Navigate to sports pages&gt;super button.
    PRECONDITIONS: 3) Click on create super button.
    PRECONDITIONS: 4) check active box then select any of the alignment from the dropdown.
    PRECONDITIONS: 5) Enter CTA title with combination of regular and special character (ex: #-@$&).
    PRECONDITIONS: 6) Enter description in aligned description field.
    PRECONDITIONS: 7) Enter destination URL.
    PRECONDITIONS: 8) Select any of the tab displayed in the  show on home tabs drop down (ex: LIVE STREAM).
    PRECONDITIONS: 9) Select any of the sport displayed on the show on sports drop down (ex: Table tennis).
    PRECONDITIONS: 10) Select any of the big competitions displayed on the show on big competitions  drop down (ex: World cup).
    PRECONDITIONS: 11) Enter start date and end date.
    PRECONDITIONS: 12) Select any of the themes from themes dropdown.
    PRECONDITIONS: 13) select segmented view and select any of the segment from the dropdown.
    PRECONDITIONS: 14) click on create button.
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    timezone = str(get_localzone())
    disabled_super_buttons = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=6, competition_id=''):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            if supper_button.get('enabled') and (
                    category_id in supper_button.get('categoryId') or competition_id in supper_button.get('competitionId') ):
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

    def verify_super_button_FE(self):
        self.assertTrue(self.site.basketball.super_button_section.super_button.has_button, msg='Super button is not displayed')
        fe_super_button_name = self.site.basketball.super_button_section.super_button.button.name.upper()
        fe_super_button_description = self.site.basketball.super_button_section.super_button.description.upper()
        fe_super_button_theme = self.site.basketball.super_button_section.super_button.theme.upper()
        fe_super_button_cta_alignment = self.site.basketball.super_button_section.cta_alignment.upper()
        self.assertEqual(fe_super_button_name, self.super_button_title,
                         msg=f'Actual button name "{fe_super_button_name}" is not same as '
                             f'Expected button name {self.super_button_title}')
        self.assertEqual(fe_super_button_description, self.super_button_description,
                         msg=f'Actual button description "{fe_super_button_description}" is not same as '
                             f'Expected button description {self.super_button_description}')
        self.assertEqual(fe_super_button_theme, self.super_button_theme,
                         msg=f'actual theme {fe_super_button_theme} is not equal to expected theme {self.super_button_theme}')
        self.assertEqual(fe_super_button_cta_alignment, self.super_button_cta_alignment,
                         msg=f'Actual alignment {fe_super_button_cta_alignment} is not same as the expected alignment {self.super_button_cta_alignment}')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Super Button
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        destination_uri = '/sport/basketball/matches'
        big_competitions = self.cms_config.get_big_competition()
        competitions_tab_id = None
        for competitions in big_competitions:
            if competitions['name'].upper() == "WORLD CUP":
                competitions_tab_id = competitions.get('id')
                break
        self.disable_all_other_super_buttons(competition_id=competitions_tab_id)
        created_super_button= self.cms_config.add_mobile_super_button(inclusionList=[vec.bma.CSP_CMS_SEGEMENT],
                                                                      universalSegment=False,
                                                                      category_id=[6],
                                                                      name='Auto-235' + f'{random.randint(1, 100000)}',
                                                                      ctaAlignment='center',
                                                                      description='Auto-super_button',
                                                                      home_tabs=[],
                                                                      target_uri=destination_uri,
                                                                      competition_id=[competitions_tab_id],
                                                                      themes='theme_2')
        self.__class__.super_button_title = created_super_button['title'].upper()
        self.__class__.super_button_description = created_super_button['description'].upper()
        self.__class__.super_button_theme = created_super_button.get('themes').replace('_', '').upper()
        self.__class__.super_button_target_uri = created_super_button['targetUri']
        self.__class__.super_button_cta_alignment = created_super_button['ctaAlignment'].upper()

    def test_001_launch_the_oxygen_application(self):
        """
        DESCRIPTION: Launch the oxygen application.
        EXPECTED: Application should be loaded successfully home tab should be loaded by default.
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User should be logged into application successfully.
        """
        self.site.login()

    def test_003_verify_configured_super_button_is_displaying_in_fe(self):
        """
        DESCRIPTION: Verify configured super button is displaying in FE.fc/
        EXPECTED: Super button should not be displayed on home screen and configured home tabs and sport tabs
        """
        self.navigate_to_page('/sport/basketball')
        actual_super_button_title = None
        if self.site.basketball.has_quick_link_section():
            actual_super_button_title = self.site.basketball.super_button_section.super_button.button.name.upper()
        self.assertNotEqual(self.super_button_title, actual_super_button_title,
                      msg=f'Expected superbutton {self.super_button_title}'
                          f'is shown in Basketball SLP')
        self.navigate_to_page(name='/')

    def test_004_now_go_to_dev_tools__ampgt_application__ampgt_click_on_local_storage__ampgt_select_test_environment_url_from_local_storage__ampgt_search_with_oxsegment_in_filter__ampgt_select_oxsegment_from_results__ampgt_enter_segmented_user_name_in__beside_segment_of_value_field__ampgt_then_refresh_the_page(self):
        """
        DESCRIPTION: Now Go to Dev tools -&amp;gt; Application -&amp;gt; Click on Local storage -&amp;gt; Select test environment url from Local storage -&amp;gt; Search with "ox.segment" in filter -&amp;gt; Select "OX.Segment" from results -&amp;gt; enter segmented user name in "" beside "segment" of Value field -&amp;gt; then refresh the page
        EXPECTED: Segmented user should be injected forcefully and Super button should be displayed in FE as per CMS config
        """

        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_005_now_validate_the_super_button_is_displaying_on_homepage(self):
        """
        DESCRIPTION: Now validate the super button is displaying on homepage.
        EXPECTED: Super button should be displayed on homepage.
        """
        self.navigate_to_page('/sport/basketball')
        available_super_buttons_in_basketball = self.site.basketball.super_button_section.super_button.button.name.upper()
        self.assertEqual(self.super_button_title, available_super_buttons_in_basketball, msg=f' Expected superbutton is  {self.super_button_title}'
                                                                               f'but actual is {available_super_buttons_in_basketball}  in Basketball SLP')

    def test_006_validate_the_alignment_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the alignment is displaying as per cms.
        EXPECTED: Super button alignment should be displayed as per cms.
        """
        self.verify_super_button_FE()

    def test_007_validate_the_title_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the title is displaying as per CMS.
        EXPECTED: The title should be same as per cms.
        """
        #Verified in above step

    def test_008_validate_the_description_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the description is displaying as per cms.
        EXPECTED: Description should be same as per cms.
        """
        #Verified in above step

    def test_009_navigate_to_configured_home_tabs_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to configured home tabs and validate the displaying of super button.
        EXPECTED: Super button should be displayed on home tabs.
        """
        #Verified in above step

    def test_010_navigate_to_configured_sports_tabs_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to configured sports tabs and validate the displaying of super button.
        EXPECTED: Super button should be displayed on sports tab
        """
        #Verified in above step

    def test_011_navigate_to_big_competitions_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to big competitions and validate the displaying of super button.
        EXPECTED: Super button should be displayed on big competition tab
        """
        self.navigate_to_page('/big-competition/world-cup')
        available_super_buttons_in_big_competitions = self.site.big_competitions.super_button_section.super_button.button.name.upper()
        self.assertEqual(self.super_button_title, available_super_buttons_in_big_competitions,
                         msg=f' Expected super button is  {self.super_button_title}'
                             f'but actual is {available_super_buttons_in_big_competitions} in big competitions.')

    def test_012_validate_the_theme_is_displaying_as_per_cms_configuration(self):
        """
        DESCRIPTION: validate the theme is displaying as per cms configuration.
        EXPECTED: Theme should be loaded successfully
        """
        actual_theme = self.site.big_competitions.super_button_section.super_button.theme.upper()
        expected_theme = self.super_button_theme
        self.assertEqual(actual_theme, expected_theme,
                         msg=f'actual theme {actual_theme} is not equal to expected theme {expected_theme}')

    def test_013_click_on_the_button_and_validate_the_destination_url(self):
        """
        DESCRIPTION: click on the button and validate the destination URL
        EXPECTED: User is navigated to the destination URL
        """
        self.site.big_competitions.super_button_section.super_button.button.click()
        self.site.wait_content_state_changed(timeout=20)
        actual_current_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}'+self.super_button_target_uri
        self.assertEqual(actual_current_url, expected_url, msg=f'Actual  destination uri {actual_current_url} is not' 
                                                               f' same as the  Expected target_uri {expected_url}')

