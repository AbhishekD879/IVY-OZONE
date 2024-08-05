from faker import Faker

import tests
import pytest
from datetime import datetime
from tests.base_test import vtest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.quick_links
@pytest.mark.adhoc06thFeb24
@vtest
class Test_C66035587_Verify_display_of_quick_links_for_RGY_users_ozone_10135(BaseFeaturedTest):
    """
    TR_ID: C66035587
    NAME: Verify display of quick links for RGY users ozone 10135
    DESCRIPTION: This testcase verifies the display of quick links for RGY users
    PRECONDITIONS: 1. Login to CMS as admin user.
    PRECONDITIONS: 2. QL is created for Home page , eventhub & SLP in CMS.
    PRECONDITIONS: 3. Above created QL are added to Bonus suppression List
    PRECONDITIONS: Navigate to Bonus Suppression-->Modules. Give a name for the module. Select above QL & SB from the alias module names & save.
    PRECONDITIONS: 5. Navigate to configuration and add above module there.
    PRECONDITIONS: Note :
    PRECONDITIONS: QL creation in CMS :
    PRECONDITIONS: Navigate to Home page-->Quick Links. Click on Create Sports Quick Link Button. Check Active check box, Enter details & Click on Save Button.
    """
    keep_browser_open = True
    quick_link_title = 'Auto_quick_link'
    target_url = 'sport/football'
    sport_id = {'homepage': 0}
    desktop_quick_link_title = None
    faker = Faker()
    quick_link_name = f'Auto {faker.city()}'[:10]
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_object = None
    now = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                      minutes=40)[:-3] + 'Z'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Getting active quick links from "Homepage", "Sport Landing Page" and  "Event Hub".
        """
        if self.device_type == 'mobile':
            # creating quick links on homepage/quick-links in cms
            if not self.is_quick_links_enabled():
                raise CmsClientException('"Quick links" module is disabled')
            if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
                raise CmsClientException('"Quick links" module is disabled for homepage')

            self.cms_config.create_quick_link(title=self.quick_link_name, sport_id=self.sport_id.get('homepage'),
                                              date_from=self.date_from, date_to=self.date_to,
                                              destination=self.destination_url)

            # creating quick links on cms homepage/event-hub
            # creating  event hub in homepage
            event_hub_title = self.create_eventhub()
            self.cms_config.get_event_hubs()
            self.__class__.event_hub_name = event_hub_title.get('title').upper()

            # getting index of the US SPORT event hub
            index_number = event_hub_title['hubIndex']
            # checking module status and creating quick link in event hub
            sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
            quick_link_module_cms = None
            for module in sports_module_event_hub:
                if module['moduleType'] == 'QUICK_LINK':
                    quick_link_module_cms = module
                    break
            if quick_link_module_cms is None:
                self.cms_config.add_sport_module_to_event_hub(module_type='QUICK_LINK', page_id=index_number)
            else:
                quick_link_status = next((module['disabled'] for module in sports_module_event_hub
                                          if module['moduleType'] == 'QUICK_LINK'), None)
                if quick_link_status is True:
                    self.cms_config.change_sport_module_state(sport_module=quick_link_module_cms)
            destination_url = f'https://{tests.HOSTNAME}/home/eventhub/{index_number}'
            # Creating event hub quick link in cms
            self.cms_config.create_quick_link(title=self.quick_link_name, sport_id=index_number,
                                              destination=destination_url, date_from=self.date_from,
                                              date_to=self.date_to, page_type='eventhub')

            # creating quick link in sport landing page in cms
            self.cms_config.create_quick_link(title=self.quick_link_name, sport_id=16, date_from=self.date_from,
                                              date_to=self.date_to, destination=self.destination_url)

            # ********************************************************************************************
            # getting all Super Button alias names from network call from cms
            alias_names = self.cms_config.get_active_feature_modules_alias_names()
            self.__class__.homepage_ql = [next((item for item in alias_names["QL"] if item['title'] == self.quick_link_name), None)]

        # Desktop quick link is different from mobile quick links
        else:
            desktop_quick_link = self.cms_config.create_desktop_quick_links(title=self.quick_link_title, target_url=self.target_url)
            self.desktop_quick_link_title = desktop_quick_link.get('title')
            self.__class__.homepage_ql = self.desktop_quick_link_title

        # ********************************************************************************************
        # verifying whether created quick links is available in bonus suppression module or not in cms
        desktop_alias_module = {"id": "",
                                "title": self.desktop_quick_link_title,
                                "addTag": True}
        module_name = self.quick_link_name if self.device_type == 'mobile' else self.desktop_quick_link_title
        modules = self.cms_config.get_all_rgy_modules()
        existing_modules = []
        self.__class__.required_module = None
        for module in modules:
            existing_modules.append(module.get('moduleName'))
        if self.homepage_ql not in existing_modules:
            self.cms_config.add_rgy_module(module_name=module_name, aliasModules=self.homepage_ql if self.device_type == 'mobile' else [desktop_alias_module])
            modules = self.cms_config.get_all_rgy_modules()
            for module in modules:
                if module.get('moduleName').upper() == module_name.upper():
                    self.required_module = module

        # *********************************************************************************************
        # adding created quick links in bonus suppression module & configuration in cms
        risk_level = self.cms_config.constants.BONUS_SUPPRESSION_RISK_LEVEL.risk_level_one
        reason_code = self.cms_config.constants.BONUS_SUPPRESSION_REASON_CODE.reason_code_one
        bonus_suppression_module = self.cms_config.get_rgy_bonus_suppression_module(risk_level=risk_level,
                                                                                    reason_code=reason_code)

        # if there is no "bonus suppression module" in cms we are adding "bonus suppression module" with "rgy module"
        if bonus_suppression_module == None:
            self.cms_config.add_rgy_bonus_suppression_module(risk_level=risk_level, reason_code=reason_code,
                                                             bonus_suppression_enabled=True,
                                                             rgy_module_ids=[self.required_module.get('id')])
        else:
            # if there is "bonus suppression module" in cms but "super button" rgy module has not there in it,
            # we are adding rgy module to "bonus suppression module"
            existing_modules = []
            modules = bonus_suppression_module.get('modules')
            for module in modules:
                existing_modules.append(module.get('moduleName'))
            if self.required_module.get("moduleName") not in existing_modules:
                alias_module = self.cms_config.get_rgy_module_with_alias(module_name=self.required_module.get("moduleName"))
                self.cms_config.update_rgy_bonus_suppression_module(risk_level=risk_level,
                                                                    reason_code=reason_code,
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

    def test_003_verify_the_display_of_created_ql_in_homepage_event_hub_amp_slp(self):
        """
        DESCRIPTION: Verify the display of created QL in homepage, event hub &amp; SLP
        EXPECTED: QL are displayed properly.
        """
        if self.device_type == 'mobile':
            # ************************* Homepage quick link front end Validation *********************************
            selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                             msg=f'Selected tab is "{selected_tab}" instead of "'
                                 f'{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}" tab')
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=15)
            # checking quick link section is available or not
            quick_link_status = self.site.home.tab_content.has_quick_links()
            if quick_link_status:
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                self.assertIn(self.quick_link_name, quick_links, msg=f'Can not find "{self.quick_link_name}" in homepage feature tab quick links "{quick_links}"')

            # ********************** Event hub quick link front end validation ***********************************
            event_hub_content = self.site.home.get_module_content(self.event_hub_name)
            self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_name}" was not found')
            # checking quick link section is available or not
            event_hub_quick_link_status = self.site.home.tab_content.has_quick_links()
            if event_hub_quick_link_status:
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                self.assertIn(self.quick_link_name, quick_links, msg=f'Can not find "{self.quick_link_name}" in homepage event hub quick links "{quick_links}"')

            # ********************** Sport landing page quick link front end validation ******************************
            self.navigate_to_page('sport/football/matches')
            self.site.wait_content_state(state_name='football')
            slp_quick_link_status = self.site.football.tab_content.has_quick_links()
            if slp_quick_link_status:
                quick_links = self.site.football.tab_content.quick_links.items_as_ordered_dict
                self.assertIn(self.quick_link_name, quick_links, msg=f'Can not find "{self.quick_link_name}" in sport page quick links "{quick_links}"')
        else:
            # for desktop quick links are only displayed in homepage
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=20)
            quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
            if self.homepage_ql not in quick_links:
                self.device.refresh_page()
                self.site.wait_content_state_changed(timeout=10)
            quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
            self.assertIn(self.homepage_ql, quick_links, msg=f'"{self.homepage_ql}" is not present in quick links "{quick_links}" in front end')

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
        if self.site.brand == "ladbrokes":
            self.site.login(username='ganeshgunjal99', password='Sand1234')
        else:
            self.site.login(username='testbonus02', password='Qwerty@123')

    def test_006_verify_the_display_of_created_ql_in_homepage_event_hub_amp_slp(self):
        """
        DESCRIPTION: Verify the display of created QL in homepage, event hub &amp; SLP
        EXPECTED: User is not able to view created QL
        """
        if self.device_type == 'mobile':
            # ************************* Homepage quick link front end Validation *********************************
            selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(selected_tab,
                             self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                             msg=f'Selected tab is "{selected_tab}" instead of "'
                                 f'{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}" tab')
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=15)
            # checking quick link section is available or not
            quick_link_status = self.site.home.tab_content.has_quick_links()
            if quick_link_status:
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                self.assertNotIn(self.quick_link_name, quick_links, msg=f'find "{self.quick_link_name}" in homepage feature tab"{quick_links}"')

            # ********************** Event hub quick link front end validation ***********************************
            event_hub_content = self.site.home.get_module_content(self.event_hub_name)
            self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_name}" was not found')

            # checking quick link section is available or not
            event_hub_quick_link_status = self.site.home.tab_content.has_quick_links()
            if event_hub_quick_link_status:
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                self.assertNotIn(self.quick_link_name, quick_links, msg=f'find "{self.quick_link_name}" in homepage event hub quick links "{quick_links}"')

            # ********************** Sport landing page quick link front end validation ******************************
            self.navigate_to_page('sport/football/matches')
            self.site.wait_content_state(state_name='football')
            slp_quick_link_status = self.site.football.tab_content.has_quick_links()
            if slp_quick_link_status:
                quick_links = self.site.football.tab_content.quick_links.items_as_ordered_dict
                self.assertNotIn(self.quick_link_name, quick_links, msg=f'find "{self.quick_link_name}" in sport page quick links "{quick_links}"')
        else:
            # for desktop quick links are only displayed in homepage
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=20)
            quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
            if self.homepage_ql in quick_links:
                self.device.refresh_page()
                self.site.wait_content_state_changed(timeout=10)
            quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
            self.assertNotIn(self.homepage_ql, quick_links, msg=f'"{self.homepage_ql}" is present in quick links "{quick_links}" in front end')