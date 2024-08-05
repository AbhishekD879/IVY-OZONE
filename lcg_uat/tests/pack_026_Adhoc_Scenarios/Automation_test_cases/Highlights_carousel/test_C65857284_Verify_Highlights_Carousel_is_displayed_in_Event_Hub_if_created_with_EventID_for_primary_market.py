import pytest
from faker import Faker
import tests
from tests.base_test import vtest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name, BaseHighlightsCarouselTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@pytest.mark.last
@vtest
class Test_C65857284_Verify_Highlights_Carousel_is_displayed_in_Event_Hub_if_created_with_EventID_for_primary_market(
    BaseHighlightsCarouselTest):
    """
    TR_ID: C65857284
    NAME: Verify Highlights Carousel is displayed in Event Hub if created with EventID for primary market
    DESCRIPTION: This test case verifies display of Highlights Carousel in event hub with EventID for primary market
    PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
    PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
    PRECONDITIONS: 1. Login to Environment specific CMS
    PRECONDITIONS: 2. Navigate to Sports Pages -->Event Hub
    PRECONDITIONS: 3. Click on Create Event Hub
    PRECONDITIONS: 4. Enter title and click on Create button
    PRECONDITIONS: 5. Click on Add Sport Module --> Select option from dropdown as Highlights Carousel
    PRECONDITIONS: 6. Click on Create button
    PRECONDITIONS: 7. Click on Highlights Carousel module in newly created Event Hub --> Click on Create Highlight Carousel button
    PRECONDITIONS: 8. Enter All fields like
    PRECONDITIONS: - Active Checkbox
    PRECONDITIONS: - Title as 'Featured - Ladies Matches '
    PRECONDITIONS: - TypeId/EventId (Create with EventId)
    PRECONDITIONS: - Select market and Market Type will be auto selected (Select Market as 2Up Market)
    PRECONDITIONS: - Display From
    PRECONDITIONS: - Display To
    PRECONDITIONS: - SVG Icon
    PRECONDITIONS: - No.Of Events
    PRECONDITIONS: - Display Inplay
    PRECONDITIONS: 9. Click on Create button
    PRECONDITIONS: 10. Select Active checkbox for Highlight Carosel in Event hub and save the changes
    PRECONDITIONS: Module Ribbon Tab Creation(MRT) in CMS :
    PRECONDITIONS: 1. Navigate to Module Ribbon tab
    PRECONDITIONS: 2. Click on Create Module Ribbon tab and enter below fields
    PRECONDITIONS: - Module Ribbon tab Title
    PRECONDITIONS: - Directive name as Event Hub
    PRECONDITIONS: - Select Event Hub name(Which we created above)
    PRECONDITIONS: - Visible from,Visible To(User can change accordingly)
    PRECONDITIONS: 3. Click on Create button
    PRECONDITIONS: 4. Select Active checkbox,IOS,Android checkboxes
    PRECONDITIONS: 5. Select Show Tab on field and click on Save Changes button
    PRECONDITIONS: Check the Sort Order of Highlight Carousel Module in Event Hub:
    PRECONDITIONS: 1. Navigate to Sports Pages--> Event Hub--> Select newly Created Evnet Hub--> Check the Highlights Carousel order
    """
    keep_browser_open = True
    highlights_carousels_titles = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]
    quick_link_name = 'Autotest ' + Faker().city()
    expected_highlights_carousel_events = []
    svg_icon = "football"
    events_start_time = {}

    def changing_the_order_of_modules_in_cms(self, modules, index_number):
        modules = modules
        # getting the modules
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        # getting the ids of the module which we need to change the order
        drag_panel_ids = []
        for module in modules:
            for item in sports_module_event_hub:
                if item.get('moduleType').upper() == module.upper():
                    drag_panel_ids.append(item.get('id'))
                    break
        order = [item['id'] for item in sports_module_event_hub]
        i = 0
        for drag_panel_id in drag_panel_ids:
            order.remove(drag_panel_id)
            order.insert(i, drag_panel_id)
            self.cms_config.change_order_of_module_items(new_order=order, moving_item=drag_panel_id)
            i += 1

    def check_module_status_and_create_hightlight_carousel(self, index_number: int = None, active=True,
                                                           create_high_light=True):
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        hc_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL', page_id=index_number)
        else:
            highlights_module_status = next((module['disabled'] for module in sports_module_event_hub
                                             if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL'), None)
            if highlights_module_status is True and active is True:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms, active=active)
            else:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms, active=active)
        if active is True and create_high_light:
            #   Adding sports module to event hub
            hightlight_carousel = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_titles[0],
                                                                             events=[self.event_id_1],
                                                                             page_type='eventhub',
                                                                             sport_id=index_number, limit=1,
                                                                             svgId=self.svg_icon
                                                                             )
            return hightlight_carousel

    def check_module_status_and_create_surface_bet(self, index_number: int = None, selection_id: int = None,
                                                   eventID=[]):
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        surface_bet_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_module_cms = module
                break
        if surface_bet_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET', page_id=index_number)
        else:
            surface_module_status = next((module['disabled'] for module in sports_module_event_hub
                                        if module['moduleType'] == 'SURFACE_BET'), None)
            if surface_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=surface_bet_module_cms)

        #   Adding sports module to event hub
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      eventIDs=eventID,
                                                      event_hub_id=index_number,
                                                      edp_on=True,
                                                      highlightsTabOn=True,
                                                      svg_icon='football',
                                                      )
        return surface_bet

    def check_module_status_and_create_quick_link(self, index_number: int = None):
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
        #   Adding sports module to event hub
        quick_link = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                       sport_id=index_number,
                                                       destination=destination_url,
                                                       page_type='eventhub'
                                                       )
        return quick_link

    def checking_ordering_of_modules(self, index_number):
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        # we are getting the section in the tab with tab name as key and order as value
        # getting frontend order
        if self.brand != 'bma':
            sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='ladbrokes')
        else:
            sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='bma')
        for section in sports_module_event_hub[:3]:
            module_type = section.get('moduleType').upper()
            for count in range(3):
                if sections_names_with_order.get(module_type) != sports_module_event_hub.index(section):
                    # taking time to reflect the order changes
                    wait_for_haul(5)
                    self.device.refresh_page()
                    self.device.driver.implicitly_wait(3)
                    if self.brand != 'bma':
                        sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='ladbrokes')
                    else:
                        sections_names_with_order = self.site.home.tab_content.get_all_sections_order(brand='bma')
                else:
                    break
            self.assertEqual(sections_names_with_order.get(module_type), sports_module_event_hub.index(section),
                             msg=f'the module of cms {module_type} order {sports_module_event_hub.index(section)} is '
                                 f'not same as frontend {sections_names_with_order.get(module_type)} ')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            self.__class__.event_id_1 = events[-1]['event']['id']
            self.__class__.event_id_2 = events[-2]['event']['id']
            outcomes = next(((market['market']['children']) for market in events[-1]['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(event_selection.values())[0]
            self.expected_highlights_carousel_events.append(events[-1]['event']['name'].upper())
            # ******** Getting event start time  ********
            self.events_start_time[events[-1]['event']['name'].upper()] = events[-1]['event']['startTime']
        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id_1 = event1.event_id
            self.__class__.selection_id = event1.selection_ids[event1.team1]
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id_2 = event2.event_id
            self.expected_highlights_carousel_events.append(event1.ss_response['event']['name'].upper())
            # ******** Getting event start time  ********
            self.events_start_time[event1.ss_response['event']['name'].upper()] = event1.ss_response['event'][
                'startTime']
        # getting tabs of module ribbon tab from cms and checking if any of them are event hub
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                    tab['visible'] is True and
                    tab['directiveName'] == 'EventHub' and
                    (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                        time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.event_hub_tab_name = next((tab.upper() for tab in tabs_cms if tab.upper() == 'US SPORTS'),
                                                 None)
        # getting index of the US SPORT event hub
        self.__class__.index_number = None
        if self.event_hub_tab_name:
            self.__class__.index_number = next((tab['hubIndex'] for tab in module_ribbon_tabs if
                                                tab['title'].upper() == self.event_hub_tab_name.upper()), None)
        if self.event_hub_tab_name is None or self.index_number is None:
            # Creating the eventhub
            existing_event_hubs = self.cms_config.get_event_hubs()
            existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
            # need a unique non-existing index for new Event hub
            self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
            # Create the event hub name
            self.cms_config.create_event_hub(index_number=self.index_number)
            # Adding event hub to module ribbon tab
            internal_id = f'tab-eventhub-{self.index_number}'
            event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=self.index_number,
                                                                               display_date=True)
            self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

        # create or update the highlight carousel in event hub
        created_hight_carousel = self.check_module_status_and_create_hightlight_carousel(index_number=self.index_number)
        self.__class__.highlight_carousel_id1 = created_hight_carousel.get('id')

        # converting the highlight carousel name as required for both brands
        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[0])
        self.__class__.highlights_carousel_name_2 = self.convert_highlights_carousel_title(
            self.highlights_carousels_titles[1])

    def test_001_1_login_to_ladscoral_ltenvironmentgt(self):
        """
        DESCRIPTION: 1. Login to Lads/Coral &lt;Environment&gt;
        EXPECTED: User should be logged in
        """
        self.site.login()

    def test_002_2_navigate_to_module_ribbon_tab_which_is_created_in_cms(self):
        """
        DESCRIPTION: 2. Navigate to Module Ribbon tab which is created in CMS
        EXPECTED: 2. Highlight Carousel should be displayed in Module Ribbon tab
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.device.refresh_page()
            wait_for_haul(5)
            # getting tabs in home page tabs for mobile
            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            if self.event_hub_tab_name.upper() not in home_page_tab_names:
                wait_for_haul(20)
                self.device.refresh_page()
                home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
                home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            self.assertIn(self.event_hub_tab_name, home_page_tab_names,
                          f'Created Event Hub tab:{self.event_hub_tab_name} is not found in '
                          f'Current Home Page tabs : {home_page_tab_names}')
            self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),
                                           None)
            # navigating to the event hub tab which is created
            home_page_tabs.get(self.event_hub_tab_name).click()
            self.assertEqual(self.site.home.tabs_menu.current,
                             self.event_hub_tab_name,
                             f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')
        # checking whether there are highlight carousels in event hub tab
        status_highlight_carousele = self.site.home.tab_content.has_highlight_carousels(expected_result=True)
        self.assertTrue(status_highlight_carousele,
                        msg=f'created highlight carousels {self.highlights_carousel_name_1} is not present in the event hub tab{self.event_hub_tab_name}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        # getting the highlight carousel which we created among all the highlight carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1}')
        actual__highlights_carousel_events = [item_name.upper() for item_name in highlight_carousel.items_names]
        self.assertListEqual(self.expected_highlights_carousel_events, actual__highlights_carousel_events,
                             msg=f'actual highlights carousel events {actual__highlights_carousel_events} not equals to expected highlights carousel events {self.expected_highlights_carousel_events}')
        self.assertEqual(highlight_carousel.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')
        surface_bets_status = self.site.home.tab_content.has_surface_bets(expected_result=True)
        if not surface_bets_status:
            # create or update the status of surface bet module event hub and create a surface bet in that module
            surface_bet = self.check_module_status_and_create_surface_bet(index_number=self.index_number,
                                                                          eventID=[self.event_id_1],
                                                                          selection_id=self.selection_id)

            self.__class__.created_surface_bet = surface_bet.get('title').upper()
            self.device.refresh_page()
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(self.created_surface_bet)
            self.assertTrue(surface_bet, msg=f'Failed to display Surface Bets named {self.created_surface_bet} is not '
                                             f'present in the event hub tab{self.event_hub_tab_name}')
        quick_links_status = self.site.home.tab_content.has_quick_links(expected_result=True)
        if not quick_links_status:
            # create or update the status of quick link module event hub and create a quick link
            quick_link = self.check_module_status_and_create_quick_link(index_number=self.index_number)
            self.__class__.created_quick_link = quick_link.get('title')
            self.device.refresh_page()
            quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
            quick_link = quick_links.get(self.created_quick_link)
            self.assertTrue(quick_link, msg=f'Failed to display quick link named {self.created_quick_link} is not '
                                            f'present in the event hub tab{self.event_hub_tab_name}')

    def test_003_3_validate_the_order_of_highlights_carousel_module_in_event_hub(self):
        """
        DESCRIPTION: 3. Validate the Order of Highlights Carousel Module in Event Hub
        EXPECTED: 3. Order of Highlights Carousel Module in Event Hub should be as per CMS config
        """
        # setting the order of the module in the event hub
        self.modules = ['HIGHLIGHTS_CAROUSEL', 'SURFACE_BET', 'QUICK_LINK']
        self.changing_the_order_of_modules_in_cms(modules=self.modules, index_number=self.index_number)
        self.checking_ordering_of_modules(index_number=self.index_number)

    def test_004_4_change_the_highlights_carousel_order_in_event_hub(self):
        """
        DESCRIPTION: 4. Change the Highlights Carousel order in Event Hub
        EXPECTED: 4. Order of Highlights Carousel Module in Event Hub should be as per CMS config
        """
        # setting the order of the module in the event hub
        self.modules = ['SURFACE_BET', 'QUICK_LINK', 'HIGHLIGHTS_CAROUSEL']
        self.changing_the_order_of_modules_in_cms(modules=self.modules, index_number=self.index_number)
        self.checking_ordering_of_modules(index_number=self.index_number)

    def test_005_5_validate_the_highlights_carousel_title_and_svg_icon(self):
        """
        DESCRIPTION: 5. Validate the Highlights Carousel Title and SVG Icon
        EXPECTED: 5. Title Name and SVG icon should be displayed as per CMS config
        """
        # coverd in above step

    def test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time(
            self):
        """
        DESCRIPTION: 6. Validate the Team names and selections display of Highlights Carousel along with event Date &amp; Start Time
        EXPECTED: 6. Team names and selections display as per Typeid/Eventid config in CMS
        EXPECTED: - Event Date &amp; Start Time should be displayed above the team names
        """
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        # getting the highlight carousel which we created among all the highlight carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        highlight_carousel.scroll_to()
        # getting evnets present in the highlight carousel which we created
        self.__class__.highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name_1}"')
        # converting the events name to upper
        self.assertEqual(len(self.highlight_carousel_events), 1,
                         msg=f'events in highlight carousel named "{self.highlights_carousel_name_1} is not same as limit"')
        # getting one event among events
        event_name, event = next(iter(self.highlight_carousel_events.items()))
        # *********** reading frontend date and time ***********
        actual_event_date_time = event.event_time
        # ********** getting start time from ss call and converting to the local ********************************
        if self.brand == "ladbrokes":
            future_date_formate = '%H:%M %d %b'
            ui_format_pattern = '%H:%M Today'
        else:
            future_date_formate = '%H:%M, %d %b'
            ui_format_pattern = '%H:%M, Today'
        expected_event_start_date_time = self.convert_time_to_local(
            date_time_str=self.events_start_time.get(event_name.upper()),
            ui_format_pattern=ui_format_pattern,
            ob_format_pattern=self.ob_format_pattern,
            ss_data=True, future_datetime_format=future_date_formate)
        self.assertEqual(expected_event_start_date_time, actual_event_date_time,
                         msg=f"{actual_event_date_time} is not equal to expected_event_start_date_time {expected_event_start_date_time}")
        # ***************validating whether the event contains bet buttons *******************************
        bet_buttons = event.get_all_prices()
        self.assertTrue(bet_buttons,
                        msg=f"event does not contain bet buttons for the event in the created highlight carousel{self.highlights_carousel_name_1}")
        # ******** Verification of Highlight Carousel event odds header *************************
        expected_list = ['HOME', 'DRAW', 'AWAY']
        actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
        self.assertListEqual(expected_list, actual_list,
                             f'actual headers of odds is {actual_list} is not same as expected odds headers {expected_list}')
        bet_button = next(iter(bet_buttons.values()))
        bet_button.click()
        self.site.quick_bet_panel.close()
        self.assertTrue(bet_button.is_selected(), f'unable to select bet buttons')

    def test_007_7_validate_the_events_are_displayed_as_per_events_display_in_typeleague_if_morethan_one_event_present_in_highlights_carousel(
            self):
        """
        DESCRIPTION: 7. Validate the Events are displayed as per events display in Type/League if morethan one event present in Highlights Carousel
        EXPECTED: 7. Events Should be displayed as per events display in Type/League if morethan one event present in Highlights Carousel
        """
        # created highlight carousel with event id this can't validate in this script

    def test_008_8_validate_the_see_all_link_if_created_highlights_carousel_with_typeid(self):
        """
        DESCRIPTION: 8. Validate the See All link if created Highlights Carousel with TypeId
        EXPECTED: 8. See All link should be displayed and navigates to respective event Type/league upon clicking on it
        EXPECTED: - See All link should not be displayed if created with EventId
        """
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        # getting the highlight carousel which we created among all the highlight carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        highlight_carousel.scroll_to()
        highlight_carousel_see_all_status = highlight_carousel.has_see_all_link(expected_result=False)
        self.assertFalse(highlight_carousel_see_all_status, msg="Highlight carousel contains see all link")
        events_section = highlight_carousel.items_as_ordered_dict
        event_names = list(events_section.keys())
        event = events_section.get(event_names[0])
        event.click()
        self.site.wait_content_state_changed()
        current_event = self.device.get_current_url()
        self.assertIn(self.event_id_1, current_event,
                      msg="user is not navigated to event detail page when clicking on event in highlight carousel")

    def test_009_9_validate_user_navigates_back_to_event_hub_tab___upon_clicking_browser_back_button(self):
        """
        DESCRIPTION: 9. Validate user navigates back to Event Hub tab - upon clicking Browser back button
        EXPECTED: 9. User should navigate back to Event Hub
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed()
        current_url = self.device.get_current_url()
        self.assertIn(str(self.index_number), current_url,
                      msg="user is not navigated to Event Hub tab when clicking browser back button from event detail page")

    def test_010_10_verify_the_highlight_carousel_display_from_and_to_date(self):
        """
        DESCRIPTION: 10. Verify the Highlight Carousel Display From and To date
        EXPECTED: 10. Highlights Carousel should be displayed based on CMS config start date in Event Hub
        EXPECTED: - Highlights Carousel should be disappeared based on CMS config end date in Event Hub
        """
        # covered in below steps

    def test_011_11_verify_live_watch_live_icons_display(self):
        """
        DESCRIPTION: 11. Verify live, Watch Live icons display
        EXPECTED: 11. Live icons should display for inplay events.
        EXPECTED: - If event has streaming watch live icon should display
        """
        # created highlights_carousels with preplay eventid so we cant cover this step  in this test case

    def test_012_12_verify_highlights_carousel_price_and_score_updates_color_change_as_per_brand_for_in_play_event(
            self):
        """
        DESCRIPTION: 12. Verify Highlights Carousel price and score updates, color change as per brand for in-play event
        EXPECTED: 12. Price and score updates, color change should happen
        """
        # created highlights_carousels with preplay eventid so we cant cover this step  in this test case

    def test_013_13_verify_highlights_carousel_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: 13. Verify Highlights Carousel display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: 13. Highlights Carousel should display with green(coral)/orange(lads) dots for inplay events
        """
        # created highlights_carousels with preplay eventid so we cant cover this step  in this test case

    def test_014_14_verify_highlights_carousel_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: 14. Verify Highlights Carousel 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: 14. Highlights Carousel should not be displayed in FE
        """

    #     covered in test case C65857286

    def test_015_15_verify_highlights_carousel_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: 15. Verify Highlights Carousel 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: 15.  Highlights Carousel should disappear in FE
        """
        #     covered in test case C65857286

    def test_016_16_verify_highlights_carousel_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: 16. Verify Highlights Carousel 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: 16. Highlights Carousel should display as per 'Display from' time
        """
        #     covered in test case C65857286

    def test_017_17_verify_highlights_carousel_display_if_it_has_more_than_3_events(self):
        """
        DESCRIPTION: 17. Verify Highlights Carousel display if it has more than 3 events
        EXPECTED: 17. Highlights Carousel with Right or Left arrow should display for only 3 events
        """

    #     can't cover in this test case because it created using event id only one event is present,C65857286

    def test_018_18_verify_highlights_carousel_left_and_right_scroll(self):
        """
        DESCRIPTION: 18. Verify Highlights Carousel left and right scroll
        EXPECTED: 18. User should able to scroll from left to right &amp; from right to left
        """
        # can't cover in this test case because it created using event id only one event is present,C65857286

    def test_019_19_verify_the_chevron_on_highlights_carousel_amp_navigation(self):
        """
        DESCRIPTION: 19. Verify the chevron on Highlights Carousel &amp; navigation
        EXPECTED: 19. Highlights Carousel Chevron should be in blue color and aligned to right &amp;  should redirect to EDP of that event upon clicking on it
        """
        # covered in above steps

    def test_020_20_verify_highlights_carousel_no_of_events_display(self):
        """
        DESCRIPTION: 20. Verify Highlights Carousel No of events display
        EXPECTED: 20. Highlights Carousel No of events should be displayed as per CMS value
        """
        # test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time

    def test_021_21_verify_the_set_details_amp_score_detailssgp_for_tennis_inplay_events(self):
        """
        DESCRIPTION: 21. Verify the set details &amp; score details(S,G,P) for Tennis inplay events
        EXPECTED: 21. Set 'n' and S,G,P scores should display &amp; align properly
        """
        # test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time

    def test_022_22_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_highlights_carousel(
            self):
        """
        DESCRIPTION: 22. Verify selections are displaying properly according to the sports/markets in Highlights Carousel
        EXPECTED: 22. Selections should display according to the sports/markets (Ex: Football HOME DRAW AWAY, Tennis 1 2)
        """
        # test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time

    def test_023_23_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_premier_league_or_championship(
            self):
        """
        DESCRIPTION: 23. Verify Team kits when HC is configured using the Type ID for the Premier League or Championship
        EXPECTED: 23. Highlights Carousel with the team kits should display
        """
        # covered in test cases C65857286

    def test_024_24_verify_highlights_carousel_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(
            self):
        """
        DESCRIPTION: 24. Verify Highlights Carousel navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: 24. User should navigate to the EDP of the event
        """
        # covered in  test_008_8_validate_the_see_all_link_if_created_highlights_carousel_with_typeid

    def test_025_25_verify_user_is_able_to_select_the_selections_on_highlights_carousel(self):
        """
        DESCRIPTION: 25. Verify user is able to select the selections on Highlights Carousel
        EXPECTED: 25. User should be able to select &amp; selections should be highlighted
        """
        # covered in above step test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time

    def test_026_26_activatedeactivate_the_whole_highlights_carousel_module_in_events_hub(self):
        """
        DESCRIPTION: 26. Activate/Deactivate the whole Highlights carousel module in Events Hub
        EXPECTED: 26. Highlights Carousel should display on Event Hub if it is activated
        EXPECTED: - Highlights Carousel should not display on Event Hub if it is deactivated
        """
        self.check_module_status_and_create_hightlight_carousel(index_number=self.index_number, active=False)
        status_highlight_carousle = self.site.home.tab_content.has_highlight_carousels(expected_result=False)
        self.assertFalse(status_highlight_carousle,
                         msg=f'highlight carousels tab is present in the event hub tab{self.event_hub_tab_name}')
        self.check_module_status_and_create_hightlight_carousel(index_number=self.index_number, create_high_light=False)

    def test_027_27_verify_display_of_event_cards_when_the_event_is_resulted_in_highlights_carousel(self):
        """
        DESCRIPTION: 27. Verify display of event cards when the event is resulted in Highlights carousel
        EXPECTED: 27. The resulted event should be removed from the Highlights carousel automatically
        """
        # can't automate as we are using exiting events from ss call we can't get the event which is already resulted

    def test_028_28_verify_display_of_highlights_carousel_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(
            self):
        """
        DESCRIPTION: 28. Verify display of Highlights carousel when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: 28. The event card should be removed from Highlights carousel and the Highlights carousel should be removed from the Event Hub
        """
        # can't automate as we are using exiting events from ss call we can't get the event which is already resulted

    def test_029_29_verify_highlights_carousel_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: 29. Verify Highlights carousel disappears in FE upon deletion in CMS
        EXPECTED: 29. Highlights Carousel should disappear in FE
        """
        created_highlight_carousel_2 = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_titles[1],
            events=[self.event_id_2],
            page_type='eventhub',
            sport_id=self.index_number, limit=1)
        highlight_carousel_id2 = created_highlight_carousel_2.get('id')
        # checking whether there are surface bets in event hub tab
        status_highlight_carousel = self.site.home.tab_content.has_highlight_carousels(expected_result=True)
        self.assertTrue(status_highlight_carousel,
                        msg=f'created highlight carousels {self.highlights_carousel_name_2} is not present in the event hub tab{self.event_hub_tab_name}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        highlight_carousel.scroll_to()
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_2} for  user')

        self.cms_config.delete_highlights_carousel(highlight_carousel_id=highlight_carousel_id2)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id2)
        # checking whether there are surface bets in event hub tab
        status_highlight_carousel = self.site.home.tab_content.has_highlight_carousels(expected_result=True)
        self.assertTrue(status_highlight_carousel,
                        msg=f'created highlight carousels {self.highlights_carousel_name_1} is not present in the event hub tab{self.event_hub_tab_name}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_2)
        self.assertFalse(highlight_carousel,
                         msg=f'Failed to undisplayed Highlights Carousel named {self.highlights_carousel_name_2}')

    def test_030_30_verify_edited_field_changes_are_reflecting_in_fe_for_highlights_carousel_in_event_hub(self):
        """
        DESCRIPTION: 30. Verify Edited field changes are reflecting in FE for Highlights Carousel in Event Hub
        EXPECTED: 30. Edited fields data should be updated for Highlights Carousel in Event Hub
        """
        # covered in above steps

    def test_031_31_verify_highlights_carousel_display_for_loggedin_amp_logged_out_users(self):
        """
        DESCRIPTION: 31. Verify Highlights Carousel display for Loggedin &amp; Logged out users
        EXPECTED: 31. Highlights Carousel should display for all Loggedin &amp; Loggedout users
        """
        self.site.logout()
        # after logout user is navigated back to home page
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.device.refresh_page()
            self.device.driver.implicitly_wait(3)
            # getting tabs in home page tabs for mobile
            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            if self.event_hub_tab_name.upper() not in home_page_tab_names:
                wait_for_haul(20)
                self.device.refresh_page()
                home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
                home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
            self.assertIn(self.event_hub_tab_name, home_page_tab_names,
                          f'Created Event Hub tab:{self.event_hub_tab_name} is not found in '
                          f'Current Home Page tabs : {home_page_tab_names}')
            self.event_hub_tab_name = next((tab for tab in home_page_tabs if tab.upper() == self.event_hub_tab_name),
                                           None)
            # navigating to the event hub tab which is created
            home_page_tabs.get(self.event_hub_tab_name).click()
            self.assertEqual(self.site.home.tabs_menu.current,
                             self.event_hub_tab_name,
                             f'Tab is not switched after clicking the "{self.event_hub_tab_name}" tab')
        # checking whether there are highlight carousels in event hub tab
        status_highlight_carousel = self.site.home.tab_content.has_highlight_carousels(expected_result=True)
        self.assertTrue(status_highlight_carousel,
                        msg=f'created highlight carousels {self.highlights_carousel_name_1} is not present in the event hub tab{self.event_hub_tab_name}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_1)
        highlight_carousel.scroll_to()
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_1} for logedout user')
