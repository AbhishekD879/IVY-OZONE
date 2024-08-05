import random
from datetime import datetime
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_ob_client.utils.waiters import wait_for_result
from tzlocal import get_localzone
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@vtest
@pytest.mark.timeout(1200)
@pytest.mark.slow
# This TestCase Covers C65866508, C65865538
class Test_C65866508_Verify_surface_bet_created_for_Event_hubs_like_US_Sports_Horse_Racing_hub(Common):
    """
    TR_ID: C65866508
    NAME: Verify surface bet created for Event hubs like 'US Sports', Horse Racing hub
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Click Event Hubs from side navigation and select 'US Sports or Horse Racing hub' option
    PRECONDITIONS: 3.Click 'Surface Bet Module' and click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled', 'Display on Highlights tab', 'Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title
    PRECONDITIONS: EventIds (Create with EventId)
    PRECONDITIONS: Show on Sports select 'All Sports'
    PRECONDITIONS: Show on EventHub
    PRECONDITIONS: Content Header
    PRECONDITIONS: Content
    PRECONDITIONS: Was Price
    PRECONDITIONS: Selection ID
    PRECONDITIONS: Display From
    PRECONDITIONS: Display To
    PRECONDITIONS: SVG Icon
    PRECONDITIONS: SVG Background
    PRECONDITIONS: 6.Check segment as 'Universal'
    PRECONDITIONS: 7.Click Save Changes
    PRECONDITIONS: Check the Sort Order of Surface bet Module
    PRECONDITIONS: Navigate to Event Hubs-->US Sports-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
    """
    keep_browser_open = True
    timezone = str(get_localzone())
    surface_bet_titles = ["Auto Surface Bet 5081 " + f'{random.randint(1, 100000)}',
                          "Auto Surface Bet 5082 " + f'{random.randint(1, 100000)}']
    bet_amount = 0.1

    def verify_surface_bet_on_event_hub(self, event_hub_name=None, cms_surface_bet=None, expected_result=True):
        # ************** Getting  all the module ribbon tabs ***********************
        wait_for_haul(5)
        self.device.refresh_page()
        wait_for_result(
            lambda: event_hub_name in list(self.site.home.tabs_menu.items_as_ordered_dict.keys()),
            timeout=30,
            expected_result=expected_result
        )
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        # ************** Verification of event hub  ***********************
        self.assertIn(event_hub_name, home_page_tab_names,
                      f'Created Event Hub tab:{event_hub_name} is not found in '
                      f'Current Home Page tabs : {home_page_tab_names}')
        # ************** Navigating to event hub  ***********************
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == event_hub_name),
                                       None)
        home_page_tabs.get(event_hub_name).click()
        wait_for_haul(2)
        self.assertEqual(self.site.home.tabs_menu.current,
                         event_hub_name,
                         f'Tab is not switched to "{event_hub_name}" after clicking the "{event_hub_name}" tab')
        self.device.refresh_page()
        wait_for_haul(5)
        fe_surface_bet = False
        for i in range(10):
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
            # ************************ Verification of Surface bet SVG Id ****************************
            self.assertEqual(f'#' + cms_surface_bet['svgId'], fe_surface_bet.header.icontext,
                             msg=f"expected surface bet SVG Id : {f'#' + cms_surface_bet['svgId']} but actual {fe_surface_bet.header.icontext}")
        else:
            if self.site.home.tab_content.has_surface_bets(expected_result=True, timeout=0.1):
                surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
                fe_surface_bet = surface_bets.get(cms_surface_bet['title'].upper())
                self.assertFalse(fe_surface_bet,
                                 msg=f"surface bet : {cms_surface_bet['title'].upper()} is displayed under {event_hub_name} event hub")

    def change_surface_bets_order_under_event_hub(self, index=0, surface_bet_titles=[]):
        # ************* Changing order of SB under eventhub *************************************
        all_sbs = self.cms_config.get_surface_bets_for_page(related_to='eventhub', reference_id=index)
        sb_ids = []
        for i in range(len(surface_bet_titles)):
            for sb in all_sbs:
                if sb.get('title').upper() == surface_bet_titles[i].upper():
                    sb_ids.append(sb.get('id'))
                    break
        all_sb_ids = [item['id'] for item in all_sbs]
        i = 0
        for sb_id in sb_ids[::-1]:
            all_sb_ids.remove(sb_id)
            all_sb_ids.insert(i, sb_id)
            self.cms_config.set_surfacebet_ordering(new_order=all_sb_ids, moving_item=sb_id, pageType='eventhub',
                                                    pageId=index)
            i += 1

    def verify_surface_bets_order_on_fe_under_event_hub(self, surface_bet_titles=[], event_hub_name=None):
        # ************* Verification of SB order under eventhub *************************************
        # ************** Getting  all the module ribbon tabs ***********************
        wait_for_haul(5)
        self.device.refresh_page()
        wait_for_result(
            lambda: event_hub_name in list(self.site.home.tabs_menu.items_as_ordered_dict.keys()),
            timeout=30,
            expected_result=True
        )
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        # ************** Verification of event hub  ***********************
        self.assertIn(event_hub_name, home_page_tab_names,
                      f'Created Event Hub tab:{event_hub_name} is not found in '
                      f'Current Home Page tabs : {home_page_tab_names}')
        # ************** Navigating to event hub  ***********************
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == event_hub_name),
                                       None)
        home_page_tabs.get(event_hub_name).click()
        wait_for_haul(2)
        self.assertEqual(self.site.home.tabs_menu.current,
                         event_hub_name,
                         f'Tab is not switched to "{event_hub_name}" after clicking the "{event_hub_name}" tab')
        self.device.refresh_page()
        wait_for_haul(5)
        # ************** Verification of surface bet order **********************
        expected_surface_bets_order = [sb.upper() for sb in surface_bet_titles]
        expected_surface_bets_order.reverse()
        for i in range(60):
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            self.assertTrue(surface_bets, msg=f'No Surface Bets found in {event_hub_name} event hub')
            actual_surface_bets_order = [surface_bet.upper() for surface_bet in list(surface_bets.keys())[:2]]
            if expected_surface_bets_order == actual_surface_bets_order:
                break
            else:
                wait_for_haul(2)
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        actual_surface_bets_order = [surface_bet.upper() for surface_bet in list(surface_bets.keys())[:2]]
        self.assertListEqual(expected_surface_bets_order, actual_surface_bets_order,
                             msg=f'Expected Surface Bets order {expected_surface_bets_order} but actual {actual_surface_bets_order}')

    def verify_bet_placement_on_surface_bet(self, event_hub_name=None, cms_surface_bet=None):
        # ********************************* Verify Bet Placement **************************
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        # ************** Verification of event hub  ***********************
        self.assertIn(event_hub_name, home_page_tab_names,
                      f'Created Event Hub tab:{event_hub_name} is not found in '
                      f'Current Home Page tabs : {home_page_tab_names}')
        # ************** Navigating to event hub  ***********************
        self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == event_hub_name),
                                       None)
        home_page_tabs.get(event_hub_name).click()
        self.assertEqual(self.site.home.tabs_menu.current,
                         event_hub_name,
                         f'Tab is not switched to "{event_hub_name}" after clicking the "{event_hub_name}" tab')
        # ************** Getting  all the surface bets from event hub ***********************
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg=f'No Surface Bets found under {event_hub_name} event hub')
        # ************************ Verification of Surface bet Title ****************************
        surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
        fe_surface_bet = surface_bets.get(cms_surface_bet['title'].upper())
        fe_surface_bet.scroll_to_we()
        bet_button = fe_surface_bet.bet_button
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), f"unable to select {cms_surface_bet['title'].upper()} bet button")
        wait_for_haul(5)
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet.place_bet.click()
        bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        quick_bet.header.close_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        cms_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        cms_module_ribbon_tab_names = [tab['title'].upper() for tab in cms_module_ribbon_tabs if
                                       tab['visible'] is True and
                                       tab['directiveName'] == 'EventHub' and
                                       (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                           time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.event_hub_names = []
        name1 = next((tab.upper() for tab in cms_module_ribbon_tab_names if tab.upper() == "TODAY'S RACING"), None)
        if name1:
            self.event_hub_names.append(name1)
        name2 = next((tab.upper() for tab in cms_module_ribbon_tab_names if tab.upper() == 'US SPORTS'), None)
        if name2:
            self.event_hub_names.append(name2)

        self.__class__.event_hub_index_numbers = []
        event_1_index = next(
            (tab['hubIndex'] for tab in cms_module_ribbon_tabs if tab['title'].upper() == "TODAY'S RACING"), None)
        if event_1_index:
            self.event_hub_index_numbers.append(event_1_index)
        event_2_index = next((tab['hubIndex'] for tab in cms_module_ribbon_tabs if tab['title'].upper() == 'US SPORTS'),
                             None)
        if event_2_index:
            self.event_hub_index_numbers.append(event_2_index)

        # ******************** Creation of Event Hubs if Event Hubs are not available ***************************
        if len(self.event_hub_names) < 2:
            for i in range(2 - len(self.event_hub_names)):
                existing_event_hubs = self.cms_config.get_event_hubs()
                existing_event_hubs_index_numbers = [index['indexNumber'] for index in existing_event_hubs]
                self.__class__.index_number = next(
                    index for index in range(1, 20) if index not in existing_event_hubs_index_numbers)
                self.__class__.event_hub_index_numbers.append(self.index_number)
                self.__class__.created_event_hub_id = self.cms_config.create_event_hub(
                    index_number=self.index_number).get('id')
                self.__class__.event_hub_name = f'Auto EventHub_{self.index_number}'
                #   Adding event hub to module ribbon tab
                internal_id = f'tab-eventhub-{self.index_number}'
                event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                                   internal_id=internal_id,
                                                                                   hub_index=self.index_number,
                                                                                   display_date=True)
                self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
                self.event_hub_names.append(self.event_hub_tab_name)
        # *************************** Adding Sport Module to Eventhub ******************************
        for i in range(2):
            sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(self.event_hub_index_numbers[i])
            sb_module_cms = None
            for module in sports_module_event_hub:
                if module['moduleType'] == 'SURFACE_BET':
                    sb_module_cms = module
                    break
            if sb_module_cms is None:
                self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET', page_id=self.event_hub_index_numbers[i])
            else:
                surface_bet_module_status = next((module['disabled'] for module in sports_module_event_hub
                                                  if module['moduleType'] == 'SURFACE_BET'), None)
                if surface_bet_module_status is True:
                    self.cms_config.change_sport_module_state(sport_module=sb_module_cms, active=True)
        # **************************** Getting Events *************************************
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            # **************************** Getting Event Ids *************************************
            self.event_id1 = events[0]['event']['id']
            self.event_id2 = events[1]['event']['id']
            self.event_id3 = events[2]['event']['id']
            # **************************** Getting Selection Ids *************************************
            outcomes1 = next(((market['market']['children']) for market in events[0]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes1}
            self.selection_id1 = list(event_selection1.values())[0]
            outcomes2 = next(((market['market']['children']) for market in events[1]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes2}
            self.selection_id2 = list(event_selection2.values())[0]
            outcomes3 = next(((market['market']['children']) for market in events[2]['event']['children'] if
                              market['market'].get('children')), None)
            event_selection3 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes3}
            self.selection_id3 = list(event_selection3.values())[0]
        else:
            event1 = self.ob_config.add_football_event_to_england_premier_league()
            event2 = self.ob_config.add_football_event_to_england_premier_league()
            event3 = self.ob_config.add_football_event_to_england_premier_league()
            # **************************** Getting Selection Ids *************************************
            self.selection_id1 = event1.selection_ids[event1.team1]
            self.selection_id2 = event2.selection_ids[event1.team1]
            self.selection_id3 = event3.selection_ids[event1.team1]
            # **************************** Getting Event Ids *************************************
            self.event_id1 = event1.event_id
            self.event_id2 = event2.event_id
            self.event_id3 = event3.event_id
        self.__class__.cms_surface_bet1 = self.cms_config.add_surface_bet(title=self.surface_bet_titles[0],
                                                                          selection_id=self.selection_id1,
                                                                          on_homepage=True,
                                                                          eventIDs=[self.event_id1],
                                                                          eventHubsIndexes=[
                                                                              self.event_hub_index_numbers[0],
                                                                              self.event_hub_index_numbers[1]],
                                                                          svg_icon='Football',
                                                                          categoryIDs=[])
        self.__class__.cms_surface_bet2 = self.cms_config.add_surface_bet(title=self.surface_bet_titles[1],
                                                                          selection_id=self.selection_id2,
                                                                          on_homepage=True,
                                                                          eventIDs=[self.event_id2],
                                                                          eventHubsIndexes=[
                                                                              self.event_hub_index_numbers[0]],
                                                                          svg_icon='Football',
                                                                          categoryIDs=[])
        self.__class__.cms_surface_bet3 = self.cms_config.add_surface_bet(
            title="exclude sb 508" + f'{random.randint(1, 100000)}',
            selection_id=self.selection_id3,
            on_homepage=True,
            eventIDs=[self.event_id3],
            eventHubsIndexes=[
                self.event_hub_index_numbers[0],
                self.event_hub_index_numbers[1]],
            svg_icon='Football',
            categoryIDs=[])

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.site.login()

    def test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub(self):
        """
        DESCRIPTION: Validate the surface bet is displayed under events hubs 'US Sports' or 'Horse Racing hub'
        EXPECTED: Surface bet created should reflect on events hubs 'US Sports' or 'Horse Racing hub' as per CMS config
        """
        # ************** Verification of surface bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2)

    def test_003_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        # ************** Changing the order of Surface Bet **********************
        self.change_surface_bets_order_under_event_hub(index=self.event_hub_index_numbers[0],
                                                       surface_bet_titles=self.surface_bet_titles)
        # ************** Verification of Surface Bet order **********************
        self.verify_surface_bets_order_on_fe_under_event_hub(surface_bet_titles=self.surface_bet_titles,
                                                             event_hub_name=self.event_hub_names[0])

    def test_004_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        # Covered in test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub

    def test_005_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        # Covered in test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub

    def test_006_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        # Covered in test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub

    def test_007_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        # Covered in test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub

    def test_008_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # Covered in test_002_validate_the_surface_bet_is_displayed_under_events_hubs_us_sports_or_horse_racing_hub

    def test_009_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        # ************** Changing Surface Bet Display From and Display To to Past Time **********************
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-22)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=-20)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], displayFrom=start_time,
                                           displayTo=end_time)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], displayFrom=start_time,
                                           displayTo=end_time)
        # ************** Verify Surface Bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2, expected_result=False)

    def test_010_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # ************** Changing Surface Bet Display To to few min from Current time **********************
        self._logger.info(f'*** Current timezone is" "{self.timezone}"')
        end_time = None
        if self.timezone.upper() == "UTC":
            end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                               url_encode=False, minutes=2)[:-3] + 'Z'
        else:
            end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                               url_encode=False, hours=-5.5, minutes=2)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], displayTo=end_time)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2, expected_result=False)
        # ************** Changing Surface Bet Display From to Past and Display To to Future **********************
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-22)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=20)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], displayFrom=start_time,
                                           displayTo=end_time)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], displayFrom=start_time,
                                           displayTo=end_time)
        # ************** Verify Surface Bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2)

    def test_011_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=12)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=20)[:-3] + 'Z'
        # ************** Changing Surface Bet Display From and Display To to Future Time **********************
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], displayFrom=start_time,
                                           displayTo=end_time)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], displayFrom=start_time,
                                           displayTo=end_time)
        # ************** Verify Surface Bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2, expected_result=False)
        # ************** Changing Surface Bet Display From to Past and Display To to Future **********************
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-22)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=20)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], displayFrom=start_time,
                                           displayTo=end_time)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], displayFrom=start_time,
                                           displayTo=end_time)
        # ************** Verify Surface Bet on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2)

    def test_012_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_homepage(self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in homepage
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        # Left and Right arrows not available for mobile

    def test_013_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # Left and Right arrows not available for mobile

    def test_014_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        # ************** Verify Surface Bet bet placement **********************
        self.verify_bet_placement_on_surface_bet(event_hub_name=self.event_hub_names[0],
                                                 cms_surface_bet=self.cms_surface_bet1)

    def test_015_activatedeactivate_created_surface_bet_on_event_hub(self):
        """
        DESCRIPTION: Activate/Deactivate created surface bet on event hub
        EXPECTED: Surface bet should display on event hub if it is activated
        EXPECTED: Surface bet should not display on event hub if it is deactivated
        """
        # ************** Deactivate Surface Bet **********************
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], disabled=True)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], disabled=True)
        # ************** Verification of Surface Bets on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1, expected_result=False)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2, expected_result=False)
        # ************** Activate Surface Bet **********************
        self.cms_config.update_surface_bet(self.cms_surface_bet1['id'], disabled=False)
        self.cms_config.update_surface_bet(self.cms_surface_bet2['id'], disabled=False)
        # ************** Verification of Surface Bets on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2)

    def test_016_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # ************** Delete Surface Bet **********************
        self.cms_config.delete_surface_bet(surface_bet_id=self.cms_surface_bet2['id'])
        self.cms_config._created_surface_bets.remove(self.cms_surface_bet2['id'])
        # ************** Verification of Surface Bets on FE **********************
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet2, expected_result=False)

    def test_017_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        self.cms_surface_bet1 = self.cms_config.update_surface_bet(self.cms_surface_bet1['id'],
                                                                   content="Automation testing content")
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[0],
                                             cms_surface_bet=self.cms_surface_bet1)
        self.verify_surface_bet_on_event_hub(event_hub_name=self.event_hub_names[1],
                                             cms_surface_bet=self.cms_surface_bet1)
