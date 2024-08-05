import json
from json import JSONDecodeError
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from faker import Faker
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.Common import Common
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.websocket
@pytest.mark.UseFSCCached
@pytest.mark.adhoc_suite
@pytest.mark.adhoc06thFeb24
@pytest.mark.desktop
@vtest
class Test_C66035585_Verify_Featured_Publisher_WebSocket_Multiconnection_reduction(BaseFeaturedTest):
    """
    TR_ID: C66035585
    NAME: Verify Featured Publisher WebSocket Multiconnection reduction
    DESCRIPTION: This tc verifies the Featured Publisher WebSocket Multiconnection reduction
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    first_ws_call_req_id = None
    faker = Faker()
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_default
    is_max_amount_increased = False

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms = cls.get_cms_config()
        cms.update_system_configuration_structure(config_item='UseFSCCached', field_name="enabled", field_value='true')

        if cls.is_max_amount_increased:
            cms.update_system_configuration_structure(
                config_item='Sport Quick Links', field_name='maxAmount', field_value=cls.cms_number_of_quick_links)

    def check_status_highlight_carousel_and_create_new_hc(self):
        hc_module_cms = self.cms_config.get_sport_module(module_type='HIGHLIGHTS_CAROUSEL')[0]
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL', page_id='0')
        elif hc_module_cms['disabled']:
            self.cms_config.change_sport_module_state(sport_module=hc_module_cms)
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        type_id = event['event']['typeId']
        return self.cms_config.create_highlights_carousel(
            title=f'Autotest Highlight Carousel {self.faker.color_name()}',
            typeId=type_id,
            page_type='sport',
            sport_id=0,
            limit=2,
            svgId='football',
            displayOnDesktop=True)

    def check_status_of_module(self, type=None, name=None, time=1, timeout=120):
        if time > timeout:
            return False
        else:
            try:
                wait_for_haul(2)
                tab_content = self.site.home.tab_content if self.device_type == 'mobile' else self.site.home.desktop_modules.featured_module.tab_content
                items_in_module = tab_content.highlight_carousels if type == 'HC' else tab_content.surface_bets.items_as_ordered_dict
                if name.upper().strip() in [title.upper().strip() for title in items_in_module.keys()]:
                    return True
                else:
                    return self.check_status_of_module(type=type, name=name, time=time + 2)
            except:
                return self.check_status_of_module(type=type, name=name, time=time + 2)

    def check_status_surface_bet_and_create_new_sb(self):
        sb_module_cms = self.cms_config.get_sport_module(module_type='SURFACE_BET')[0]
        if sb_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET', page_id='0')
        elif sb_module_cms['disabled']:
            self.cms_config.change_sport_module_state(sport_module=sb_module_cms)

        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        event_id = event['event']['id']
        outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                         market['market'].get('children')), None)
        event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        selection_id = list(event_selection.values())[0]

        return self.cms_config.add_surface_bet(selection_id=selection_id,
                                               title=f'Auto WS {self.faker.color_name()}',
                                               categoryIDs=[0, 16],
                                               eventIDs=[event_id],
                                               highlightsTabOn=True,
                                               svg_icon='football',
                                               displayOnDesktop=True
                                               )

    def check_and_create_quick_link(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        if not self.is_quick_links_enabled():
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                  field_name="enabled",
                                                                  field_value=True)

        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})

        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')

        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')

        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])

        self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                              field_name='maxAmount',
                                                              field_value=self.cms_number_of_quick_links + 1)
        self.__class__.is_max_amount_increased = True

        self.__class__.quick_link_name = 'Autotest QL ' + Faker().city()

        if self.is_quick_link_disabled_for_sport_category(sport_id=0):
            raise CmsClientException('"Quick links" module is disabled for homepage')

        return self.cms_config.create_quick_link(title=self.quick_link_name,
                                                 sport_id=0,
                                                 destination=f'https://{tests.HOSTNAME}/sport/football',
                                                 svgId='football'
                                                 )

    def ql_status(self, ql_name=None, time=1, expected_result=True):
        ql_name = self.quick_link_name if not ql_name else ql_name
        if time > 120:
            return not expected_result
        try:
            ql_stat = next(
                (True for fe_ql_name, ql in self.site.home.tab_content.quick_links.items_as_ordered_dict.items()
                 if fe_ql_name == ql_name or
                 (fe_ql_name[-3:] == '...' and ql_name[:len(fe_ql_name) - 3] + '...' == fe_ql_name)), False)
        except StaleElementReferenceException:
            ql_stat = not expected_result
            time -= 1
        if ql_stat == expected_result:
            return expected_result
        else:
            wait_for_haul(1)
            return self.ql_status(ql_name=ql_name, time=time + 1, expected_result=expected_result)

    def get_featured_modules_and_req_id(self, delimiter='42'):
        """
        wss://featured-sports
        :param delimiter:
        :return:
        """
        attempts = 5
        res = {'modules': None, 'req_id': None}
        while attempts:
            logs = self.device.get_performance_log()
            for entry in logs[::-1]:
                try:
                    if 'FEATURED_STRUCTURE_CHANGED' in str(entry):
                        res['modules'] = json.loads('[' + entry[1]['message']['message']['params']['response'][
                            'payloadData'].split(delimiter + '[')[1])[1].get('modules')
                        res['req_id'] = entry[1]['message']['message']['params']['requestId']
                        break
                except (KeyError, IndexError, AttributeError):
                    continue
            if not res['modules']:
                wait_for_haul(5)
                attempts -= 1
            else:
                break
        return res

    def get_count_and_logs_websocket(self):
        """
        :param url: Required URl
        :return: Complete url
        """
        host = tests.HOSTNAME.replace('-sports', '').replace('2', '')
        url = f'wss://featured-publisher.{host}/socket.io/?EIO=3&transport=websocket&sportId=0'
        count_of_calls, logs = 0, []
        perflog = self.device.get_performance_log(preserve=False)
        for log in list(reversed(perflog)):
            try:
                requested_url = log[1]['message']['message']['params']['url']
                if url in requested_url:
                    count_of_calls += 1
                    logs.append(log)
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        return count_of_calls, logs

    def check_log_updated_in_existing_ws_call(self, req_id=None, prev_page_id=None, new_page_id=None):
        self.assertIsNotNone(req_id, f"Request Id Won't be None/null")
        entries, is_page_end_and_switch_msgs_found, attempts = [], False, 5
        while attempts:
            perf_logs = self.device.get_performance_log()[::-1]
            for entry in perf_logs:
                try:
                    if entry[1].get('message').get('message').get('params').get('requestId') == req_id and (
                            (len(entries) == 0 and f'42["page-switch","{new_page_id}"]' in str(entry)) or (
                            len(entries) == 1 and f'42["page-end","{prev_page_id}"]' in str(entry))):
                        entries.append(entry)
                    if len(entries) == 2:
                        is_page_end_and_switch_msgs_found = True
                        break
                except KeyError:
                    continue
            if is_page_end_and_switch_msgs_found:
                break
            else:
                wait_for_haul(2)
                attempts -= 1
        self.assertTrue(is_page_end_and_switch_msgs_found,
                        msg=f'Unable to get page-end and page-switch messages in same web socket call')

    def get_first_socket_call_req_id(self):
        count_calls, count_of_logs, logs_for_url = 5, 0, []
        while count_calls:
            count_of_logs, logs_for_url = self.get_count_and_logs_websocket()
            if count_of_logs:
                break
            else:
                wait_for_haul(5)
                count_calls -= 1
        self.assertTrue(count_of_logs)
        req_id = logs_for_url[0][1]['message']['message']['params']['requestId']
        return req_id

    def navigate_to_sport_and_validate_ws_call(self, sport_name='football', req_id=None, prev_page_id=0,
                                               new_page_id=16):
        if self.device_type == 'desktop':
            self.site.open_sport(sport_name)
        else:
            footer_menu_items = self.site.navigation_menu.items_as_ordered_dict
            all_sports = next((menu for name, menu in footer_menu_items.items() if name.upper() == self.all_sports_title.upper()), None)
            all_sports.click()
            sport = next((obj for name, obj in self.site.all_sports.a_z_sports_section.items_as_ordered_dict.items() if
                          name.upper() == sport_name.upper()), None)
            sport.click()
            self.site.wait_content_state_changed()
        self.check_log_updated_in_existing_ws_call(req_id=req_id, prev_page_id=prev_page_id, new_page_id=new_page_id)

    def change_order_of_footer_menu(self, title=None, pos=0):
        footer_items = self.cms_config.get_cms_menu_items(menu_types='Footer Menus')['Footer Menus']
        drag_panel_id = next((item['id'] for item in footer_items if item['linkTitle'] == title), None)
        if not drag_panel_id:
            raise CMSException(f'Created item {self.title} not found')
        order = [item['id'] for item in footer_items]
        order.remove(drag_panel_id)
        order.insert(pos, drag_panel_id)
        self.cms_config.change_order_of_footer_items(new_order=order, moving_item=drag_panel_id)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Oxygen application is loaded on Mobile/Tablet or Desktop
        PRECONDITIONS: 2. Modules are created and contain events/selections
        """
        system_config = self.get_initial_data_system_configuration()
        fsc_call = system_config.get('UseFSCCached', {})
        if not fsc_call:
            fsc_call = self.cms_config.get_system_configuration_item('UseFSCCached')
        if fsc_call.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='UseFSCCached',
                                                                  field_name="enabled",
                                                                  field_value=False)
        if self.device_type == 'mobile':
            self.__class__.all_sports_title = next((item.get('linkTitle') for item in self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
                                                     if item.get('targetUri') == 'az-sports'), None)
            if not self.all_sports_title:
                self.__class__.all_sports_title = 'All Sports'
                self.cms_config.create_footer_menu(title=self.all_sports_title, uri='az-sports')
            self.change_order_of_footer_menu(self.all_sports_title)

            self.__class__.home_title = next((item.get('linkTitle') for item in self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
                                                     if item.get('targetUri') == '/'), None)
            if not self.all_sports_title:
                self.__class__.all_sports_title = 'Home'
                self.cms_config.create_footer_menu(title=self.all_sports_title, uri='/')
            self.change_order_of_footer_menu(self.home_title, pos=1)

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application.
        EXPECTED: Application is loaded successfully.
        """
        self.site.launch_application()
        self.__class__.first_ws_call_req_id = self.get_first_socket_call_req_id()

    def test_002_go_to_the_featured_tab_in_module_ribbon_tabs(self):
        """
        DESCRIPTION: Go to the 'Featured' tab in Module Ribbon Tabs.
        EXPECTED: 1. For mobile/tablet:
        EXPECTED: 'Featured' tab is selected by default.
        EXPECTED: For desktop:
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play &amp; Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        EXPECTED: 2. Network tab--&gt;Featured ws connection is established.
        """
        # covering below steps

    def test_003_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page.
        EXPECTED: 1. Page end &amp; Page switch calls are triggered within the same featured connection call.
        EXPECTED: 2. New featured ws connection is not established.
        """
        self.navigate_to_sport_and_validate_ws_call(sport_name='football', req_id=self.first_ws_call_req_id,
                                                    prev_page_id=0,
                                                    new_page_id=self.ob_config.football_config.category_id)

    def test_004_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing page.
        EXPECTED: 1. Page end &amp; Page switch calls are triggered within the same featured connection call.
        EXPECTED: 2. New featured ws connection is not established.
        """
        self.navigate_to_sport_and_validate_ws_call(sport_name='Horse Racing', req_id=self.first_ws_call_req_id,
                                                    prev_page_id=self.ob_config.football_config.category_id,
                                                    new_page_id=self.ob_config.horseracing_config.category_id)

    def test_005_create_a_new_featured_tab_module_in_cms(self):
        """
        DESCRIPTION: Create a new Featured tab module in CMS.
        EXPECTED: 1. Created Featured tab module is displayed in FE.
        EXPECTED: 2. Featured structured changed call is generated in the same featured ws call.
        EXPECTED: 3. New featured ws connection is not established.
        """
        if self.device_type == 'desktop':
            actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(actual_sport_tabs, msg='No one submenu tabs found')
            actual_sport_tabs.get('HOME').click()
            self.site.wait_content_state('Home')
        else:
            home = next((item for name, item in self.site.navigation_menu.items_as_ordered_dict.items() if name.upper() == self.home_title.upper()), None)
            home.click()
        self.site.wait_content_state('Home')

        # highlight carousel verification in fsc
        highlight_carousel_name = self.check_status_highlight_carousel_and_create_new_hc().get('title')
        status = self.check_status_of_module(type='HC', name=highlight_carousel_name)
        self.assertTrue(status,
                        f'"{highlight_carousel_name}" is not found on home page after pooling of 2 mins of time')
        response = self.get_featured_modules_and_req_id()
        is_hc_found_in_fsc = next((True for module in response.get('modules') if
                                   module['@type'] == 'HighlightCarouselModule' and module[
                                       'title'] == highlight_carousel_name), False)
        self.assertTrue(is_hc_found_in_fsc, f'"{highlight_carousel_name}" is not found in FSC')
        is_newly_created_hc_in_same_ws_call = self.first_ws_call_req_id == response.get('req_id')
        self.assertTrue(is_newly_created_hc_in_same_ws_call,
                        f'Highlight Carousel Module in FSC but, FSC is not in same WS call!! \n'
                        f'FSC message call request id : "{response["req_id"]}" is not same as'
                        f'First Web Socket Call Created. WS request id : "{self.first_ws_call_req_id}"')

    def test_006_repeat_step_5_for_hcsbquick_links(self):
        """
        DESCRIPTION: Repeat step 5 for HC,SB,Quick links
        EXPECTED: 
        """
        # Surface Bet verification in fsc
        sb_name = self.check_status_surface_bet_and_create_new_sb().get('title')
        status = self.check_status_of_module(type='SB', name=sb_name)
        self.assertTrue(status, f'"{sb_name}" is not found on home page after pooling of 2 mins of time')
        sb_resp = next((entry for entry in self.device.get_performance_log()[::-1] if
                        'SurfaceBetModule' in str(entry) and sb_name.upper() in str(entry).upper()), None)
        self.assertTrue(sb_resp, f'"{sb_name}" is not found in FSC')
        sb_req_id = sb_resp[1]['message']['message']['params']['requestId']
        is_newly_created_sb_in_same_ws_call = self.first_ws_call_req_id == sb_req_id
        self.assertTrue(is_newly_created_sb_in_same_ws_call,
                        f'Surface Bet Module in FSC but, FSC is not in same WS call!! \n'
                        f'FSC message call request id : "{sb_req_id}" is not same as'
                        f'First Web Socket Call Created. WS request id : "{self.first_ws_call_req_id}"')

        if self.device_type == 'mobile':
            # Quick Link verification in fsc
            ql_name = self.check_and_create_quick_link().get('title')
            status = self.ql_status(ql_name=ql_name)
            self.assertTrue(status, f'"{ql_name}" is not found on home page after pooling of 2 mins of time')
            ql_resp = next(
                (entry for entry in self.device.get_performance_log()[::-1] if 'QuickLinkModule' in str(entry) and
                 'QuickLinkData' in str(entry) and ql_name.upper() in str(entry).upper()), None)
            self.assertTrue(ql_resp, f'"{sb_name}" is not found in FSC')
            ql_req_id = sb_resp[1]['message']['message']['params']['requestId']
            is_newly_created_ql_in_same_ws_call = self.first_ws_call_req_id == ql_req_id
            self.assertTrue(is_newly_created_ql_in_same_ws_call,
                            f'Quick Link Module in FSC but, FSC is not in same WS call!! \n'
                            f'FSC message call request id : "{sb_req_id}" is not same as'
                            f'First Web Socket Call Created. WS request id : "{self.first_ws_call_req_id}"')

    def test_007_leave_the_application_idle_till_the_current_featured_ws_connection_is_closed_and_navigate_to_tennis_page(
            self):
        """
        DESCRIPTION: Leave the application idle till the current featured ws connection is closed and navigate to Tennis page.
        EXPECTED: 1. Featured ws connection is closed.
        EXPECTED: 2. New Featured ws connection is established.
        """
        # can't wait up-to ws disconnects

    def test_008_click_on_a_z_menu(self):
        """
        DESCRIPTION: Click on A-Z menu
        EXPECTED: Page ended should be displayed in network call.
        """

        def check_end_or_switch(msg='42["page-end","0"]'):
            msg_found = False
            for entry in self.device.get_performance_log()[::-1]:
                try:
                    if entry[1].get('message').get('message').get('params').get(
                            'requestId') == self.first_ws_call_req_id and msg in str(entry):
                        msg_found = True
                        break
                except KeyError:
                    continue
            self.assertTrue(msg_found, f'Messages : "{msg}" not found in Web Socket call which is established at first')

        if self.device_type == 'mobile':
            footer_menu_items = self.site.navigation_menu.items_as_ordered_dict
            all_sports = next((menu for name, menu in footer_menu_items.items() if name.upper() == self.all_sports_title.upper()), None)
            all_sports.click()
            check_end_or_switch()
            self.site.back_button.click()
            check_end_or_switch(msg='42["page-switch","0"]')

    def test_009_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back button.
        EXPECTED: It should show the page switch with previous page in network call.
        """
        # covered in above step
