from datetime import datetime
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from faker import Faker
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@vtest
class Test_C65857286_Verify_Highlights_Carousel_is_displayed_in_Event_Hub_if_created_with_TypeId_for_Primary_Market_Type(
    BaseBetSlipTest):
    """
    TR_ID: C65857286
    NAME: Verify Highlights Carousel is displayed in Event Hub if created with TypeId for Primary Market Type
    DESCRIPTION: This test case verifies display of Highlights Carousel in event hub with TypeId for Primary Market Type
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
    PRECONDITIONS: - TypeId/EventId (Create with TypeID)
    PRECONDITIONS: - Select market and Market Type will be auto selected (Select Market as Primary Market)
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
    faker = Faker()
    highlights_carousels_title = f'Autotest Highlight Carousel {faker.color_name()}'
    now = datetime.now()
    svg_icon = "football"
    end_date = f'{get_date_time_as_string(days=30)}T00:00:00.000Z'

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()

    def create_check_status_hightlight_carousel(self, index_number: int = None):
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(
            index_number)  # getting all modules for specific event hub
        hc_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL', page_id=index_number)
        elif hc_module_cms['disabled']:
            self.cms_config.change_sport_module_state(sport_module=hc_module_cms)
        #   Adding sports module to event hub
        self.__class__.highlights_carousels_response = self.cms_config.create_highlights_carousel(
                                                                            title=self.highlights_carousels_title,
                                                                            typeId=self.type_id,
                                                                            page_type='eventhub',
                                                                            sport_id=index_number,
                                                                            limit=2,
                                                                            svgId=self.svg_icon
                                                                        )
    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
        PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
        PRECONDITIONS: 1. Login to Environment specific CMS
        PRECONDITIONS: 2. Navigate to Sports Pages -->Event Hub
        PRECONDITIONS: 3. Click on Create Event Hub
        PRECONDITIONS: 4. Enter title and click on Create button
        PRECONDITIONS: 5. Click on Add Sport Module --> Select option from dropdown as Highlights Carousel
        """

        self.__class__.team_kits_available = True
        self.__class__.type_id, self.__class__.expected_type_name = None, None
        self.__class__.events_for_type_id, self.__class__.event_names_for_type_id = None, None

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)

            self.__class__.type_id, self.__class__.expected_type_name = \
                next(([event['event']['typeId'], event['event']['typeName']]
                      for event in events if event['event']['typeName'].title() in ['Championship', 'Premier League']),
                     [None, None])  # getting type id and type name

            if not self.type_id:  # if we don't have types with 'Championship' or 'Premier League' then getting type name and type id of first event
                self.__class__.team_kits_available = False
                self.__class__.type_id, self.__class__.expected_type_name = next(
                    ([event['event']['typeId'], event['event']['typeName']] for event in events), None)

            self.__class__.events_for_type_id = {event['event']['name']: event for event in events if
                                                 self.type_id == event['event']['typeId']}  # getting dictionary of events, with event name Key : event name, Value : event(ss response)
        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            self.type_id = event1[7]['event']['typeId']  # getting type id
            self.__class__.expected_type_name = event1[7]['event']['typeName']  # getting  type name
            self.__class__.events_for_type_id = {event1[7]['event']['name']: event1[7],
                                                 event2[7]['event']['name']: event2[7]}  # getting dictionary of events, with event name Key : event name, Value : event(ss response)
            self.team_kits_available = False
        self.__class__.event_names_for_type_id = list(self.events_for_type_id)  # getting event names

        # getitng tabs of module ribbon tab from cms and checking if any of them are event hub
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and
                                   tab['directiveName'] == 'EventHub' and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.event_hub_tab_name = next((tab for tab in self.tabs_cms if tab.upper() == 'US SPORTS'), None)
        if self.event_hub_tab_name is None:
            #     Creating the eventhub
            existing_event_hubs = self.cms_config.get_event_hubs()
            existed_index_numbers = [event_hub['indexNumber'] for event_hub in existing_event_hubs]
            # need a unique non-existing index for new Event hub
            self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_numbers)
            response = self.cms_config.create_event_hub(index_number=self.index_number)
            self.__class__.created_event_hub_id = response.get('id')
            #  Create the event hub name
            self.__class__.event_hub_name = f'Auto EventHub_{self.index_number}'
            #   Adding event hub to module ribbion tab
            internal_id = f'tab-eventhub-{self.index_number}'
            event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=self.index_number,
                                                                               display_date=True)
            self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        else:
            # getting index of the US SPORT event hub
            self.__class__.index_number = next((tab['hubIndex'] for tab in module_ribbon_tabs if
                                                tab['title'].upper() == self.event_hub_tab_name.upper()), None)
        # create or update the highlight carousel inn event hub
        self.create_check_status_hightlight_carousel(index_number=self.index_number)
        self.__class__.highlights_carousel_name = self.convert_highlights_carousel_title(
            self.highlights_carousels_title)

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
        self.device.refresh_page()
        wait_for_haul(5)
        # getting tabs in home page tabs for mobile
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        home_page_tab_names = list(tab.upper() for tab in home_page_tabs)
        if self.event_hub_tab_name not in home_page_tab_names:
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
        # checking whether there are highlight carousel in event hub tab
        staus_highlight_carousle = self.site.home.tab_content.has_highlight_carousels(expected_result=True)
        self.assertTrue(staus_highlight_carousle,
                        msg=f'created highlight carousels {self.highlights_carousel_name} is not present in the event hub tab{self.event_hub_tab_name}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')

    def test_003_3_validate_the_order_of_highlights_carousel_module_in_event_hub(self):
        """
        DESCRIPTION: 3. Validate the Order of Highlights Carousel Module in Event Hub
        EXPECTED: 3. Order of Highlights Carousel Module in Event Hub should be as per CMS config
        """
        # covered in C65857284

    def test_004_4_change_the_highlights_carousel_order_in_event_hub(self):
        """
        DESCRIPTION: 4. Change the Highlights Carousel order in Event Hub
        EXPECTED: 4. Order of Highlights Carousel Module in Event Hub should be as per CMS config
        """
        # covered in C65857284

    def test_005_5_validate_the_highlights_carousel_title_and_svg_icon(self):
        """
        DESCRIPTION: 5. Validate the Highlights Carousel Title and SVG Icon
        EXPECTED: 5. Title Name and SVG icon should be displayed as per CMS config
        """
        highlight_carousels = self.site.home.tab_content.highlight_carousels  # getting all highlight carousels

        # validating the title
        hc_names = [name.upper() for name in highlight_carousels]
        self.assertIn(self.highlights_carousels_title.upper(), hc_names,
                      f'{self.highlights_carousels_title.upper()} is not fount in {hc_names}')

        # validating the Svg Icon
        self.__class__.hc_ = next((hc for hc_name, hc in highlight_carousels.items() if
                                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        self.__class__.highlights_carousels_title = next(
            (hc_name for hc_name in highlight_carousels if hc_name.upper() == self.highlights_carousels_title.upper()),
            None)
        self.hc_.scroll_to_we()
        self.assertEqual(self.hc_.svg_icon_text, f'#{self.svg_icon}',
                         f'Svg Icon is not same as configured in CMS')

    def test_006_6_validate_the_team_names_and_selections_display_of_highlights_carousel_along_with_event_date_amp_start_time(
            self):
        """
        DESCRIPTION: 6. Validate the Team names and selections display of Highlights Carousel along with event Date &amp; Start Time
        EXPECTED: 6. Team names and selections display as per Typeid/Eventid config in CMS
        EXPECTED: - Event Date &amp; Start Time should be displayed above the team names
        """

        self.__class__.events = self.hc_.items_as_ordered_dict  # to get all events present in highlight carousel
        for event_key, event in self.events.items():  # iterating over the events
            event.scroll_to_we()
            self.assertIn(event.event_name, self.event_names_for_type_id,
                          f'{event.event_name} is not in {self.event_names_for_type_id}')

            fe_event_date = event.event_time  # getting event start date from Front End

            if self.brand == "ladbrokes":
                future_datetime_format = '%H:%M %d %b'
                ui_format_pattern = '%H:%M Today'
            else:
                future_datetime_format = '%H:%M, %d %b'
                ui_format_pattern = '%H:%M, Today'

            # formating the event start time(OB) as front end start time
            expected_event_start_date_time = self.convert_time_to_local(
                date_time_str=self.events_for_type_id[event.event_name]['event']['startTime'],
                # getting start time from OB
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True, future_datetime_format=future_datetime_format, ui_format_pattern=ui_format_pattern)

            self.assertEqual(fe_event_date, expected_event_start_date_time,
                             f'actual time {fe_event_date} is not same as expected time {expected_event_start_date_time}')

    def test_007_7_validate_the_events_are_displayed_as_per_events_display_in_typeleague_if_morethan_one_event_present_in_highlights_carousel(
            self):
        """
        DESCRIPTION: 7. Validate the Events are displayed as per events display in Type/League if more than one event present in Highlights Carousel
        EXPECTED: 7. Events Should be displayed as per events display in Type/League if more than one event present in Highlights Carousel
        """
        # covered in above step

    def test_008_8_validate_the_see_all_link_if_created_highlights_carousel_with_typeid(self):
        """
        DESCRIPTION: 8. Validate the See All link if created Highlights Carousel with TypeId
        EXPECTED: 8. See All link should be displayed and navigates to respective event Type/league upon clicking on it
        """
        self.hc_.scroll_to_we()
        self.assertTrue(self.hc_.has_see_all_link(expected_result=True),
                        f'See All link is not displyed')  # asserting the see all link present or not
        self.hc_.see_all_link.click()  # clicking the see all link
        actual_type_name = self.site.competition_league.title_section.type_name.text  # getting type name from Frontend
        self.assertEqual(actual_type_name, self.expected_type_name,
                         f'actual_type_name {actual_type_name} is not same as expeceted type name {self.expected_type_name}')  # verifying the Frontend Type name with Expected Type( which is getting from OB)

    def test_009_9_validate_user_navigates_back_to_event_hub_tab___upon_clicking_browser_back_button(self):
        """
        DESCRIPTION: 9. Validate user navigates back to Event Hub tab - upon clicking Browser back button
        EXPECTED: 9. User should navigate back to Event Hub
        """
        self.site.back_button_click()  # clicking on back button
        self.assertEqual(self.event_hub_tab_name, self.site.home.tabs_menu.current,
                         f'{self.event_hub_tab_name} is not selected while navigating to back')  # verifying the after clicking on back button navigating to back and current tab is expected event hub tab

    def test_010_10_verify_the_highlight_carousel_display_from_and_to_date(self):
        """
        DESCRIPTION: 10. Verify the Highlight Carousel Display From and To date
        EXPECTED: 10. Highlights Carousel should be displayed based on CMS config start date in Event Hub
        EXPECTED: - Highlights Carousel should be disappeared based on CMS config end date in Event Hub
        """
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now, time_format='%Y-%m-%dT%H:%M:%S.%f', url_encode=False,
                                      hours=-10)[:-3] + 'Z'  # formating the now time as CMS time format
        display_from = self.highlights_carousels_response[
            'displayFrom']  # getting "display from" time from CMS for Highlight Carousel which is created by script
        display_to = self.highlights_carousels_response[
            'displayTo']  # getting "display to" time from CMS for  Highlight Carousel which is created by script
        status = display_from < now < display_to  # checking now time is in between "display from" and "display to"
        self.assertTrue(status, f'highlights carousels is not displayed as per CMS configurations(in between start '
                              f'time and end time)')

    def test_011_11_verify_live_watch_live_icons_display(self):
        """
        DESCRIPTION: 11. Verify live, Watch Live icons display
        EXPECTED: 11. Live icons should display for inplay events.
        EXPECTED: - If event has streaming watch live icon should display
        """
        # covered in C65861228

    def test_012_12_verify_highlights_carousel_price_and_score_updates_color_change_as_per_brand_for_in_play_event(
            self):
        """
        DESCRIPTION: 12. Verify Highlights Carousel price and score updates, color change as per brand for in-play event
        EXPECTED: 12. Price and score updates, color change should happen
        """
        # covered in C65861228

    def test_013_13_verify_highlights_carousel_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: 13. Verify Highlights Carousel display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: 13. Highlights Carousel should display with green(coral)/orange(lads) dots for inplay events
        """
        # can't be automate

    def test_014_14_verify_highlights_carousel_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: 14. Verify Highlights Carousel 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: 14. Highlights Carousel should not be displayed in FE
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-20)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-15)[:-3] + 'Z'

        # setting the highlight carousel "display from" to past and "display to" to past
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, start_time=start_time,
                                                   end_time=end_time)
        wait_for_haul(20)
        self.device.refresh_page()

        section = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.highlights_carousels_title), timeout=2,
            refresh_count=1, ref=self)
        self.assertFalse(section, msg=f'{self.highlights_carousels_title} highlight carousel is available')

    def test_015_15_verify_highlights_carousel_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: 15. Verify Highlights Carousel 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: 15.  Highlights Carousel should disappear in FE
        """
        # covered in above step

    def test_016_16_verify_highlights_carousel_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: 16. Verify Highlights Carousel 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: 16. Highlights Carousel should display as per 'Display from' time
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=1)[:-3] + 'Z'

        # setting the highlight carousel "display from" to present time and "display to" to future time
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, start_time=start_time,
                                                   end_time=end_time)
        wait_for_haul(20)
        self.device.refresh_page()
        section = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.highlights_carousels_title), timeout=2,
            refresh_count=1, ref=self)
        self.assertTrue(section, msg=f'{self.highlights_carousels_title} highlight carousel is not available')

    def test_017_17_verify_highlights_carousel_display_if_it_has_more_than_3_events(self):
        """
        DESCRIPTION: 17. Verify Highlights Carousel display if it has more than 3 events
        EXPECTED: 17. Highlights Carousel with Right or Left arrow should display for only 3 events
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, limit=5)
        wait_for_haul(10)
        self.device.refresh_page()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        events = hc.items_as_ordered_dict

        # test_018_18_verify_highlights_carousel_left_and_right_scroll
        if len(events) > 3:
            hc.scroll_to_we()
            wait_for_haul(2)
            self.assertTrue(hc.has_next_button(expected_result=True), 'Next button is not displayed')
            hc.scroll_next_button.click()
            hc.scroll_to_we()
            wait_for_haul(5)
            self.assertTrue(hc.has_prev_button(expected_result=True), 'prev button is not displayed')
            hc.scroll_previous_button.click()

        # test_019_19_verify_the_chevron_on_highlights_carousel_amp_navigation
        wait_for_haul(2)
        event = next(iter(events.values()))
        event.click()
        self.site.wait_content_state('EventDetails')
        self.site.back_button_click()
        self.site.wait_content_state('HomePage')

    def test_018_18_verify_highlights_carousel_left_and_right_scroll(self):
        """
        DESCRIPTION: 18. Verify Highlights Carousel left and right scroll
        EXPECTED: 18. User should able to scroll from left to right &amp; from right to left
        """
        # covered in above step

    def test_019_19_verify_the_chevron_on_highlights_carousel_amp_navigation(self):
        """
        DESCRIPTION: 19. Verify the chevron on Highlights Carousel &amp; navigation
        EXPECTED: 19. Highlights Carousel Chevron should be in blue color and aligned to right &amp;  should redirect to EDP of that event upon clicking on it
        """
        # covered in above step

    def test_020_20_verify_highlights_carousel_no_of_events_display(self):
        """
        DESCRIPTION: 20. Verify Highlights Carousel No of events display
        EXPECTED: 20. Highlights Carousel No of events should be displayed as per CMS value
        """
        no_of_events_to_displyed = 1
        self.cms_config.update_highlights_carousel(highlight_carousel=self.highlights_carousels_response,
                                                   limit=no_of_events_to_displyed)
        wait_for_haul(25)
        self.device.refresh_page()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        hc.scroll_to_we()
        events = hc.items_as_ordered_dict
        self.assertEqual(no_of_events_to_displyed, len(events), f'No.of events to displayed is not sane as CMS config')

        event = next(iter(events.values()))

        # test_023_23_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_premier_league_or_championship
        self.assertEqual(event.has_team_kits, self.team_kits_available, f'teams kits are not available')

        # test_022_22_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_highlights_carousel
        event.scroll_to_we()
        expected_event_name = event.event_name
        bet_buttons = event.get_all_prices()
        expected_list = ['HOME', 'DRAW', 'AWAY']
        actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
        self.assertListEqual(expected_list, actual_list,
                             f'actual headers of odds is {actual_list} is not same as expected odds headers {expected_list}')

        # test_025_25_verify_user_is_able_to_select_the_selections_on_highlights_carousel
        event.scroll_to_we()
        bet_button = next(iter(bet_buttons.values()))
        index_of_bet_button = list(bet_buttons.values()).index(bet_button)
        expected_selection_name = expected_event_name.split(' v ')[index_of_bet_button].strip()
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), f'unable to select bet buttons')

        # quick bet
        quick_bet = self.site.quick_bet_panel
        event_name_on_qd_panel = quick_bet.selection.content.event_name
        self.assertEqual(expected_event_name.upper(), event_name_on_qd_panel.upper(), f'expected event name : {expected_event_name} is not same as actual event name on QD panel : {event_name_on_qd_panel}')
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        qb_market_name = quick_bet.selection.content.market_name
        qd_odd = quick_bet.selection.content.odds
        self.site.wait_content_state_changed()
        quick_bet.place_bet.click()
        bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

        # bet placement through reuse selection
        quick_bet.bet_receipt.reuse_selection_button.click()
        self.assertTrue(bet_button.is_selected(), f'bet button is not selected after clicking on reuse selection')
        self.site.open_betslip()
        bestslip_sections = self.site.betslip.betslip_sections_list.ordered_collection.get('Single').ordered_collection
        betslip_selections_names = list(bestslip_sections.keys())
        selection_name, selection = next(([name, selection] for name, selection in bestslip_sections.items() if name.upper() == expected_selection_name.upper()), [None,None])
        self.assertIsNotNone(selection_name, f'expected selection name : "{expected_selection_name}" is not in bet slip selections : "{betslip_selections_names}"')
        self.assertEqual(qb_market_name.upper(), selection.market_name.upper(), f'market name on quick bet panel : "{qb_market_name}" is not same as in betslip section : "{selection.market_name.upper()}" ')
        self.assertEqual(qd_odd, selection.odds, f'odds on quick bet panel : "{qd_odd}" is not same as in betslip section : "{selection.odds}" ')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        event_name_on_betslip = self.site.bet_receipt.event_description
        self.assertEqual(expected_event_name, event_name_on_betslip, f'actual event name on betslip : "{event_name_on_betslip}" is not same as expected event name "{expected_event_name}"')
        self.site.close_betreceipt()

    def test_021_21_verify_the_set_details_amp_score_detailssgp_for_tennis_inplay_events(self):
        """
        DESCRIPTION: 21. Verify the set details &amp; score details(S,G,P) for Tennis inplay events
        EXPECTED: 21. Set 'n' and S,G,P scores should display &amp; align properly
        """
        # covered in C65861230

    def test_022_22_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_highlights_carousel(
            self):
        """
        DESCRIPTION: 22. Verify selections are displaying properly according to the sports/markets in Highlights Carousel
        EXPECTED: 22. Selections should display according to the sports/markets (Ex: Football HOME DRAW AWAY, Tennis 1 2)
        """
        # covered in above step

    def test_023_23_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_premier_league_or_championship(
            self):
        """
        DESCRIPTION: 23. Verify Team kits when HC is configured using the Type ID for the Premier League or Championship
        EXPECTED: 23. Highlights Carousel with the team kits should display
        """
        # covered in above step

    def test_024_24_verify_highlights_carousel_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(
            self):
        """
        DESCRIPTION: 24. Verify Highlights Carousel navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: 24. User should navigate to the EDP of the event
        """
        # covered in above steps

    def test_025_25_verify_user_is_able_to_select_the_selections_on_highlights_carousel(self):
        """
        DESCRIPTION: 25. Verify user is able to select the selections on Highlights Carousel
        EXPECTED: 25. User should be able to select &amp; selections should be highlighted
        """
        # covered in above step

    def test_026_26_activatedeactivate_the_whole_highlights_carousel_module_in_events_hub(self):
        """
        DESCRIPTION: 26. Activate/Deactivate the whole Highlights carousel module in Events Hub
        EXPECTED: 26. Highlights Carousel should display on Event Hub if it is activated
        EXPECTED: - Highlights Carousel should not display on Event Hub if it is deactivated
        """
        #  covered whole activate and deactivate in C65857284

        # here validating deactivating and activating the highlight carousel which is created by script
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, disabled=True)
        wait_for_haul(20)
        self.device.refresh_page()
        hc = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.highlights_carousels_title), timeout=2,
            refresh_count=1, ref=self)
        self.assertFalse(hc, 'Highlight Carousel still displyed after disabled')

        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, disabled=False)
        wait_for_haul(20)
        self.device.refresh_page()
        hc = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.highlights_carousels_title), timeout=2,
            refresh_count=1, ref=self)
        self.assertTrue(hc, 'Highlight Carousel not displyed after enabled')

    def test_027_27_verify_display_of_event_cards_when_the_event_is_resulted_in_highlights_carousel(self):
        """
        DESCRIPTION: 27. Verify display of event cards when the event is resulted in Highlights carousel
        EXPECTED: 27. The resulted event should be removed from the Highlights carousel automatically
        """
        # can not be automated

    def test_028_28_verify_display_of_highlights_carousel_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(
            self):
        """
        DESCRIPTION: 28. Verify display of Highlights carousel when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: 28. The event card should be removed from Highlights carousel and the Highlights carousel should be removed from the Event Hub
        """
        # can not be automated

    def test_029_29_verify_highlights_carousel_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: 29. Verify Highlights carousel disappears in FE upon deletion in CMS
        EXPECTED: 29. Highlights Carousel should disappear in FE
        """
        # covered in below step "test_031_31_verify_highlights_carousel_display_for_loggedin_amp_logged_out_users"

    def test_030_30_verify_edited_field_changes_are_reflecting_in_fe_for_highlights_carousel_in_event_hub(self):
        """
        DESCRIPTION: 30. Verify Edited field changes are reflecting in FE for Highlights Carousel in Event Hub
        EXPECTED: 30. Edited fields data should be updated for Highlights Carousel in Event Hub
        """
        no_of_events_to_displyed = 2

        # upadating the svg icon and limit of events displyed in highlight carousel
        self.svg_icon = "footballnew"
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, limit=2, svgId=self.svg_icon)

        wait_for_haul(20)
        self.device.refresh_page()

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        hc.scroll_to_we()
        self.assertEqual(hc.svg_icon_text, f'#{self.svg_icon}',
                         f'Svg Icon is not same as configured in CMS')
        events = hc.items_as_ordered_dict
        actual_no_of_events_displyed = len(events)
        self.assertEqual(actual_no_of_events_displyed, no_of_events_to_displyed,
                         f'Number of events displyed is not same as configured in CMS')

    def test_031_31_verify_highlights_carousel_display_for_loggedin_amp_logged_out_users(self):
        """
        DESCRIPTION: 31. Verify Highlights Carousel display for Loggedin &amp; Logged out users
        EXPECTED: 31. Highlights Carousel should display for all Loggedin &amp; Loggedout users
        """

        # logout and verifying the highlight carousel presence
        self.site.logout()
        tabs = self.site.home.tabs_menu.items_as_ordered_dict
        tabs.get(self.event_hub_tab_name).click()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        self.assertIsNotNone(hc, f'Highlight Carousel {self.highlights_carousels_title} is not displyed after logout')

        # login and verifying the highlight carousel presence
        self.site.login()
        tabs = self.site.home.tabs_menu.items_as_ordered_dict
        tabs.get(self.event_hub_tab_name).click()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        self.assertIsNotNone(hc, f'Highlight Carousel {self.highlights_carousels_title} is not displyed after login')

        # deleting the highlight carousel and verifying it's presence in Frontend
        self.cms_config.delete_highlights_carousel(highlight_carousel_id=self.highlights_carousels_response['id'])
        self.cms_config._created_highlights_carousels.remove(self.highlights_carousels_response['id'])
        wait_for_haul(6)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        tabs = self.site.home.tabs_menu.items_as_ordered_dict
        tabs.get(self.event_hub_tab_name).click()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        hc = next((hc_ for hc_name, hc_ in highlight_carousels.items() if
                   hc_name.upper() == self.highlights_carousels_title.upper()), None)
        self.assertFalse(hc, f'Highlight Carousel {self.highlights_carousels_title} is displayed after deletion')
