import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone

from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65934234_Verify_and_create_super_button_using_special_character_in_CMS_and_check_the_same_in_Front_end(
    Common):
    """
    TR_ID: C65934234
    NAME: Verify and create super button using special character in CMS and check the same in Front end
    DESCRIPTION: This test case is to validate the super button is displaying as per CMS configuration
    PRECONDITIONS: 1) Login to oxygen CMS.
    PRECONDITIONS: 2) Navigate to sports pages&gt;super buttons.
    PRECONDITIONS: 3) Click on create super button.
    PRECONDITIONS: 4) check active box then select any of the alignment from the dropdown.
    PRECONDITIONS: 5) Enter CTA title with combination of regular and special character (Ex: @_&$)-.
    PRECONDITIONS: 6) Enter description in aligned description field.
    PRECONDITIONS: 7) Enter destination URL.
    PRECONDITIONS: 8) Select any of the tab displayed in the  show on home tabs drop down (Ex: World cup).
    PRECONDITIONS: 9) Select any of the sport displayed on the show on sports drop down (ex: Handball).
    PRECONDITIONS: 10) Select any of the big competitions displayed on the show on big competitions drop down (Ex: World cup).
    PRECONDITIONS: 11) Enter start date and end date.
    PRECONDITIONS: 12) Select any of the themes from themes dropdown.
    PRECONDITIONS: 14) click on create button.
    """
    keep_browser_open = True
    disabled_super_buttons = []
    timezone = str(get_localzone())
    TEST_CONFIG = {
        "super_button_title": "Auto_C65934234!&@#$%&*()^",
        "super_button_description": "Auto_C65934234_Description",
        "cta_alignment": "center",
        "theme": "theme_1",
        "sport": {
            "name": "handball",
            "category_id": 20,
            "url": ""
        },
        "hometab": {
            "name": "Accas" if tests.settings.brand == "ladbrokes" else "Football Accas",
            "url": ""
        }
    }

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        for supper_button in all_super_buttons:
            if self.TEST_CONFIG.get("sport").get("category_id") in supper_button.get("categoryId") or \
                    self.TEST_CONFIG.get("hometab").get("url") in supper_button.get("homeTabs"):
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

    def check_handball_enabled(self):
        all_sports_categories = self.cms_config.get_sport_categories()
        required_sport_tab = self.TEST_CONFIG.get('sport').get('name')
        filtered_tabs = list(filter(lambda sport_tab: sport_tab['imageTitle'].upper() == required_sport_tab.upper(),
                                    all_sports_categories))
        if not filtered_tabs:
            raise CmsClientException(f"Required tab {required_sport_tab} not found")
        if filtered_tabs[0]['disabled']:
            raise CmsClientException(f"Required tab {required_sport_tab} Is Disabled")
        sport_tab_url = filtered_tabs[0]['targetUri']
        self.__class__.TEST_CONFIG['sport']['url'] = sport_tab_url
        self.__class__.TEST_CONFIG['sport']['name'] = filtered_tabs[0]['imageTitle']
        self.__class__.TEST_CONFIG['sport']['category_id'] = filtered_tabs[0]['categoryId']

    def check_accas_enabled(self):
        all_active_home_tabs = self.cms_config.module_ribbon_tabs.visible_tabs_data
        required_acca_tab = self.TEST_CONFIG.get('hometab').get('name')
        filtered_tabs = list(filter(lambda home_tab: home_tab['title'].upper() == required_acca_tab.upper(),
                                    all_active_home_tabs))
        if not filtered_tabs:
            raise CmsClientException(f"Required tab {required_acca_tab} not found on Module Ribbon Tabs")
        acca_tab_url = filtered_tabs[0]['url']
        self.__class__.TEST_CONFIG['hometab']['url'] = acca_tab_url

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) Login to oxygen CMS.
        PRECONDITIONS: 2) Navigate to sports pages&gt;super buttons.
        PRECONDITIONS: 3) Click on create super button.
        PRECONDITIONS: 4) check active box then select any of the alignment from the dropdown.
        PRECONDITIONS: 5) Enter CTA title with combination of regular and special character (Ex: @_&$)-.
        PRECONDITIONS: 6) Enter description in aligned description field.
        PRECONDITIONS: 7) Enter destination URL.
        PRECONDITIONS: 8) Select any of the tab displayed in the  show on home tabs drop down (Ex: World cup).
        PRECONDITIONS: 9) Select any of the sport displayed on the show on sports drop down (ex: Handball).
        PRECONDITIONS: 10) Select any of the big competitions displayed on the show on big competitions drop down (Ex: World cup).
        PRECONDITIONS: 11) Enter start date and end date.
        PRECONDITIONS: 12) Select any of the themes from themes dropdown.
        PRECONDITIONS: 14) click on create button.
        """
        self.check_accas_enabled()
        self.check_handball_enabled()
        self.disable_all_other_super_buttons()
        super_button_config = {
            'category_id': [self.TEST_CONFIG.get("sport").get("category_id")],
            'competition_id': [],
            'ctaAlignment': self.TEST_CONFIG.get("cta_alignment"),
            'description': self.TEST_CONFIG.get("super_button_description"),
            'home_tabs': [self.TEST_CONFIG.get("hometab").get("url")],
            'target_uri': self.TEST_CONFIG.get('sport').get("url"),
            'name': self.TEST_CONFIG.get("super_button_title"),
            'themes': self.TEST_CONFIG.get("theme"),
        }
        created_super_button = self.cms_config.add_mobile_super_button(**super_button_config)

    def test_001_launch_the_oxygen_application(self):
        """
        DESCRIPTION: Launch the oxygen application.
        EXPECTED: Application should be loaded successfully home tab should be loaded by default.
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_validate_super_button_is_displaying_on_homepage(self):
        """
        DESCRIPTION: Validate super button is displaying on homepage.
        EXPECTED: Super button should be displayed on homepage by default.
        """
        pass
        # Covered in C65934230

    def test_003_validate_the_alignment_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the alignment is displaying as per CMS.
        EXPECTED: Super button alignment should be displayed as per CMS.
        """
        # Covered in step 6

    def test_004_validate_the_title_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the title is displaying as per CMS.
        EXPECTED: The title should be same as per CMS.
        """
        # Covered in step 6

    def test_005_validate_the_description_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the description is displaying as per CMS.
        EXPECTED: Description should be same as per CMS.
        """
        # Covered in step 6

    def test_006_navigate_to_configured_home_tabs_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to configured home tabs and validate the displaying of super button.
        EXPECTED: Super button should be displayed on home tabs.
        """

        # Check Navigation
        self.navigate_to_page(self.TEST_CONFIG.get('hometab').get("url"))
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        expected_tab = self.TEST_CONFIG.get("hometab").get("name").upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: "{current_tab}", '
                                                        f'expected: "{expected_tab}"')

        # Check Super Button Section
        self.assertTrue(self.site.home.has_super_button_section(),
                        msg=f'Super Button section is not found on "{expected_tab}" page')
        has_button = wait_for_result(lambda: self.site.home.super_button_section.super_button.has_button(),
                                     expected_result=True,
                                     timeout=10)

        self.assertTrue(has_button,
                        msg=f'Mobile Super Button was not found on "{expected_tab}" page')

        # Alignment
        super_button_section = self.site.home.super_button_section
        super_button_alignment = super_button_section.cta_alignment
        self.assertEqual(super_button_alignment, self.TEST_CONFIG.get("cta_alignment"))

        # Description
        super_button_description = self.site.home.super_button_section.super_button.description
        self.assertEqual(super_button_description.upper(), self.TEST_CONFIG.get("super_button_description").upper())

        # Button Title
        super_button = self.site.home.super_button_section.super_button.button.name
        self.assertEqual(super_button.upper(), self.TEST_CONFIG.get("super_button_title").upper())

        # Button Theme
        super_button_theme = self.site.home.super_button_section.super_button.theme
        # .replace("_", "").upper()
        self.assertIn(self.TEST_CONFIG.get("theme").upper().replace("_", "").upper(), super_button_theme.upper())

    def test_007_navigate_to_configured_sports_tabs_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to configured sports tabs and validate the displaying of super button.
        EXPECTED: Super button should be displayed on sports tab
        """

        # Check Navigation
        self.navigate_to_page(self.TEST_CONFIG.get('sport').get("url"))
        expected_tab = self.TEST_CONFIG.get("sport").get("name").upper()
        self.assertTrue(self.site.handball.has_super_button_section(),
                        msg=f'Super Button section is not found on "{expected_tab}" page')
        has_button = wait_for_result(lambda: self.site.handball.super_button_section.super_button.has_button(),
                                     expected_result=True,
                                     timeout=10)
        self.assertTrue(has_button,
                        msg=f'Mobile Super Button was not found on "{expected_tab}" page')

        # Alignment
        super_button_section = self.site.handball.super_button_section
        super_button_alignment = super_button_section.cta_alignment
        self.assertEqual(super_button_alignment, self.TEST_CONFIG.get("cta_alignment"))

        # Description
        super_button_description = self.site.handball.super_button_section.super_button.description
        self.assertEqual(super_button_description.upper(), self.TEST_CONFIG.get("super_button_description").upper())

        # Button Title
        super_button = self.site.handball.super_button_section.super_button.button.name
        self.assertEqual(super_button.upper(), self.TEST_CONFIG.get("super_button_title").upper())

        # Button Theme
        super_button_theme = self.site.handball.super_button_section.super_button.theme
        self.assertIn(self.TEST_CONFIG.get("theme").upper().replace("_", "").upper(), super_button_theme.upper())

    def test_008_navigate_to_big_competitions_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to big competitions and validate the displaying of super button.
        EXPECTED: Super button should be displayed on big competition tab
        """
        # Covered in C65934230

    def test_009_validate_the_theme_is_displaying_as_per_cms_configuration(self):
        """
        DESCRIPTION: validate the theme is displaying as per CMS configuration.
        EXPECTED: Theme should be loaded successfully
        """
        # covered in above test

    def test_010_click_on_the_button_and_validate_the_destination_url(self):
        """
        DESCRIPTION: click on the button and validate the destination URL
        EXPECTED: User is navigated to the destination URL
        """
        super_button = self.site.handball.super_button_section.super_button
        super_button.click()
        self.assertIn(self.TEST_CONFIG.get('sport').get('url'),
                      self.device.get_current_url(),
                      msg=f"Not Navigated to {self.TEST_CONFIG.get('sport').get('url')} "
                          f"after clicking on super_button")

    def test_011_login_into_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login into the application with valid credentials.
        EXPECTED: User should be logged into application successfully.
        """
        self.site.login()

    def test_012_repeat_2_11_steps(self):
        """
        DESCRIPTION: repeat 2-11 steps.
        EXPECTED: Result should be as expected.
        """
        self.test_006_navigate_to_configured_home_tabs_and_validate_the_displaying_of_super_button()
        self.test_007_navigate_to_configured_sports_tabs_and_validate_the_displaying_of_super_button()
        self.test_010_click_on_the_button_and_validate_the_destination_url()
