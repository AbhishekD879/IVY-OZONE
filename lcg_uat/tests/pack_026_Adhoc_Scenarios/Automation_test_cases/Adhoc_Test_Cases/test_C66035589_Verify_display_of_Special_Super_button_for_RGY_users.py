import pytest
from datetime import datetime
from faker import Faker
from tests.Common import Common
from tests.base_test import vtest
from tzlocal import get_localzone
from crlat_cms_client.utils.exceptions import CMSException
from voltron.utils.waiters import wait_for_cms_reflection
from crlat_cms_client.utils.date_time import get_date_time_as_string


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.super_button
@pytest.mark.adhoc06thFeb24
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035589_Verify_display_of_Special_Super_button_for_RGY_users(Common):
    """
    TR_ID: C66035589
    NAME: Verify display of Special Super button for RGY users
    DESCRIPTION: This testcase verifies the display of Special Super button for RGY users
    PRECONDITIONS: 1. Login to CMS as admin user.
    PRECONDITIONS: 2. Special Super Button is created in CMS.
    PRECONDITIONS: 3. Above created special SB is added to Bonus suppression List
    PRECONDITIONS: Navigate to Bonus Suppression-->Modules. Give a name for the module. Select above SB & special super button from the alias module names & save.
    PRECONDITIONS: 5. Navigate to configuration and add above module there.
    PRECONDITIONS: Note :
    PRECONDITIONS: Super Button creation in CMS :
    PRECONDITIONS: Navigate to Home page-->Special Super Button. Click on Create Special Super Button. Enter details & Click on Save Button.
    """
    keep_browser_open = True
    faker = Faker()
    name = f'Auto {faker.city()}'[:10]
    target_uri = '/1-2-free'
    description = 'Auto Test Special Super Button'
    disabled_super_buttons = []
    timezone = str(get_localzone())
    disabled_special_super_buttons = []
    required_module = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)
        for sb_name in cls.disabled_special_super_buttons:
            cms_config.update_mobile_special_super_button(name=sb_name, enabled=True)

    def get_next_races_tab_url(self):
        tab_name = 'NEXT RACES'
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        next_races_tab = next((tab for tab in module_ribbon_tabs if
                                  tab['title'].upper() == tab_name), None)
        if not (bool(next_races_tab) and next_races_tab.get('visible')):
            raise CMSException(f'"{tab_name}" tab is not configured or enabled in CMS')
        home_tabs.append(next_races_tab.get('url'))
        return home_tabs

    def disable_all_other_super_buttons(self, category_id=0):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        all_special_super_buttons = self.cms_config.get_mobile_special_super_buttons()
        for super_button in all_special_super_buttons:
            all_super_buttons.append(super_button)
        for supper_button in all_super_buttons:
            home_tabs = self.get_next_races_tab_url()
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
                if supper_button.get('featureTag'):
                    self.cms_config.update_mobile_special_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_special_super_buttons.append(supper_button.get('title'))
                else:
                    self.cms_config.update_mobile_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_super_buttons.append(supper_button.get('title'))
        self._logger.info(f'{self.disabled_super_buttons}')

    def test_000_preconditions(self):
        """
        Description : Creating 1-2 free game in cms
        Description : Creating new special super button in cms
        """
        self.disable_all_other_super_buttons()
        # getting next races home tab from cms
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        next_races_tab = next((tab for tab in module_ribbon_tabs if tab['title'].upper() == "NEXT RACES"), None)
        self.assertIsNotNone(next_races_tab, msg=f'"{next_races_tab}" tab is not found in cms')
        home_tabs.append(next_races_tab.get('url'))
        # creating new special super button in cms
        self.__class__.special_super_button = self.cms_config.add_mobile_special_super_button(name=self.name,
                                                                                              category_id=[16],
                                                                                              competition_id=[],
                                                                                              target_uri=self.target_uri,
                                                                                              description=self.description,
                                                                                              home_tabs=home_tabs,
                                                                                              enabled=True)
        self.__class__.special_super_button_title = self.special_super_button.get('title').upper()
        self.__class__.tab_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races,
                                                           raise_exceptions=True)
        self.assertTrue(self.tab_name, msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races}" is not available')
        # ***************************************************************************************************
        # getting all special Super Button alias names from network call from cms
        alias_names = self.cms_config.get_active_feature_modules_alias_names()
        alias_Modules = next((item for item in alias_names["SB"] if item['title'].upper() == self.special_super_button_title), None)
        # ********************************************************************************************
        # verifying whether created special super button is available in bonus suppression module or not in cms
        all_rgy_modules = self.cms_config.get_all_rgy_modules()
        all_rgy_module_names = []
        for module in all_rgy_modules:
            module_name = module.get('moduleName')
            all_rgy_module_names.append(module_name)
        if self.special_super_button_title not in all_rgy_module_names:
            self.cms_config.add_rgy_module(module_name=self.special_super_button_title, aliasModules=[] if not alias_Modules else [alias_Modules])
            modules = self.cms_config.get_all_rgy_modules()
            for module in modules:
                if module.get('moduleName').upper() == self.special_super_button_title:
                    self.required_module = module
        # *********************************************************************************************
        # adding created special super button in bonus suppression module & configuration in cms
        risk_level = self.cms_config.constants.BONUS_SUPPRESSION_RISK_LEVEL.risk_level_one
        reason_code = self.cms_config.constants.BONUS_SUPPRESSION_REASON_CODE.reason_code_one
        bonus_suppression_module = self.cms_config.get_rgy_bonus_suppression_module(risk_level=risk_level, reason_code=reason_code)
        if bonus_suppression_module == None:
            self.cms_config.add_rgy_bonus_suppression_module(risk_level=risk_level,reason_code=reason_code,
                                                             bonus_suppression_enabled=True,
                                                             rgy_module_ids=[self.required_module.get('id')])
        else:
            existing_modules = []
            modules = bonus_suppression_module.get('modules')
            for module in modules:
                existing_modules.append(module.get('moduleName'))
            if self.required_module.get("moduleName") not in existing_modules:
                alias_module = self.cms_config.get_rgy_module_with_alias(module_name=self.required_module.get("moduleName"))
                self.cms_config.add_rgy_bonus_suppression_module(risk_level=risk_level, reason_code=reason_code,
                                                                 bonus_suppression_enabled=True,
                                                                 rgy_module_ids=[alias_module['id']])

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Application is loaded.
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_002_login_with_a_valid_user(self):
        """
        DESCRIPTION: Login with a valid user.
        EXPECTED: 1. Login is successful.
        EXPECTED: 2. Home page is loaded.
        """
        self.site.login()
        self.site.wait_content_state("homepage")

    def test_003_verify_the_display_of_created_special_sb_in_1_2_free_page(self):
        """
        DESCRIPTION: Verify the display of created special SB in 1-2 free page.
        EXPECTED: special SB is displayed properly.
        """
        # verifying whether special super button is visible in "Homepage" or not.
        tab_menus = self.site.home.module_selection_ribbon.tab_menu.items_names
        self.assertIn(self.tab_name, tab_menus, msg=f'{self.tab_name} is not present inside {tab_menus}')
        if self.site.home.module_selection_ribbon.tab_menu.current != self.tab_name:
            self.site.home.module_selection_ribbon.tab_menu.click_button(self.tab_name)
        wait_for_cms_reflection(lambda: self.site.home.super_button_section.super_button.button.name == self.special_super_button_title, ref=self, timeout=3, haul=5)
        has_super_button = self.site.home.super_button_section.super_button.has_button()
        self.assertTrue(has_super_button, msg=f'super button section is not available in home page')
        super_button_section = self.site.home.super_button_section.super_button
        super_button_section.scroll_to_we()
        actual_title = super_button_section.button.name
        self.assertEqual(actual_title.upper(), self.special_super_button_title, msg=f'{self.special_super_button_title} is not displaying on home page')

    def test_004_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out successfully.
        """
        self.site.logout()
        self.site.wait_content_state("homepage")

    def test_005_login_into_the_application_with_a_rgy_user(self):
        """
        DESCRIPTION: Login into the application with a RGY user.
        EXPECTED: User is logged in successfully.
        """
        self.site.login(username='ganeshgunjal99', password='Sand1234')

    def test_006_verify_the_display_of_created_special_sb_1_2_free_page(self):
        """
        DESCRIPTION: Verify the display of created special SB 1-2 Free page.
        EXPECTED: User is not able to view created special SB.
        """
        # verifying whether special super button in visible for RGY user in "Home Page" or not.
        tab_menus = self.site.home.module_selection_ribbon.tab_menu.items_names
        self.assertIn(self.tab_name, tab_menus, msg=f'{self.tab_name} is not present inside {tab_menus}')
        if self.site.home.module_selection_ribbon.tab_menu.current != self.tab_name:
            self.site.home.module_selection_ribbon.tab_menu.click_button(self.tab_name)
        super_button = self.site.home.super_button_section.has_super_button()
        self.assertFalse(super_button, msg=f'special supper button {self.special_super_button_title} is available in home page')
