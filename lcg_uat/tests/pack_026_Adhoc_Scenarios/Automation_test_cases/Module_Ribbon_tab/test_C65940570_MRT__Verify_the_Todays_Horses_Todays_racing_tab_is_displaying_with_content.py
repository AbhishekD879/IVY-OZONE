import pytest
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from datetime import datetime
from crlat_ob_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@vtest
class Test_C65940570_MRT__Verify_the_Todays_Horses_Todays_racing_tab_is_displaying_with_content(BaseFeaturedTest):
    """
    TR_ID: C65940570
    NAME: MRT - Verify the Today's Horses/ Today's racing tab is displaying with content
    DESCRIPTION: This test case is to verify the Today's Horses/ Today's Racing tab is displaying with content
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: --Configuration for Event hub in CMS
    PRECONDITIONS: 2)Click on Sport pages > Event hub
    PRECONDITIONS: 3) Click on "+ Create Event Hub"
    PRECONDITIONS: 4) Enter Title  and  Click on Create button
    PRECONDITIONS: 5) Click on Add  Sports Module and select any module from
    PRECONDITIONS: Drop down like Surface Bet Module,
    PRECONDITIONS: Quick Link Module, Featured Events
    PRECONDITIONS: -click on create button
    PRECONDITIONS: 5a)Click on Surface bet module
    PRECONDITIONS: -enabled Active checkbox and click on Save changes button
    PRECONDITIONS: -Click on  +Create Surface Bet and enter all Mandatory fields and Click on Save button
    PRECONDITIONS: -click on quick link module
    PRECONDITIONS: -enabled Active checkbox and click on Save changes button -Click on +Create Sports Quick link and enter all Mandatory fields and click on create button.
    PRECONDITIONS: -Click on Feature Module
    PRECONDITIONS: -enabled Active checkbox and click on Save changes button
    PRECONDITIONS: -click on +Featured Tab Module and enter Mandatory field with race type id and save changes.
    PRECONDITIONS: 5) Configuration for module ribbon tab in the CMS
    PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
    PRECONDITIONS: 6) Click on "+ Create Module ribbon tab" button to create new MRT.
    PRECONDITIONS: 7) Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Coral: -
    PRECONDITIONS: -Module ribbon tab title as Today's racing
    PRECONDITIONS: Ladbrokes: -
    PRECONDITIONS: Module ribbon tab title as Todays horses
    PRECONDITIONS: -Directive name option from dropdown like Event hub
    PRECONDITIONS: -id
    PRECONDITIONS: -URL
    PRECONDITIONS: -Click on "Create" CTA button
    PRECONDITIONS: 8)Check and select below required fields in module ribbon tab configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -IOS
    PRECONDITIONS: -Android
    PRECONDITIONS: -Windows Phone
    PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
    PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
    PRECONDITIONS: -Click on "Save changes" button
    """
    keep_browser_open = True
    now = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                      days=3)[:-3] + 'Z'

    def verify_feature_module_on_event_hub(self):
        featured_module = None
        for i in range(5):
            featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(internal_id=self.internal_id))
            featured_module.scroll_to()
            self.sections = featured_module.accordions_list.items_as_ordered_dict
            self.sections = [section.upper() for section in self.sections]
            if self.created_featured_module_name not in self.sections:
                wait_for_haul(5)
                self.device.refresh_page()
                wait_for_haul(5)
            else:
                break
        self.created_featured_module_name = next(
            (section for section in self.sections if section.upper() == self.created_featured_module_name), None)
        section = featured_module.accordions_list.items_as_ordered_dict.get(self.created_featured_module_name)
        self.assertTrue(section, msg=f'Section "{self.created_featured_module_name}" is not found on FEATURED tab')
        self.assertTrue(section.is_expanded(),
                        msg=f'Section "{self.created_featured_module_name}" feature module is not expanded')
        actual_featured_module_events = [item_name.upper() for item_name in section.items_names]
        self.assertListEqual(self.featured_module_events, actual_featured_module_events,
                             msg=f'actual featured module events {actual_featured_module_events} not equals to expected featured module events {self.featured_module_events}')

    def verify_surface_bet_on_event_hub(self, event_hub_name=None, cms_surface_bet=None, expected_result=True):
        fe_surface_bet = False
        for i in range(2):
            if self.site.home.tab_content.has_surface_bets(expected_result=True, timeout=2):
                surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
                fe_surface_bet = surface_bets.get(cms_surface_bet['title'].upper())
            if expected_result == bool(fe_surface_bet):
                break
            else:
                wait_for_haul(2)
        if expected_result:
            # ************************ Verification of Surface bet Title ****************************
            fe_surface_bet = None
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
            fe_surface_bet = surface_bets.get(cms_surface_bet['title'].upper())
            wait_for_haul(5)
            fe_surface_bet.scroll_to_we()
            self.assertTrue(fe_surface_bet,
                            msg=f"surface bet : {cms_surface_bet['title'].upper()} is not displayed in {event_hub_name} event hub")
            # ************************ Verification of Surface bet Content Header ****************************
            self.assertEqual(cms_surface_bet["contentHeader"].upper(), fe_surface_bet.content_header.upper(),
                             msg=f'expected surface bet content header: "{cms_surface_bet["contentHeader"].upper()}" but actual {fe_surface_bet.content_header.upper()}')
            # ************************ Verification of Surface bet Content ****************************
            for i in range(5):
                if cms_surface_bet['content'].strip().upper() != fe_surface_bet.content.strip().upper():
                    wait_for_haul(5)
                    surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                    surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
                    fe_surface_bet = surface_bets.get(cms_surface_bet['title'].upper())
                else:
                    break
            self.assertEqual(cms_surface_bet['content'].strip().upper(), fe_surface_bet.content.strip().upper(),
                             msg=f"expected surface bet content: {cms_surface_bet['content'].strip().upper()} but actual {fe_surface_bet.content.upper()}")

    def test_000_preconditions(self):
        """
        DESCRIPTION:
        EXPECTED:
        """
        # getitng tabs of module ribbon tab from cms and checking if any of them are event hub

        if self.brand == 'ladbrokes':
            self.__class__.event_hub = self.get_module_data_by_directive_name_from_cms(expected_tab_display_name='TODAYS HORSES',directiveName='EventHub')
        else:
            self.__class__.event_hub = self.get_module_data_by_directive_name_from_cms(expected_tab_display_name='TODAYS RACING',directiveName='EventHub')
        if self.event_hub is None:
            if self.brand == 'ladbrokes':
                self.__class__.event_hub_tab_name = f'TODAYS HORSES'
            else:
                self.__class__.event_hub_tab_name = f'TODAYS RACING'
            response = self.create_eventhub(title = self.event_hub_tab_name)
            self.__class__.event_hub_tab_name = response['title']
            self.__class__.index_number = response.get('hubIndex')
            self.__class__.internal_id = response.get('internalId')
            self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')
            self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='QUICK_LINK')
            self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='SURFACE_BET')
            self.__class__.event_hub_tab_name = response.get('title').upper()
        else:
            # getting index of the TODAY'S RACING event hub
            self.__class__.index_number = self.event_hub.get('hubIndex')
            self.__class__.event_hub_tab_name = self.event_hub.get('title').upper()
            self.__class__.internal_id = self.event_hub.get('internalId')
            # getting all modules for specific event hub
            sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(self.index_number)
            expected_module_type = ['FEATURED','QUICK_LINK','SURFACE_BET']
            if not sports_module_event_hub:
                self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='FEATURED')
                self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='QUICK_LINK')
                self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='SURFACE_BET')
            else:
                existing_modules ={module_tab.get("moduleType").upper():module_tab for module_tab in sports_module_event_hub}
                for expected_module_tab in expected_module_type:
                    if expected_module_tab in existing_modules.keys():
                        if existing_modules.get(expected_module_tab).get('disabled'):
                            self.cms_config.change_sport_module_state(sport_module=existing_modules.get(expected_module_tab))
                    else:
                        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type=expected_module_tab)

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True)
            self.__class__.race_type_id = events[0]['event']['typeId']
            # **************************** Getting Event Ids *************************************
            self.event_id1 = events[0]['event']['id']
            # **************************** Getting Selection Ids *************************************
            outcomes1 = next(((market['market']['children']) for market in events[0]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes1}
            self.selection_id1 = list(event_selection1.values())[0]
        else:
            event1 = self.ob_config.add_football_event_to_england_premier_league()
            # **************************** Getting Selection Ids *************************************
            self.selection_id1 = event1.selection_ids[event1.team1]
            # **************************** Getting Event Ids *************************************
            self.event_id1 = event1.event_id
            # Surface bet Creation::
        self.__class__.cms_surface_bet1 = self.cms_config.add_surface_bet(title='Racing_surface_bet',
                                                                          selection_id=self.selection_id1,
                                                                          on_homepage=False,
                                                                          pageType='sport',
                                                                          eventIDs=self.event_id1,
                                                                          eventHubsIndexes=[self.index_number]
                                                                          )
        # quick link creation:
        destination_url = f'https://{tests.HOSTNAME}/horse-racing'
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                            days=-1,
                                            minutes=-1)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                          minutes=40)[:-3] + 'Z'
        self.__class__.quick_links_data = self.cms_config.create_quick_link(title="Racing_QL",
                                                                            sport_id=self.index_number,
                                                                            page_type='eventhub',
                                                                            destination=destination_url,
                                                                            date_from=date_from, date_to=date_to
                                                                            )
        self.__class__.quick_link_name = self.quick_links_data['title']
        race_url = '/horse-racing/featured'
        featured_module = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId',
                                                                   id=self.race_type_id,
                                                                   page_type='eventhub',
                                                                   page_id=self.index_number,
                                                                   footer_link_url=race_url,
                                                                   show_all_events=True,
                                                                   events_time_from_hours_delta=-10,
                                                                   module_time_from_hours_delta=-10
                                                                   )
        # Checking if the module is Created
        self.assertTrue(featured_module, msg=f'Featured module was not created')
        self.__class__.featured_module_events = []
        for i in (range(len(featured_module['data']))):
            self.featured_module_events.append(featured_module['data'][i]['name'].strip().upper())

        self.__class__.created_featured_module_name = featured_module['title'].strip().upper()

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.navigate_to_page('Homepage')

    def test_002_ladbrokesverify_todays_horses_tab_present_in_mrtcoralverify_todays_racing_tab_present_in_mrt(self):
        """
        DESCRIPTION: Ladbrokes:
        DESCRIPTION: verify Todays Horses tab present in MRT
        DESCRIPTION: Coral:
        DESCRIPTION: verify Todays Racing tab present in MRT
        EXPECTED: Ladbrokes:
        EXPECTED: Today's Horses tab should be present in MRT
        EXPECTED: Coral:
        EXPECTED: verify Todays racing tab present in MRT
        """
        # ************** Getting  all the module ribbon tabs ***********************
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        # ************** Verification of event hub  ***********************
        self.assertIn(self.event_hub_tab_name, home_page_tab_names,
                      f'Created Event Hub tab:{self.event_hub_tab_name} is not found in '
                      f'Current Home Page tabs : {home_page_tab_names}')
        # ************** Navigating to event hub  ***********************
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),
                                       None)
        home_page_tabs.get(self.event_hub_tab_name).click()
        self.assertEqual(self.site.home.tabs_menu.current,
                         self.event_hub_tab_name,
                         f'Tab is not switched to "{self.event_hub_tab_name}" after clicking the "{self.event_hub_tab_name}" tab')

    def test_003_ladbrokesclick_on_todays_horses_tabcoralclick_on_todays_racing_tab(self):
        """
        DESCRIPTION: Ladbrokes:
        DESCRIPTION: click on Todays Horses tab
        DESCRIPTION: Coral:
        DESCRIPTION: click on Todays Racing tab
        EXPECTED: Ladbrokes:
        EXPECTED: 1) User should be able to see Todays Horses tab
        EXPECTED: 2) Should display Surface bets, Quick links,Feature module created with race type Id
        EXPECTED: Coral:
        EXPECTED: 1) User should be able to see Todays Racing tab
        EXPECTED: 2) Should display Surface bets, Quick links,Feature module created with race type Id
        """
        # ************** Verification of surface bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_tab_name,
                                             cms_surface_bet=self.cms_surface_bet1)
        # **************************Verification of Quick links on FE***********************
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        if not quick_links:
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=15)
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            self.assertTrue(quick_links, msg='No "Quick Links" present')
        else:
            self.assertTrue(quick_links, msg='No "Quick Links" present')
        quick_links.get(self.quick_link_name)
        self.verify_quick_link_displayed(name=self.quick_link_name)
        #********************Verification of Feature module on  FE****************
        self.verify_feature_module_on_event_hub()